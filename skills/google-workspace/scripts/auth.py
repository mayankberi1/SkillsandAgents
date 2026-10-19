"""Local-browser OAuth and fail-closed OS keyring persistence for Gmail."""

from __future__ import annotations

import json
from pathlib import Path

import keyring
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ("https://www.googleapis.com/auth/gmail.readonly",)
MODIFY_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
KEYRING_SERVICE = "google-workspace-gmail"
KEYRING_ACCOUNT = "default"

class AuthError(Exception):
    """A user-safe authentication failure with a stable category."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _secure_backend():
    try:
        return keyring.get_keyring()
    except Exception as error:
        raise AuthError(
            "storage_unavailable",
            "The system keyring is unavailable. Unlock or configure it, then retry.",
        ) from error


def _read_token() -> Credentials | None:
    backend = _secure_backend()
    try:
        serialized = backend.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
    except Exception as error:
        raise AuthError("storage_unavailable", "Could not read credentials from the system keyring.") from error
    if serialized is None:
        return None
    try:
        credential_data = json.loads(serialized)
        if not isinstance(credential_data, dict):
            raise ValueError("credential data must be an object")
        return Credentials.from_authorized_user_info(credential_data)
    except Exception as error:
        raise AuthError(
            "reauthorization_required",
            "Stored credentials are invalid. Run `auth setup` to authorize again.",
        ) from error


def _write_token(credentials: Credentials) -> None:
    backend = _secure_backend()
    try:
        serialized = credentials.to_json()
        backend.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, serialized)
        # Verify the backend retained the exact serialized credential value.
        if backend.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT) != serialized:
            raise RuntimeError("keyring did not retain the stored value")
    except Exception as error:
        raise AuthError(
            "storage_unavailable",
            "Credentials could not be safely persisted in the system keyring.",
        ) from error


def setup(client_secrets: str, *, modify: bool = False) -> dict[str, str]:
    """Request readonly access by default; modify access requires explicit opt-in."""
    scopes = (MODIFY_SCOPE,) if modify else SCOPES
    path = Path(client_secrets).expanduser()
    try:
        if not path.is_file():
            raise AuthError("invalid_input", "The Desktop OAuth client file was not found.")
        flow = InstalledAppFlow.from_client_secrets_file(str(path), scopes=scopes)
        credentials = flow.run_local_server(port=0, open_browser=True, **({"prompt": "consent"} if modify else {}))
    except AuthError:
        raise
    except Exception as error:
        # Library exceptions may contain client details or authorization data.
        raise AuthError(
            "oauth_cancelled",
            "Authorization did not complete. Retry from a local browser session.",
        ) from error
    granted_scopes = credentials.granted_scopes
    effective_scopes = credentials.scopes if granted_scopes is None else granted_scopes
    if not set(scopes).issubset(set(effective_scopes or ())):
        raise AuthError("insufficient_scope", "Google did not grant the requested Gmail permission.")
    _write_token(credentials)
    return {"status": "authenticated", "scope": scopes[0]}


def status() -> dict[str, str]:
    """Report stored authentication state without returning credential values."""
    credentials = _read_token()
    if credentials is None:
        return {"status": "not_configured"}
    scopes = set(credentials.scopes or ())
    if MODIFY_SCOPE not in scopes and not set(SCOPES).issubset(scopes):
        return {"status": "reauthorization_required", "reason": "insufficient_scope"}
    if not credentials.valid:
        return {"status": "reauthorization_required", "reason": "credentials_expired_or_invalid"}
    return {"status": "authenticated", "scope": MODIFY_SCOPE if MODIFY_SCOPE in scopes else SCOPES[0]}


def revoke() -> dict[str, str]:
    """Delete local credentials only; this does not revoke Google's grant."""
    backend = _secure_backend()
    try:
        stored = backend.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
        if stored is not None:
            backend.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
    except Exception as error:
        raise AuthError("storage_unavailable", "Could not remove credentials from the system keyring.") from error
    return {"status": "removed_locally", "google_grant": "not_revoked"}


def credentials_for_use(*, modify: bool = False) -> Credentials:
    """Load approved credentials; readonly credentials cannot authorize mutations."""
    credentials = _read_token()
    if credentials is None:
        raise AuthError("not_configured", "Run `auth setup` before using Gmail.")
    scopes = set(credentials.scopes or ())
    if modify and MODIFY_SCOPE not in scopes:
        raise AuthError("insufficient_scope", "Explicitly authorize Gmail modify access with `auth setup --modify` first.")
    if not modify and MODIFY_SCOPE not in scopes and not set(SCOPES).issubset(scopes):
        raise AuthError("insufficient_scope", "Run `auth setup` again to grant Gmail readonly access.")
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except GoogleAuthError as error:
            raise AuthError(
                "reauthorization_required",
                "Google rejected the saved authorization. Run `auth setup` again.",
            ) from error
        granted_scopes = credentials.granted_scopes
        effective_scopes = set((credentials.scopes if granted_scopes is None else granted_scopes) or ())
        required = {MODIFY_SCOPE} if modify or MODIFY_SCOPE in scopes else set(SCOPES)
        if not required.issubset(effective_scopes):
            raise AuthError("insufficient_scope", "Refreshed authorization lacks the required Gmail permission.")
        _write_token(credentials)
    if not credentials.valid:
        raise AuthError("reauthorization_required", "Run `auth setup` again to authorize Gmail.")
    return credentials
