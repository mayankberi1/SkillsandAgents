"""Allowlisted Gmail operations and safe response normalization."""

from __future__ import annotations

import base64
import binascii
import json
from collections.abc import Callable
from email.message import Message
from typing import Any

from google.auth.exceptions import GoogleAuthError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import auth


class GmailError(Exception):
    """A safe Gmail failure with a stable category."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _call(operation: Callable[[], Any]) -> Any:
    try:
        return operation()
    except HttpError as error:
        status = error.resp.status
        try:
            details = json.loads(error.content)
            error_details = details.get("error", {})
            reasons = {item.get("reason") for item in
                       error_details.get("errors", []) + error_details.get("details", [])}
        except (ValueError, TypeError, AttributeError):
            reasons = set()
        if status == 403 and reasons & {"insufficientPermissions", "ACCESS_TOKEN_SCOPE_INSUFFICIENT"}:
            raise GmailError("insufficient_scope", "Run `auth setup` again to grant Gmail readonly access.") from error
        if status == 403 and reasons & {"rateLimitExceeded", "userRateLimitExceeded"}:
            status = 429
        code, message = {
            400: ("invalid_input", "Gmail rejected the request. Check the query or ID."),
            401: ("reauthorization_required", "Run `auth setup` again to authorize Gmail."),
            403: ("permission_denied", "Gmail denied access. Check account permissions and API access."),
            404: ("not_found", "The requested Gmail message was not found."),
            429: ("rate_limited", "Gmail rate limit reached. Retry later."),
        }.get(status, ("api_unavailable", "Gmail is unavailable. Retry later."))
        raise GmailError(code, message) from error
    except GoogleAuthError as error:
        raise GmailError("reauthorization_required", "Run `auth setup` again to authorize Gmail.") from error
    except OSError as error:
        raise GmailError("api_unavailable", "Could not connect to Gmail. Retry later.") from error


def _service(*, modify: bool = False) -> Any:
    credentials = auth.credentials_for_use(modify=True) if modify else auth.credentials_for_use()
    return _call(lambda: build("gmail", "v1", credentials=credentials, cache_discovery=False))


def _summary(message: dict[str, Any]) -> dict[str, Any]:
    headers = {
        header["name"].lower(): header.get("value", "")
        for header in message.get("payload", {}).get("headers", [])
    }
    return {
        "id": message["id"],
        "thread_id": message.get("threadId"),
        "subject": headers.get("subject", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "date": headers.get("date", ""),
        "snippet": message.get("snippet", ""),
        "label_ids": message.get("labelIds", []),
    }


def search(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Return at most limit summaries, following Gmail pagination as necessary."""
    if not query.strip() or not 1 <= limit <= 500:
        raise GmailError("invalid_input", "Supply a nonempty query and a limit from 1 to 500.")
    messages = _service().users().messages()
    results: list[dict[str, Any]] = []
    page_token = None
    seen_tokens: set[str] = set()
    pages = 0
    while len(results) < limit:
        if pages >= limit:
            raise GmailError("api_unavailable", "Gmail pagination exceeded the request budget. Retry later.")
        pages += 1
        page = _call(lambda: messages.list(
            userId="me", q=query, maxResults=limit - len(results), pageToken=page_token,
        ).execute())
        for item in page.get("messages", [])[:limit - len(results)]:
            message = _call(lambda: messages.get(
                userId="me", id=item["id"], format="metadata",
                metadataHeaders=["Subject", "From", "To", "Date"],
            ).execute())
            results.append(_summary(message))
        next_token = page.get("nextPageToken")
        if not next_token or len(results) >= limit:
            break
        if next_token in seen_tokens:
            raise GmailError("api_unavailable", "Gmail returned a repeated page token. Retry later.")
        seen_tokens.add(next_token)
        page_token = next_token
    return results


def _body_parts(part: dict[str, Any]) -> list[dict[str, str]]:
    headers = Message()
    for header in part.get("headers", []):
        if header["name"].lower() in ("content-type", "content-disposition"):
            headers[header["name"]] = header.get("value", "")
    # Exclude whole attachment subtrees even when Gmail supplies no filename.
    if part.get("filename") or headers.get_content_disposition() == "attachment":
        return []
    result = []
    mime_type = part.get("mimeType", "")
    data = part.get("body", {}).get("data")
    if mime_type in ("text/plain", "text/html") and data:
        try:
            decoded = base64.b64decode(data + "=" * (-len(data) % 4), altchars=b"-_", validate=True)
        except (ValueError, binascii.Error) as error:
            raise GmailError("api_unavailable", "Gmail returned invalid message content.") from error
        charset = headers.get_content_charset() or "utf-8"
        try:
            text = decoded.decode(charset, errors="replace")
        except LookupError:
            text = decoded.decode("utf-8", errors="replace")
        result.append({"mime_type": mime_type, "text": text})
    for child in part.get("parts", []):
        result.extend(_body_parts(child))
    return result


def get_message(message_id: str) -> dict[str, Any]:
    """Fetch metadata and inline text/HTML, without marking a message read."""
    if not message_id.strip():
        raise GmailError("invalid_input", "Supply a nonempty message ID.")
    messages = _service().users().messages()
    message = _call(lambda: messages.get(userId="me", id=message_id, format="full").execute())
    result = _summary(message)
    result["body_parts"] = _body_parts(message.get("payload", {}))
    return result


def list_labels() -> list[dict[str, Any]]:
    """List API-provided label identity and optional counts/visibility."""
    labels = _service().users().labels()
    response = _call(lambda: labels.list(userId="me").execute())
    fields = ("id", "name", "type", "messageListVisibility", "labelListVisibility",
              "messagesTotal", "messagesUnread", "threadsTotal", "threadsUnread")
    return [{field: label[field] for field in fields if field in label}
            for label in response.get("labels", [])]


def change_label(message_id: str, label_id: str, action: str) -> dict[str, Any]:
    """Apply/remove one label after the caller obtains exact user confirmation."""
    if action not in ("apply", "remove"):
        raise GmailError("invalid_input", "Choose apply or remove for the label action.")
    if any(not identifier or any(character.isspace() for character in identifier)
           for identifier in (message_id, label_id)):
        raise GmailError("invalid_input", "Supply one nonempty message ID and one label ID without whitespace.")
    if label_id in {"TRASH", "SPAM", "SENT", "DRAFT"} or (label_id == "INBOX" and action == "remove"):
        raise GmailError("invalid_input", "That system-label change is outside this skill's label-management scope.")
    messages = _service(modify=True).users().messages()
    field = "addLabelIds" if action == "apply" else "removeLabelIds"
    response = _call(lambda: messages.modify(
        userId="me", id=message_id, body={field: [label_id]},
    ).execute())
    return {"id": response["id"], "label_ids": response.get("labelIds", []),
            "action": action, "label_id": label_id}
