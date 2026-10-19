#!/usr/bin/env python3
"""Command-line entry point for Google Workspace Gmail authentication and label operations."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

import auth
import gmail_api


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Set up and inspect local Gmail API authentication."
    )
    commands = parser.add_subparsers(dest="service", required=True)
    auth_parser = commands.add_parser("auth", help="Manage Gmail authentication")
    auth_commands = auth_parser.add_subparsers(dest="auth_command", required=True)

    setup_parser = auth_commands.add_parser("setup", help="Authorize Gmail access")
    setup_parser.add_argument(
        "--client-secrets", required=True, help="Path to a Desktop OAuth client JSON file"
    )
    setup_parser.add_argument("--modify", action="store_true", help="Explicitly consent to broad Gmail modify access for label changes")
    auth_commands.add_parser("status", help="Show local authentication status")
    auth_commands.add_parser("revoke", help="Remove locally stored authentication")
    gmail_parser = commands.add_parser("gmail", help="Read Gmail and manage explicitly confirmed labels")
    gmail_commands = gmail_parser.add_subparsers(dest="gmail_command", required=True)
    search_parser = gmail_commands.add_parser("search", help="Search using Gmail query syntax")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--limit", type=int, default=20)
    get_parser = gmail_commands.add_parser("get", help="Read a message by ID")
    get_parser.add_argument("--message-id", required=True)
    labels_parser = gmail_commands.add_parser("labels", help="Inspect labels")
    labels_commands = labels_parser.add_subparsers(dest="labels_command", required=True)
    labels_commands.add_parser("list", help="List labels")
    for action in ("apply", "remove"):
        label_parser = labels_commands.add_parser(action, help=f"{action.capitalize()} one label on one confirmed message")
        label_parser.add_argument("--message-id", required=True)
        label_parser.add_argument("--label-id", required=True)
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    parsed = parser.parse_args(arguments)
    try:
        if parsed.service == "gmail":
            if parsed.gmail_command == "search":
                result = gmail_api.search(parsed.query, parsed.limit)
            elif parsed.gmail_command == "get":
                result = gmail_api.get_message(parsed.message_id)
            elif parsed.labels_command == "list":
                result = gmail_api.list_labels()
            else:
                result = gmail_api.change_label(parsed.message_id, parsed.label_id, parsed.labels_command)
        elif parsed.auth_command == "setup":
            result = auth.setup(parsed.client_secrets, modify=True) if parsed.modify else auth.setup(parsed.client_secrets)
        elif parsed.auth_command == "status":
            result = auth.status()
        else:
            result = auth.revoke()
        print(json.dumps(result, sort_keys=True))
        return 0
    except (auth.AuthError, gmail_api.GmailError) as error:
        print(json.dumps({"error": error.code, "message": str(error)}, sort_keys=True), file=sys.stderr)
        return 1
    except Exception:
        print(json.dumps({"error": "internal_error", "message": "The operation failed unexpectedly."}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
