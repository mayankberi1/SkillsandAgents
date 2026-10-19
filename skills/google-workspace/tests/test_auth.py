"""Offline tests for Gmail OAuth state and its command-line boundary."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from google.oauth2.credentials import Credentials

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIRECTORY))

import auth  # noqa: E402
import gmail  # noqa: E402


class Keyring:
    """Small in-memory backend selected by the test environment."""

    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, account: str) -> str | None:
        return self.values.get((service, account))

    def set_password(self, service: str, account: str, value: str) -> None:
        self.values[(service, account)] = value

    def delete_password(self, service: str, account: str) -> None:
        del self.values[(service, account)]


@pytest.fixture
def memory_keyring(monkeypatch: pytest.MonkeyPatch) -> Keyring:
    backend = Keyring()
    monkeypatch.setattr(auth.keyring, "get_keyring", lambda: backend)
    return backend


def credential(*, token: str = "test-token", valid: bool = True) -> Credentials:
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    if not valid:
        expiry = datetime.now(timezone.utc) - timedelta(hours=1)
    return Credentials(
        token=token,
        refresh_token="test-refresh-token",
        token_uri="https://oauth2.googleapis.com/token",
        client_id="test-client-id",
        client_secret="test-client-secret",
        scopes=auth.SCOPES,
        expiry=expiry,
    )


def store_credential(backend: Keyring, credentials: Credentials) -> None:
    backend.set_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT, credentials.to_json())


def test_status_uses_backend_selected_by_keyring(memory_keyring: Keyring) -> None:
    store_credential(memory_keyring, credential())

    assert auth.status()["status"] == "authenticated"


@pytest.mark.parametrize("operation", ["get_password", "set_password"])
def test_keyring_operation_failures_are_storage_unavailable(
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
) -> None:
    class FailingKeyring:
        def get_password(self, service: str, account: str) -> str | None:
            if operation == "get_password":
                raise RuntimeError("backend failure")
            return None

        def set_password(self, service: str, account: str, value: str) -> None:
            raise RuntimeError("backend failure")

        def delete_password(self, service: str, account: str) -> None:
            raise RuntimeError("backend failure")

    monkeypatch.setattr(auth.keyring, "get_keyring", lambda: FailingKeyring())

    with pytest.raises(auth.AuthError) as error:
        if operation == "get_password":
            auth.status()
        else:
            auth._write_token(credential())

    assert error.value.code == "storage_unavailable"


def test_keyring_discovery_failure_is_storage_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_discovery() -> None:
        raise RuntimeError("backend discovery failure")

    monkeypatch.setattr(auth.keyring, "get_keyring", fail_discovery)

    with pytest.raises(auth.AuthError) as error:
        auth.status()

    assert error.value.code == "storage_unavailable"


def test_status_does_not_expose_credential_values(memory_keyring: Keyring) -> None:
    store_credential(memory_keyring, credential())

    result = auth.status()

    assert result == {"status": "authenticated", "scope": auth.SCOPES[0]}
    assert "test-token" not in json.dumps(result)
    assert "test-client-secret" not in json.dumps(result)


def test_status_reports_explicit_modify_scope(memory_keyring: Keyring) -> None:
    insufficient = Credentials(
        token="test-token",
        refresh_token="test-refresh-token",
        token_uri="https://oauth2.googleapis.com/token",
        client_id="test-client-id",
        client_secret="test-client-secret",
        scopes=("https://www.googleapis.com/auth/gmail.modify",),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    store_credential(memory_keyring, insufficient)

    assert auth.status() == {"status": "authenticated", "scope": auth.MODIFY_SCOPE}
    assert auth.credentials_for_use().valid
    assert auth.credentials_for_use(modify=True).valid


def test_setup_requests_readonly_and_persists_to_keyring(
    memory_keyring: Keyring,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    client_file = tmp_path / "desktop-client.json"
    client_file.write_text("{}", encoding="utf-8")
    captured: dict[str, object] = {}

    class FakeFlow:
        def run_local_server(self, *, port: int, open_browser: bool) -> Credentials:
            captured["port"] = port
            captured["open_browser"] = open_browser
            return credential()

    def make_flow(path: str, *, scopes: tuple[str, ...]) -> FakeFlow:
        captured["path"] = path
        captured["scopes"] = scopes
        return FakeFlow()

    monkeypatch.setattr(auth.InstalledAppFlow, "from_client_secrets_file", make_flow)

    result = auth.setup(str(client_file))

    assert result["status"] == "authenticated"
    assert captured["scopes"] == auth.SCOPES
    assert captured["port"] == 0
    assert captured["open_browser"] is True
    saved = memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT)
    assert saved is not None
    assert json.loads(saved)["refresh_token"] == "test-refresh-token"


def test_setup_wraps_oauth_failure_without_leaking_exception(
    memory_keyring: Keyring,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    client_file = tmp_path / "desktop-client.json"
    client_file.write_text("{}", encoding="utf-8")

    class FakeFlow:
        def run_local_server(self, **kwargs: object) -> None:
            raise RuntimeError("sensitive oauth response")

    monkeypatch.setattr(
        auth.InstalledAppFlow,
        "from_client_secrets_file",
        lambda *args, **kwargs: FakeFlow(),
    )

    with pytest.raises(auth.AuthError) as error:
        auth.setup(str(client_file))

    assert error.value.code == "oauth_cancelled"
    assert "sensitive oauth response" not in str(error.value)


def test_revoke_removes_local_token_without_claiming_google_revocation(
    memory_keyring: Keyring,
) -> None:
    store_credential(memory_keyring, credential())

    result = auth.revoke()

    assert result == {"status": "removed_locally", "google_grant": "not_revoked"}
    assert memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT) is None


def test_delete_failure_is_storage_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailingDeleteKeyring(Keyring):
        def get_password(self, service: str, account: str) -> str | None:
            return "stored credential"

        def delete_password(self, service: str, account: str) -> None:
            raise RuntimeError("backend failure")

    monkeypatch.setattr(auth.keyring, "get_keyring", FailingDeleteKeyring)

    with pytest.raises(auth.AuthError) as error:
        auth.revoke()

    assert error.value.code == "storage_unavailable"


def test_refresh_failure_requires_reauthorization(
    memory_keyring: Keyring,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expired = credential(valid=False)
    store_credential(memory_keyring, expired)

    def fail_refresh(credentials: Credentials, request: object) -> None:
        raise auth.GoogleAuthError("sensitive refresh response")

    monkeypatch.setattr(Credentials, "refresh", fail_refresh)

    with pytest.raises(auth.AuthError) as error:
        auth.credentials_for_use()

    assert error.value.code == "reauthorization_required"
    assert "sensitive refresh response" not in str(error.value)


def test_cli_returns_structured_safe_auth_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fail_status() -> dict[str, str]:
        raise auth.AuthError("storage_unavailable", "safe message")

    monkeypatch.setattr(auth, "status", fail_status)

    exit_code = gmail.main(["auth", "status"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert json.loads(captured.err) == {
        "error": "storage_unavailable",
        "message": "safe message",
    }


def test_cli_reports_success_as_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(auth, "status", lambda: {"status": "not_configured"})

    exit_code = gmail.main(["auth", "status"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert json.loads(captured.out) == {"status": "not_configured"}


def test_readonly_cannot_mutate_or_trigger_consent(memory_keyring, monkeypatch):
    store_credential(memory_keyring, credential())
    monkeypatch.setattr(auth.InstalledAppFlow, "from_client_secrets_file", lambda *a, **k: pytest.fail("implicit consent"))
    with pytest.raises(auth.AuthError) as error:
        auth.credentials_for_use(modify=True)
    assert error.value.code == "insufficient_scope"


@pytest.mark.parametrize("outcome", ["modify", "readonly", "empty_grant", "cancel"])
def test_explicit_modify_setup_validates_before_replacing_token(memory_keyring, monkeypatch, tmp_path, outcome):
    original = credential()
    store_credential(memory_keyring, original)
    previous = memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT)
    client = tmp_path / "desktop.json"
    client.write_text("{}")
    captured = {}
    updated = credential(token="new-token")
    if outcome == "modify":
        updated = Credentials(token="new-token", refresh_token="refresh", token_uri="https://oauth2.googleapis.com/token",
                              client_id="client", client_secret="secret", scopes=(auth.MODIFY_SCOPE,),
                              expiry=datetime.now(timezone.utc) + timedelta(hours=1))
    if outcome == "empty_grant":
        updated._granted_scopes = []
    class Flow:
        def run_local_server(self, **kwargs):
            captured.update(kwargs)
            if outcome == "cancel":
                raise RuntimeError("private consent error")
            return updated
    def flow(path, *, scopes):
        assert scopes == (auth.MODIFY_SCOPE,)
        return Flow()
    monkeypatch.setattr(auth.InstalledAppFlow, "from_client_secrets_file", flow)
    if outcome == "modify":
        assert auth.setup(str(client), modify=True)["scope"] == auth.MODIFY_SCOPE
        assert auth.status()["scope"] == auth.MODIFY_SCOPE
    else:
        with pytest.raises(auth.AuthError) as error:
            auth.setup(str(client), modify=True)
        assert error.value.code == ("oauth_cancelled" if outcome == "cancel" else "insufficient_scope")
        assert memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT) == previous
    assert captured["prompt"] == "consent"


def test_successful_modify_refresh_is_persisted(memory_keyring, monkeypatch):
    expired = credential(valid=False)
    expired._scopes = (auth.MODIFY_SCOPE,)
    store_credential(memory_keyring, expired)
    def refresh(credentials, request):
        credentials.token = "refreshed-token"
        credentials.expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None)
    monkeypatch.setattr(Credentials, "refresh", refresh)
    assert auth.credentials_for_use(modify=True).token == "refreshed-token"
    stored = json.loads(memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT))
    assert stored["token"] == "refreshed-token"
    assert stored["scopes"] == [auth.MODIFY_SCOPE]


@pytest.mark.parametrize("modify", [False, True])
def test_granted_scope_downgrade_is_not_saved(memory_keyring, monkeypatch, modify):
    expired = credential(valid=False)
    expired._scopes = (auth.MODIFY_SCOPE,)
    store_credential(memory_keyring, expired)
    original = memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT)
    def refresh(credentials, request):
        credentials._granted_scopes = auth.SCOPES
        credentials.expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None)
    monkeypatch.setattr(Credentials, "refresh", refresh)
    with pytest.raises(auth.AuthError) as error:
        auth.credentials_for_use(modify=modify)
    assert error.value.code == "insufficient_scope"
    assert memory_keyring.get_password(auth.KEYRING_SERVICE, auth.KEYRING_ACCOUNT) == original


def test_cli_explicit_modify_dispatch(monkeypatch, capsys):
    captured = {}
    def setup(path, *, modify):
        captured.update(path=path, modify=modify)
        return {"status": "authenticated"}
    monkeypatch.setattr(auth, "setup", setup)
    assert gmail.main(["auth", "setup", "--client-secrets", "desktop.json", "--modify"]) == 0
    assert captured == {"path": "desktop.json", "modify": True}
    assert json.loads(capsys.readouterr().out)["status"] == "authenticated"
