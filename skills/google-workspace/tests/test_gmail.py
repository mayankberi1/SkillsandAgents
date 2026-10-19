"""Offline read-only Gmail API and CLI behavior checks."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import auth  # noqa: E402
import gmail  # noqa: E402
import gmail_api  # noqa: E402


class FakeResource:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def list(self, **kwargs):
        self.calls.append(("list", kwargs))
        return self

    def get(self, **kwargs):
        self.calls.append(("get", kwargs))
        return self

    def execute(self):
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def service(monkeypatch, responses):
    resource = FakeResource(responses)
    users = SimpleNamespace(messages=lambda: resource, labels=lambda: resource)
    monkeypatch.setattr(gmail_api, "_service", lambda: SimpleNamespace(users=lambda: users))
    return resource


def message(identifier="abc"):
    return {"id": identifier, "threadId": "thread", "labelIds": ["UNREAD"],
            "payload": {"headers": [{"name": "sUbJeCt", "value": "Hello"}]}}


def test_search_paginates_hydrates_and_respects_limit(monkeypatch):
    resource = service(monkeypatch, [
        {"messages": [{"id": "a"}], "nextPageToken": "page2"}, message("a"),
        {"messages": [{"id": "b"}], "nextPageToken": "page3"}, message("b"),
    ])
    result = gmail_api.search("is:unread", 2)
    assert [item["id"] for item in result] == ["a", "b"]
    assert result[0]["subject"] == "Hello"
    assert result[0]["label_ids"] == ["UNREAD"]
    assert resource.calls[0] == ("list", {"userId": "me", "q": "is:unread", "maxResults": 2, "pageToken": None})
    assert resource.calls[2][1]["pageToken"] == "page2"
    assert resource.calls[2][1]["maxResults"] == 1
    assert all(call[0] in ("list", "get") for call in resource.calls)


def test_empty_search_and_labels(monkeypatch):
    service(monkeypatch, [{}, {}])
    assert gmail_api.search("in:inbox") == []
    assert gmail_api.list_labels() == []


@pytest.mark.parametrize("query,limit", [(" ", 20), ("x", 0), ("x", 501)])
def test_invalid_search_never_authenticates(monkeypatch, query, limit):
    monkeypatch.setattr(gmail_api, "_service", lambda: pytest.fail("unexpected authentication"))
    with pytest.raises(gmail_api.GmailError, match="nonempty") as error:
        gmail_api.search(query, limit)
    assert error.value.code == "invalid_input"


def test_nested_body_charset_html_and_attachment_exclusion(monkeypatch):
    def part(kind, data, **extra):
        return {"mimeType": kind, "body": {"data": base64.urlsafe_b64encode(data).decode().rstrip("=")}, **extra}
    payload = message()
    payload["payload"]["parts"] = [{"mimeType": "multipart/alternative", "parts": [
        part("text/plain", b"caf\xe9", headers=[{"name": "Content-Type", "value": "text/plain; charset=iso-8859-1"}]),
        part("text/html", b"<b>Hello</b>"),
        part("text/plain", b"private attachment", filename="note.txt"),
    ]}]
    resource = service(monkeypatch, [payload])
    result = gmail_api.get_message("abc")
    assert result["body_parts"] == [{"mime_type": "text/plain", "text": "café"}, {"mime_type": "text/html", "text": "<b>Hello</b>"}]
    assert resource.calls == [("get", {"userId": "me", "id": "abc", "format": "full"})]


def test_message_without_body_and_invalid_body(monkeypatch):
    service(monkeypatch, [message(), {"id": "x", "payload": {"mimeType": "text/plain", "body": {"data": "!!"}}}])
    assert gmail_api.get_message("abc")["body_parts"] == []
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.get_message("x")
    assert error.value.code == "api_unavailable"


def test_empty_message_id_rejected_before_auth(monkeypatch):
    monkeypatch.setattr(gmail_api, "_service", lambda: pytest.fail("unexpected authentication"))
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.get_message(" ")
    assert error.value.code == "invalid_input"


def test_labels_preserve_provided_fields(monkeypatch):
    label = {"id": "INBOX", "name": "INBOX", "type": "system", "messagesUnread": 3, "labelListVisibility": "labelShow"}
    resource = service(monkeypatch, [{"labels": [label]}])
    assert gmail_api.list_labels() == [label]
    assert resource.calls == [("list", {"userId": "me"})]


@pytest.mark.parametrize("status,code", [(400,"invalid_input"), (401,"reauthorization_required"), (403,"permission_denied"), (404,"not_found"), (429,"rate_limited"), (503,"api_unavailable")])
def test_http_errors_are_safe(monkeypatch, status, code):
    response = SimpleNamespace(status=status, reason="private reason")
    service(monkeypatch, [HttpError(response, b'{"error":{"message":"private content"}}')])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.list_labels()
    assert error.value.code == code
    assert "private" not in str(error.value)


def test_transport_failure_safe(monkeypatch):
    service(monkeypatch, [OSError("private endpoint")])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.list_labels()
    assert error.value.code == "api_unavailable"
    assert "private" not in str(error.value)


def test_service_uses_existing_credentials_and_no_discovery_cache(monkeypatch):
    credentials = object()
    monkeypatch.setattr(auth, "credentials_for_use", lambda: credentials)
    captured = {}
    def build(*args, **kwargs):
        captured.update(kwargs)
        assert args == ("gmail", "v1")
        return "service"
    monkeypatch.setattr(gmail_api, "build", build)
    assert gmail_api._service() == "service"
    assert captured == {"credentials": credentials, "cache_discovery": False}


@pytest.mark.parametrize("arguments,function,expected", [
    (["gmail","search","--query","in:inbox"], "search", ("in:inbox",20)),
    (["gmail","get","--message-id","abc"], "get_message", ("abc",)),
    (["gmail","labels","list"], "list_labels", ()),
])
def test_cli_dispatch(monkeypatch, capsys, arguments, function, expected):
    def operation(*args):
        assert args == expected
        return []
    monkeypatch.setattr(gmail_api, function, operation)
    assert gmail.main(arguments) == 0
    assert json.loads(capsys.readouterr().out) == []


def test_cli_unexpected_failure_does_not_leak(monkeypatch, capsys):
    def fail():
        raise RuntimeError("private response")
    monkeypatch.setattr(gmail_api, "list_labels", fail)
    assert gmail.main(["gmail", "labels", "list"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"] == "internal_error"
    assert "private" not in captured.err


@pytest.mark.parametrize("action", ["send", "trash", "archive", "create", "rename", "delete"])
def test_mutations_not_exposed(action):
    with pytest.raises(SystemExit) as error:
        gmail.main(["gmail", "labels", action])
    assert error.value.code == 2


def test_quota_error_uses_rate_limited_category(monkeypatch):
    response = SimpleNamespace(status=403, reason="Forbidden")
    service(monkeypatch, [HttpError(response, b'{"error":{"errors":[{"reason":"userRateLimitExceeded"}]}}')])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.list_labels()
    assert error.value.code == "rate_limited"


def test_repeated_page_token_stops(monkeypatch):
    resource = service(monkeypatch, [{"nextPageToken": "a"}, {"nextPageToken": "b"}, {"nextPageToken": "a"}])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.search("x", 4)
    assert error.value.code == "api_unavailable"
    assert len(resource.calls) == 3


def test_cli_safe_api_error(monkeypatch, capsys):
    def fail():
        raise gmail_api.GmailError("not_found", "The message was not found.")
    monkeypatch.setattr(gmail_api, "get_message", lambda identifier: fail())
    assert gmail.main(["gmail", "get", "--message-id", "abc"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"] == "not_found"


@pytest.mark.parametrize("error_body", [
    {"error": {"errors": [{"reason": "insufficientPermissions"}]}},
    {"error": {"details": [{"reason": "ACCESS_TOKEN_SCOPE_INSUFFICIENT"}]}},
])
def test_insufficient_scope_has_distinct_safe_category(monkeypatch, error_body):
    response = SimpleNamespace(status=403, reason="Forbidden")
    service(monkeypatch, [HttpError(response, json.dumps(error_body).encode())])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.list_labels()
    assert error.value.code == "insufficient_scope"
    assert "auth setup" in str(error.value)


def test_filename_free_attachment_subtrees_are_excluded(monkeypatch):
    text = {"mimeType": "text/plain", "body": {"data": "cHJpdmF0ZQ"}}
    attachment = {**text, "headers": [{"name": "content-disposition", "value": "attachment"}]}
    nested_attachment = {"mimeType": "multipart/mixed", "headers": [
        {"name": "Content-Disposition", "value": "ATTACHMENT; filename=note.txt"}], "parts": [text]}
    payload = message()
    payload["payload"]["parts"] = [attachment, nested_attachment]
    service(monkeypatch, [payload])
    assert gmail_api.get_message("abc")["body_parts"] == []


def test_empty_pages_cannot_exceed_requested_limit(monkeypatch):
    resource = service(monkeypatch, [{"nextPageToken": str(i)} for i in range(10)])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.search("x", 1)
    assert error.value.code == "api_unavailable"
    assert len(resource.calls) == 1


def test_page_budget_does_not_return_partial_success(monkeypatch):
    resource = service(monkeypatch, [{"messages": [{"id": "a"}], "nextPageToken": "1"}, message("a"), {"nextPageToken": "2"}])
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.search("x", 2)
    assert error.value.code == "api_unavailable"
    assert len(resource.calls) == 3


@pytest.mark.parametrize("action,field", [("apply", "addLabelIds"), ("remove", "removeLabelIds")])
def test_exact_single_label_modification(monkeypatch, action, field):
    resource = FakeResource([{"id": "abc", "labelIds": ["Label_1"]}])
    def modify(**kwargs):
        resource.calls.append(("modify", kwargs))
        return resource
    resource.modify = modify
    def create_service(*, modify):
        assert modify is True
        return SimpleNamespace(users=lambda: SimpleNamespace(messages=lambda: resource))
    monkeypatch.setattr(gmail_api, "_service", create_service)
    result = gmail_api.change_label("abc", "Label_1", action)
    assert resource.calls == [("modify", {"userId": "me", "id": "abc", "body": {field: ["Label_1"]}})]
    assert result == {"id": "abc", "label_ids": ["Label_1"], "action": action, "label_id": "Label_1"}


@pytest.mark.parametrize("message_id,label_id,action", [
    ("", "Label_1", "apply"), ("abc", " ", "remove"), ("a b", "Label_1", "apply"),
    ("abc", "Label_1", "trash"), ("abc", "Label_1 Label_2", "apply"),
])
def test_invalid_mutation_rejected_before_auth(monkeypatch, message_id, label_id, action):
    monkeypatch.setattr(gmail_api, "_service", lambda **k: pytest.fail("unexpected auth"))
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.change_label(message_id, label_id, action)
    assert error.value.code == "invalid_input"


def test_readonly_token_never_reaches_mutation_endpoint(monkeypatch):
    def credentials(*, modify):
        assert modify is True
        raise auth.AuthError("insufficient_scope", "Explicit consent required.")
    monkeypatch.setattr(auth, "credentials_for_use", credentials)
    monkeypatch.setattr(gmail_api, "build", lambda *a, **k: pytest.fail("unexpected API construction"))
    with pytest.raises(auth.AuthError) as error:
        gmail_api.change_label("abc", "Label_1", "apply")
    assert error.value.code == "insufficient_scope"


@pytest.mark.parametrize("action", ["apply", "remove"])
def test_label_cli_exact_arguments(monkeypatch, capsys, action):
    def change(message_id, label_id, actual_action):
        assert (message_id, label_id, actual_action) == ("abc", "Label_1", action)
        return {"id": "abc", "action": action}
    monkeypatch.setattr(gmail_api, "change_label", change)
    assert gmail.main(["gmail", "labels", action, "--message-id", "abc", "--label-id", "Label_1"]) == 0
    assert json.loads(capsys.readouterr().out)["action"] == action


@pytest.mark.parametrize("extra", [["--query", "in:inbox"], ["--yes"], ["--confirmed"]])
def test_no_query_or_confirmation_flag_mutation_bypass(extra):
    with pytest.raises(SystemExit):
        gmail.main(["gmail", "labels", "apply", "--message-id", "abc", "--label-id", "Label_1", *extra])


def test_mutation_http_error_is_safe_and_not_retried(monkeypatch):
    resource = FakeResource([HttpError(SimpleNamespace(status=404, reason="private"), b'{"error":{"message":"private"}}')])
    def modify(**kwargs):
        resource.calls.append(("modify", kwargs))
        return resource
    resource.modify = modify
    monkeypatch.setattr(gmail_api, "_service", lambda **k: SimpleNamespace(users=lambda: SimpleNamespace(messages=lambda: resource)))
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.change_label("abc", "Label_1", "remove")
    assert error.value.code == "not_found"
    assert "private" not in str(error.value)
    assert len(resource.calls) == 1


@pytest.mark.parametrize("label_id,action", [
    ("TRASH", "apply"), ("TRASH", "remove"), ("SPAM", "apply"), ("SPAM", "remove"),
    ("SENT", "apply"), ("SENT", "remove"), ("DRAFT", "apply"), ("DRAFT", "remove"),
    ("INBOX", "remove"),
])
def test_excluded_system_label_aliases_rejected_before_auth(monkeypatch, label_id, action):
    monkeypatch.setattr(gmail_api, "_service", lambda **k: pytest.fail("unexpected auth"))
    with pytest.raises(gmail_api.GmailError) as error:
        gmail_api.change_label("abc", label_id, action)
    assert error.value.code == "invalid_input"
