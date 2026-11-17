# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pytest==9.0.2",
# ]
# ///
"""Offline setup checks that do not need Google packages or a keyring."""

from __future__ import annotations

import builtins
import importlib.util
import re
import tomllib
import json
import os
import zipfile
from types import SimpleNamespace
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
spec = importlib.util.spec_from_file_location("gmail_setup_checks", SKILL / "scripts/gmail.py")
gmail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gmail)


def test_imported_main_reports_missing_package_without_installing(monkeypatch, capsys):
    original_import = builtins.__import__
    def missing(name, *args, **kwargs):
        if name == "auth":
            raise ModuleNotFoundError("auth dependency is missing")
        return original_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", missing)
    assert gmail.main(["auth", "status"]) == 1
    result = capsys.readouterr()
    error = json.loads(result.err)
    assert result.out == ""
    assert error["error"] == "missing_packages"
    assert "Run gmail.py directly" in error["message"]
    assert "Traceback" not in result.err


def test_old_python_fails_before_dependency_check(monkeypatch, capsys):
    monkeypatch.setattr(gmail.sys, "version_info", (3, 12))
    assert gmail.main(["auth", "status"]) == 1
    assert json.loads(capsys.readouterr().err)["error"] == "python_version"


@pytest.fixture
def installed_skill(tmp_path):
    target = tmp_path / "installed skill"
    shutil.copytree(SKILL, target, ignore=shutil.ignore_patterns("__pycache__", "tests"))
    return target




