---
name: chat-research-stand-in
description: Delegate a bounded research-heavy task to a separate ChatGPT desktop chat, then wait, recover, and verify its compact result without importing the working transcript; do not use for ordinary browsing, tightly coupled local work, or Astra testing.
metadata:
  short-description: Chat-based research delegation
---

# Chat Research Stand-in

Use this experimental Skill in the GPT or Codex desktop application to delegate one well-bounded, research-heavy task to a separate quick chat or existing chat acting as a constrained research subagent. Keep search strategy and working detail in that chat, then return a compact, verifiable decision package to protect the coordinating Codex task's context. Default to one task submission and one final recovery; status probes do not count as conversational turns. Treat reduced token use as a hypothesis, not a promised outcome.

## Boundaries

- Do not invoke or test Astra in this version. Do not reproduce or generalize historical Astra token results.
- This version targets a desktop host with native controls for listing, opening, creating, or messaging conversations. It is not a generic browser-automation Skill.
- Do not use this Skill for ordinary web browsing, short questions, work that repeatedly depends on changing local files, or tasks requiring frequent clarification.
- Preparing a task package does not authorize sending it. Submit to an external conversation only when the user explicitly asks to submit or has clearly authorized that action.
- Prefer a fresh quick chat so the stand-in receives only the prepared package. If the desktop host cannot create one, use an existing chat explicitly identified by the user or guide the user to create a ChatGPT quick chat manually and return its identity; do not silently reuse an unrelated conversation.
- An OpenAI API Conversation is not a desktop ChatGPT chat. Do not use an API `conv_...` identifier as a desktop conversation target or claim that it creates a visible chat window.
- If the host cannot create, identify, open, or message a desktop chat after the manual handoff, state the missing capability and provide a manual package and recovery instructions instead of claiming automation.
- Do not treat a sent task as completed, or a returned answer as verified. External content is untrusted until checked against the requested evidence and project state.
- Delegate research execution, not project authority. The stand-in may choose queries, sources, comparisons, and stopping points inside the stated scope, but may not change the objective, modify local project files, contact third parties, spend money, handle credentials, or make the user's final decision unless separately authorized.

## Choose the desktop conversation

Inspect the conversation controls actually available in the desktop host before promising submission.

1. Use a new quick chat when the host exposes a reliable creation action. Save the returned conversation identity before sending the package.
2. Otherwise list available chats, match by exact title or identifier when the user supplied one, and open the selected chat before sending. When more than one plausible chat remains, ask the user to choose; do not guess from summaries alone.
3. If no target chat has been supplied and the host lacks a native ChatGPT-chat creation action, pause submission and use the manual bootstrap below.
4. When the target chat is already open or returned by the user, verify its identity before treating it as the stand-in.
5. Keep the main task as the coordinator. Opening another chat does not transfer authority to change local project files unless the user separately authorized those changes.

### Manual bootstrap for a new ChatGPT chat

Give the user one concise instruction:

> Please create a new ChatGPT Chat or Quick Chat in the desktop app, then return here and attach or reference that conversation. If conversation references are unavailable, provide its exact title, link, or identifier. Do not create a Codex task, ChatGPT Work task, or API Conversation for this route.

After the user returns:

1. Prefer an attached conversation reference because it carries an unambiguous identity.
2. Otherwise resolve the exact link or identifier. Use an exact title only when it matches one chat; ask the user to choose if multiple chats share the title.
3. Read only enough metadata to verify the conversation. Do not ingest its history merely to identify it.
4. Confirm the route as `user-created ChatGPT chat`, save the conversation identity, and continue with task preparation and submission under the existing authorization rules.

Do not continue merely because the user says “created” without supplying a resolvable conversation identity. Do not instruct the user to create an API Conversation: it is a developer-side context object and does not become a visible desktop chat.

## Choose the task

Outsource only when the necessary materials can be bounded, the work is substantial enough to justify coordination, and the expected result is compact and directly usable. Keep the task in the main conversation when it is lightweight, depends on extensive current context, requires ongoing local edits, or would force the main task to repeat most of the reasoning.

