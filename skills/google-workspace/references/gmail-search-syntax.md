# Gmail search examples

Pass the query as one quoted argument to `gmail search --query`:

- `from:alice@example.com` — messages from a sender.
- `subject:invoice newer_than:30d` — recent invoice subjects.
- `is:unread in:inbox` — unread inbox messages.
- `has:attachment after:2026/01/01` — messages with attachments after a date.
- `label:Receipts` — messages carrying a label.

Queries are passed to Gmail unchanged. Search/get/list do not change read status
or labels. Search summaries include message IDs for the `gmail get` command.