@pytest.mark.parametrize("arguments", [[], ["auth"], ["auth", "setup"], ["auth", "status"], ["auth", "revoke"], ["gmail"], ["gmail", "search"], ["gmail", "get"], ["gmail", "labels"], ["gmail", "labels", "apply"], ["gmail", "labels", "remove"]])
def test_help_works_without_dependencies(installed_skill, arguments):
    result = subprocess.run([sys.executable, "-S", str(installed_skill / "scripts/gmail.py"), *arguments, "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert result.stderr == ""


def script_metadata(path):
    blocks = re.findall(r"(?m)^# /// script\n((?:#(?: .*|)\n)+)# ///$", path.read_text())
    assert len(blocks) == 1, path
    return tomllib.loads("\n".join(line[2:] for line in blocks[0].splitlines()))


def test_all_scripts_and_tests_have_valid_inline_metadata():
    for path in [*SKILL.joinpath("scripts").glob("*.py"), *SKILL.joinpath("tests").glob("*.py")]:
        data = script_metadata(path)
        assert data["requires-python"] == ">=3.13"
        assert isinstance(data["dependencies"], list)
    assert not (SKILL / "requirements.txt").exists()


def test_entrypoint_covers_helper_dependencies_without_conflicting_pins():
    declared = set(script_metadata(SKILL / "scripts/gmail.py")["dependencies"])
    for name in ("auth.py", "gmail_api.py"):
        assert set(script_metadata(SKILL / "scripts" / name)["dependencies"]) <= declared


def test_import_does_not_start_installers(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("must not install at import time"))
    copy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(copy)


@pytest.fixture
def local_package_skill(installed_skill, tmp_path):
    """Use a real local wheel to test installation without Google or the network."""
    wheel_dir = tmp_path / "wheels"
    wheel_dir.mkdir()
    wheel = wheel_dir / "bootstrap_probe-1.0-py3-none-any.whl"
    info = "bootstrap_probe-1.0.dist-info/"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("bootstrap_probe.py", "VALUE = 'installed'\n")
        archive.writestr(info + "METADATA", "Metadata-Version: 2.1\nName: bootstrap-probe\nVersion: 1.0\n")
        archive.writestr(info + "WHEEL", "Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        archive.writestr(info + "RECORD", "")
    script = installed_skill / "scripts/gmail.py"
    text = script.read_text()
    text = re.sub(r"(?ms)^# dependencies = \[.*?^# ]", '# dependencies = ["bootstrap-probe==1.0"]', text, count=1)
    script.write_text(text)
    (installed_skill / "scripts/auth.py").write_text(
        "import bootstrap_probe, sys\n"
        "class AuthError(Exception): pass\n"
        "def status(): return {'status': bootstrap_probe.VALUE, 'python': sys.executable}\n"
    )
    (installed_skill / "scripts/gmail_api.py").write_text("class GmailError(Exception): pass\n")
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "cache"),
           "LOCALAPPDATA": str(tmp_path / "cache"), "PIP_NO_INDEX": "1",
           "PIP_FIND_LINKS": str(wheel_dir), "PIP_CONFIG_FILE": os.devnull}
    return script, wheel_dir, env


def test_direct_python_installs_inline_dependency_and_reuses_environment(local_package_skill, tmp_path):
    script, wheel_dir, env = local_package_skill
    # -S guarantees that the starting interpreter has no third-party packages.
    first = subprocess.run([sys.executable, "-S", str(script), "auth", "status"], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=45)
    assert first.returncode == 0, first.stderr
    first_status = json.loads(first.stdout)
    assert first_status["status"] == "installed"
    assert str(tmp_path / "cache") in first_status["python"]
    assert first_status["python"] != sys.executable
    shutil.rmtree(wheel_dir)
    # No wheel and no index: a second run must use the installed environment.
    second = subprocess.run([sys.executable, "-S", str(script), "auth", "status"], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=20)
    assert second.returncode == 0, second.stderr
    assert json.loads(second.stdout) == first_status
    assert "Traceback" not in first.stderr + second.stderr


@pytest.mark.parametrize("details,code", [
    ("Temporary failure in name resolution; private response", "network_unavailable"),
    ("No matching distribution found; private response", "dependency_setup_failed"),
])
def test_install_failure_is_safe_and_does_not_restart(monkeypatch, tmp_path, capsys, details, code):
    monkeypatch.setattr(gmail.checks, "network", lambda *a: None)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    def missing(name):
        raise gmail.PackageNotFoundError(name)
    monkeypatch.setattr(gmail, "version", missing)
    monkeypatch.setattr(gmail.venv.EnvBuilder, "create", lambda *a: None)
    calls = []
    def fail(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=1, stdout="", stderr=details)
    monkeypatch.setattr(gmail.subprocess, "run", fail)
    assert gmail._prepare_environment(["auth", "status"]) == 1
    assert len(calls) == 1
    assert calls[0][1:4] == ["-m", "pip", "install"]
    assert calls[0][-len(script_metadata(SKILL / "scripts/gmail.py")["dependencies"]):] == script_metadata(SKILL / "scripts/gmail.py")["dependencies"]
    output = capsys.readouterr()
    assert output.out == ""
    assert json.loads(output.err)["error"] == code
    assert "private" not in output.err


def test_venv_failure_is_safe(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    def missing(name):
        raise gmail.PackageNotFoundError(name)
    monkeypatch.setattr(gmail, "version", missing)
    def fail(*a):
        raise subprocess.CalledProcessError(1, "private ensurepip command")
    monkeypatch.setattr(gmail.venv.EnvBuilder, "create", fail)
    assert gmail._prepare_environment(["auth", "status"]) == 1
    output = capsys.readouterr()
    assert json.loads(output.err)["error"] == "dependency_setup_failed"
    assert "private" not in output.err


def test_matching_packages_do_not_install_or_restart(monkeypatch):
    pins = dict(item.split("==") for item in script_metadata(SKILL / "scripts/gmail.py")["dependencies"])
    monkeypatch.setattr(gmail, "version", pins.__getitem__)
    monkeypatch.setattr(gmail.sys, "prefix", "/prepared-env")
    monkeypatch.setattr(gmail.sys, "base_prefix", "/system-python")
    monkeypatch.setattr(gmail.subprocess, "run", lambda *a, **k: pytest.fail("unneeded installation"))
    assert gmail._prepare_environment(["auth", "status"]) is None


def test_direct_old_python_fails_before_loading_package_modules(installed_skill):
    script = str(installed_skill / "scripts/gmail.py")
    code = "import runpy,sys; sys.version_info=(3,10); sys.argv=[sys.argv[1], 'auth', 'status']; runpy.run_path(sys.argv[0], run_name='__main__')"
    result = subprocess.run([sys.executable, "-S", "-c", code, script], capture_output=True, text=True)
    assert result.returncode == 1
    assert result.stdout == ""
    assert json.loads(result.stderr)["error"] == "python_version"