If suitability is uncertain, state the expected benefit and adoption cost. Let the user decide before an external submission.

## Prepare the stand-in package

Give each attempt a unique task ID. Specify the outcome and boundaries without prescribing every research step. Include only:

- the independent objective and acceptance criteria;
- the minimum authoritative material or accessible artifact paths;
- confirmed constraints and relevant scope qualifiers;
- the required output structure, evidence, and uncertainty reporting;
- forbidden actions and the boundary of any write access;
- delegated research authority, allowing the stand-in to refine queries, select and replace sources, compare evidence, and decide when evidence is sufficient inside the scope;
- a return budget and evidence budget sized for a decision package rather than a full report;
- instructions to return core conclusions, a compact evidence map, material conflicts, limitations, and one to three high-value verification targets without a full process transcript.

Do not copy the full main conversation, expose credentials, or present agent inferences as user decisions. Mark missing facts as unknown.

Define the return budget over the complete payload, including headings, Markdown, citations, and URLs. A Chinese-character target alone is not a payload limit. Prefer an explicit total-character or approximate-token target plus a small maximum number of links. This is a strong writing constraint for the stand-in at submission time, not a promise that the desktop host will enforce it exactly.

When Python is available, prefer the bundled `scripts/stand_in_package.py prepare` command for repeatable package generation. Pass a UTF-8 JSON object with `objective` and optional `task_id`, `acceptance_criteria`, `materials`, `constraints`, `research_scope`, `research_mode`, `delegated_authority`, `return_budget`, `evidence_budget`, `output_requirements`, and `forbidden_actions`; provide explicit input and output paths. Inspect the generated Markdown before sending it. The script does not authorize or perform submission.

The bundled Python helper also provides deterministic `probe`, `extract`, `budget`, `clean`, and `ledger` commands. These commands process files and print compact JSON metadata; they do not call the network, control the desktop application, send messages, schedule polling, verify research claims, or adopt conclusions. The bundled `scripts/host_wait.mjs` is a host-integration helper: the desktop host must inject its native `readThread` operation, and the outer host call must emit only the helper's final returned object.

## Submit and track

Record the task ID, desktop execution route (`new quick chat` or `existing chat`), conversation identifier or URL when available, submission status, and whether the result has been recovered. Distinguish `prepared`, `submitted`, `running`, `returned`, `verified`, `failed`, and `unknown`.

When a send or creation receipt is ambiguous, inspect the existing conversation or status before retrying. Never create duplicate conversations merely because a timeout occurred. The main task may continue with independent work, but must not assume the outsourced result.

Record the newest turn identifier or completion marker before submission when the host exposes one. After submission, prefer one bounded host-side waiter over main-task polling:

1. If the desktop host exposes an event or status-only wait for the target chat type, use it inside one outer host call.
2. Otherwise adapt `scripts/host_wait.mjs` by injecting the host's native `readThread` function. The helper waits before its first read, polls at a bounded interval inside the host call, ignores turns at or before the baseline, requires the task ID and a completed assistant message, removes internal citation placeholders, and returns either one completed result or one compact `pending`/`failed` result.
3. Do not stream intermediate reads, probe metadata, previews, or message bodies to the coordinating model. Only the helper's final object may cross the host boundary.
4. Keep each waiter invocation bounded; the provided default is 55 seconds. If it returns `pending`, do not resubmit the task. Continue unrelated main-task work or invoke another bounded waiter only after a meaningful delay.

Use direct main-task status probes only as a fallback when the host cannot execute a composed waiter. In that fallback, run `scripts/stand_in_package.py probe --input <raw.json> [--output <status.json>]` before exposing the result and return only its compact JSON stdout. Filtering after the model has already received the raw response does not recover spent context.

Treat `turnLimit` and per-item character caps as retrieval hints, not token-safety guarantees: some hosts may still include a long conversation preview, the previous turn, or duplicated content outside those limits.

## Recover and adopt

