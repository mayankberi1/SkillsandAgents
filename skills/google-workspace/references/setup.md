# Setup and access limits

## One path for every chat

Use the installed skill copy and the same desktop OS user. Resolve `SKILL_DIR`
from the installed SKILL.md. Run the commands with `uv run --offline`; use
`uv run` when package-network access is enabled and a required package is not
cached. Do not use `python` or `python3` to run the script. Prepare the uv
cache in a network-enabled session before offline use. If the default cache is
not writable, set `UV_CACHE_DIR` to a writable workspace path:

```sh
uv run --offline "$SKILL_DIR/scripts/gmail.py" auth status
uv run --offline "$SKILL_DIR/scripts/gmail.py" auth setup --client-secrets <external-client-json>
```

Status comes first. Skip new setup when it reports authenticated. If it reports
`storage_unavailable`, do not assume credentials are missing and do not repeat
setup. Run status in the same OS user's active desktop session, or use an
approved execution context with access to that user's keyring. On Ubuntu, the
keyring usually uses Secret Service over the user's D-Bus session; a restricted
sandbox can block this access. Ask the user to unlock or start the desktop
keyring if needed. Never switch to a file or plaintext backend.

The status command does not open consent, read Gmail, or print credential
values. `authenticated` confirms that it read a usable saved credential. A
temporary Google network failure does not mean the grant is missing. Setup is
needed only for new authorization or when status reports an authorization
problem after it can read the keyring. The CLI does not have an `auth check`
command.

The entry point reads Python and exact package pins from its PEP 723 block.
`uv` creates and uses the script environment from that metadata. Keep the uv
cache readable and writable in the execution environment. It contains packages,
never credentials. Use the same installed skill, OS user and keyring in later
chats; a copied skill does not copy authorization. The keyring package is not
itself an unlocked keyring.

## Access needed at each stage

| Stage | Required access | If Codex blocks it |
|---|---|---|
| Package setup | Read/write uv cache; DNS/HTTPS to `pypi.org` and downloads at `files.pythonhosted.org` when packages are not cached | Prepare the uv cache in a network-enabled session. If package access is denied/unavailable, use an approved local session. |
| Google access | DNS/HTTPS to `accounts.google.com`, `oauth2.googleapis.com`, and `gmail.googleapis.com` | Request those destinations through available controls, or use an approved local session. Keep saved credentials during temporary failures. |
| Browser sign-in | Open the user's system browser | Allow local browser access if available, or run sign-in in the user's local desktop session. The user must complete Google's consent. |
| Browser return | Bind/connect to `127.0.0.1` and let that browser reach the listener | Allow local loopback access if available, or run browser and script on the same local machine. A cloud container's localhost is not the user's desktop. |
| Keyring | Discover/unlock the same user's native keyring and read/write/delete entries | Unlock the login keyring in the desktop session and allow local credential-store/session-bus access if available. Never use a plaintext fallback. |

These are separate permissions. Neither SKILL.md nor the script can grant them.
An approval in one Codex chat does not prove another chat has the same access.
Do not bypass denied actions or change managed policies. Explain the exact
blocked step and the next user/system action. A browser-launch check cannot
prove consent will finish; the loopback probe checks this process's local
connection, not the browser's access. A valid browser return must still arrive.

Linux native keyrings commonly need Secret Service and the desktop session bus;
KWallet may also require OS-provided D-Bus support. macOS uses Keychain and
Windows uses Credential Locker. File/plaintext, null and unsupported custom
backends are rejected. If keyring selects a chain, its first write backend must
be a supported native backend; configure an explicit native backend otherwise.
The skill never changes backend configuration. OAuth uses service
`google-workspace-gmail`, account `default`; access probes use a separate service.
On Ubuntu, the user can view entries with the **Passwords and Keys** app. Do
not ask the user to reveal or paste a token value. To verify access, prefer the
skill's `auth status` command; it reports status without exposing credentials.

## Google console and consent

Official references checked 16 November 2026:
[Google Gmail Python quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python),
[Desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app),
[keyring platform requirements](https://keyring.readthedocs.io/en/latest/).

1. Enable the Gmail API in the user's Google Cloud project.
2. Configure Google Auth platform Branding, Audience and Data Access. For an
   External app in Testing, add the Gmail account as a test user. Register
   `gmail.readonly` for ordinary reading; Workspace policy can restrict access.
3. Create an OAuth client of type Desktop app. The user keeps the downloaded
   client JSON outside the skill/repository and supplies its path. The skill
   only reads this existing file; it never writes or copies client secrets.
4. Run setup after the checks pass. It uses Google's library, PKCE and a
   random local port bound only to `127.0.0.1`. The browser receives the sign-in
   URL directly; the script does not print it. The user completes readonly
   consent. Only request `--modify` for an explicit user request for broader
   access, under the confirmation rules in SKILL.md.
5. The return must have matching state and one authorization code. Consent has
   a 180-second return timeout. The local listener closes on success/failure;
   authorization codes and return URLs are not logged. A valid grant with a
   refresh token must pass scope checks before it replaces saved credentials.

Tokens and refresh tokens remain in the native OS keyring. No credential values
are emitted to stdout/stderr, environment variables or files. Do not enable
HTTP/OAuth debug logging or paste raw exceptions, client JSON or keyring values
into chat. Keep package diagnostics separate from authentication. Local revoke
removes the keyring entry only; use Google Account security settings to revoke
the Google-side grant. External apps in Testing can have seven-day refresh-token
expiry; see [Google token expiry](https://developers.google.com/identity/protocols/oauth2#expiration).

## Errors and next steps

| Error | Next step |
|---|---|
| `python_version` | Select Python 3.12+. |
| `dependency_setup_failed` | Check venv/ensurepip support, cache write access, declared package versions and pip settings. |
| `missing_packages` | Run the entry point directly in the dedicated environment; check for an incomplete installation. |
| `dns_unavailable` / `network_unavailable` | Restore the reported service's DNS/network access in this session, then retry. |
| `network_denied` | Request access using available Codex controls; if it cannot be granted, use an approved local session. |
| `tls_error` | Fix trusted certificates/proxy configuration. Never disable TLS checks. |
| `service_unavailable` | Retry later; keep saved credentials. |
| `storage_unavailable` | Retry status/setup in the same OS user's desktop session or another approved context with keyring access. Do not assume credentials are missing or repeat setup until access works. |
| `browser_unavailable` | Enable local browser access or sign in from an approved local desktop session. |
| `loopback_unavailable` | Enable local bind/connect access or move browser and script to the same approved local session. |
| `callback_timeout` / `callback_invalid` | Complete consent within the timeout, check browser return access, then retry. |
| `invalid_client` | Supply a valid Google Desktop client file outside the skill. Google auth/token endpoints must be official HTTPS endpoints. |
| `authorization_rejected` | Check consent, client setup, test users and Google account/organization policy. |
| `authorization_failed` / `authorization_incomplete` | Retry sign-in in an approved local desktop session; no new credentials were saved. |
| `not_configured` / `reauthorization_required` | Complete Google setup/consent, once other access checks pass. |
| `insufficient_scope` | Use the requested scope; broader modify access needs explicit user approval first. |
