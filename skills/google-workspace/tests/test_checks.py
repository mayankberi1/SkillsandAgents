# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest==9.0.2"]
# ///
"""No network calls: exercise credential-free connectivity failure categories."""

import socket
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import checks  # noqa: E402


@pytest.mark.parametrize("failure,code", [
    (URLError(socket.gaierror("private")), "dns_unavailable"),
    (URLError(ssl.SSLError("private")), "tls_error"),
    (PermissionError("private"), "network_unavailable"),
    (HTTPError("https://private", 403, "private", {}, None), "network_denied"),
    (HTTPError("https://private", 503, "private", {}, None), "service_unavailable"),
])
def test_network_errors_are_distinct_and_safe(monkeypatch, failure, code):
    def fail(request, *, timeout):
        assert timeout == 5
        assert request.get_method() == "HEAD"
        assert request.headers == {}
        raise failure
    monkeypatch.setattr(checks, "urlopen", fail)
    with pytest.raises(checks.SetupError) as error:
        checks.network("https://example.org", "example.org")
    assert error.value.code == code
    assert "private" not in str(error.value)


def test_token_endpoint_head_rejection_is_reachable(monkeypatch):
    def fail(*a, **k): raise HTTPError("https://example.org", 405, "method", {}, None)
    monkeypatch.setattr(checks, "urlopen", fail)
    checks.network("https://example.org", "example.org")