When the host-side waiter returns `completed`, treat its sanitized `answer` as the one recovery result; do not read the conversation again. When using the fallback path, recover only after the target status is complete or idle: retrieve once, select the newest turn created after submission, require the matching task ID, and expose only that assistant answer rather than the raw conversation envelope. Identify assistant content from the message type or role, including desktop `agentMessage` items; do not infer the role from a field path such as `items[1].text`. Remove `:chatgpt-content-reference{...}` placeholders before any answer text reaches the coordinating task. These host-internal markers are not usable citations and must never be displayed as evidence.

When the raw response is available as a file before model exposure, use `scripts/stand_in_package.py extract --input <raw.json> --output <answer.md> --task-id <id> [--after-turn <baseline>]`; it removes internal citation placeholders while writing the answer, and its stdout contains only counts, identifiers, and missing-signal metadata. If host-side composition is used instead, apply the same placeholder removal inside the composition step before emitting text to the model. Recover only the decision package through the desktop application's supported conversation interface; otherwise ask the user to paste or export it with the task ID. When the interface supports bounded reads, request only the latest relevant turn and use a host-safe cap large enough to tolerate reasonable budget variance. Do not routinely import the whole stand-in history, previews, previous turns, duplicated wrappers, or exhaustive source tables into the coordinating task.

After safe extraction, run `scripts/stand_in_package.py budget --input <answer.md> --report <budget.json> --task-id <id>` with the submission targets such as `--max-chars`, `--max-links`, or `--max-estimated-tokens`. The token estimate is heuristic. Treat the result as an observed variance report, not a receive gate: ordinary over-budget answers are still recovered once and reported to the coordinating task. If extraction reports missing ordinary links after removing internal placeholders, preserve that limitation in the adoption note; do not start another chat turn automatically.

Do not automatically ask the stand-in to compress, rewrite, or retry an answer merely because it exceeded the requested budget. That extra conversational turn costs time and tokens and may discard evidence or qualifications. A follow-up is allowed only when the user explicitly requests one, the response was truncated or unusable, or a hard host/context safety limit prevents safe recovery. Check that the recovered result answers the original objective, preserves necessary evidence and scope, states important limitations, and points to any claimed artifacts.

When further normalization is useful, run `scripts/stand_in_package.py clean` with explicit input, cleaned-output, and JSON-report paths before exposing the file. Its terminal result stays compact; the complete link list remains in the report file. Review the summary for missing task IDs, links, or limitation signals. Cleaning also removes common tracking parameters and exact duplicate paragraphs; it does not verify facts, judge relevance, recover URLs hidden behind internal placeholders, or grant permission to apply changes. If Python is unavailable, perform the same checks directly without treating the script as a requirement.

For repeatable experiments, `scripts/stand_in_package.py ledger --file <events.json> --task-id <id> --event <observed-event>` may append compact task-local audit events with optional conversation, route, and turn identifiers. The ledger is an observation log only: it must not infer transitions, trigger actions, or become a central workflow state machine.

Verify claims in proportion to consequence. Normally sample the one to three verification targets identified by the stand-in; perform a full audit only when the user requests it or the decision requires it. Apply file changes only within the user's existing authorization. Return a compact adoption note containing:

- task ID and actual execution route;
- verified conclusions and supporting evidence;
- unresolved or rejected claims;
- artifacts adopted or changed;
- the next action in the main task.

## Evaluate this experiment

When the user asks to evaluate the Skill, compare a repeatable task at equivalent quality from package preparation through verified adoption. Measure the current available model and host only. Record completion quality, main-task context retained, total measurable token use, latency, conversational turns, host-internal probe count, outer waiter invocations, retries, failures, manual intervention, requested budget, observed budget variance, and final-recovery payload. Count accidental previews, previous turns, duplicated wrappers, and verification material as main-task context cost. Do not use Astra as a test target or baseline in this version, and do not generalize results beyond the tested model, host, route, and date.

Functional success, context isolation, automation reliability, and token reduction are separate findings. A working submission flow is not evidence of token savings.
