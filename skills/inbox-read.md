# Reading Inbox and Sent Mail

Use Outlook MCP actions for mailbox reads.

## Preferred Outlook MCP actions

- Use `outlook.list_messages` or the closest Outlook MCP mail-list action exposed by the managed server.
- Use `outlook.get_message` or the closest message-read action for full bodies and thread details.
- Filter by `receivedDateTime` for inbox reads.
- Filter by `sentDateTime` for sent-mail reads when building briefings or rule suggestions.
- Request only needed fields: id, from, toRecipients, ccRecipients, subject, bodyPreview, receivedDateTime, importance, isRead, categories, conversationId, and hasAttachments.

## Inbox filter examples

- Last 5 minutes: `receivedDateTime ge <lastCheckpoint>` and `isRead eq false`.
- Last 24 hours: `receivedDateTime ge <now-minus-24h>`.
- Last 7 days: `receivedDateTime ge <now-minus-7d>`.

## Reading bodies

- Prefer previews for classification when enough.
- Fetch full bodies only for messages that need reply drafts, incident summaries, or VIP context.
- Preserve conversation id so the reply can stay in thread.
- Do not include full sensitive bodies in Teams unless the rule explicitly requires it.

## Sent mail for grounding

- Pull sent messages in the same period to identify reply patterns.
- Match by conversation id when possible.
- Cite only real sent-message subjects and dates; never fabricate grounding.

## Missing data behavior

If an MCP action is unavailable or authorization is missing, state that sent mail, calendar, and server-side thread context are unavailable rather than inventing data.
