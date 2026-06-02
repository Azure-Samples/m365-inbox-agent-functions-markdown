# Safe Email Reply Pattern

Use Outlook MCP actions to send or reply.

## Before replying

- Confirm the message expects a response.
- Check `conversationId` and sent mail so you do not reply twice.
- Apply `vip-rules.md` first; rule actions must lead the plan.
- Include only facts present in the message, thread, or trusted context.
- If confidence is low, send a briefing to the user instead of replying to the sender.

## Reply content

- Keep the subject threaded as `Re: <original subject>` unless sending a digest.
- Be concise, specific, and helpful.
- Avoid commitments about dates, pricing, roadmap, legal terms, security posture, or incident status unless source content explicitly supports them.
- Include a next step when useful.
- Do not expose internal reasoning or rule names to external recipients.

## Execution order

1. Send a threaded response with the Outlook MCP reply action, typically `outlook.reply_mail`.
2. For digests or new messages, use the Outlook MCP send action, typically `outlook.send_mail`.
3. After a successful send, mark the original message read with the Outlook MCP update action, typically `outlook.update_message`.
4. Log the action in the run summary.

## Never do this

- Never reply twice in the same conversation.
- Never reply to spam-like or phishing-like messages.
- Never send full inbox summaries to the original sender.
- Never mark read before the reply succeeds.
