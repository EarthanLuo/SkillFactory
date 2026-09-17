# Memory Index

| ID | Type | Title | Related |
|---|---|---|---|
| [SRC-20260916-001](sources/SRC-20260916-001.md) | source | Table Skills GitHub repository | — |
| [EXT-20260916-001](extractions/EXT-20260916-001.md) | extraction | Long-task handoff as verified state transfer | SRC-20260916-001 |
| [DSC-20260916-001](discussions/DSC-20260916-001.md) | discussion | Invalid draft retained for traceability; no user decision | EXT-20260916-001, FB-20260916-001 |
| [DSC-20260916-002](discussions/DSC-20260916-002.md) | discussion | Adapt verified handoff as a manual-first workflow | EXT-20260916-001, SRC-20260916-001 |
| [FB-20260916-001](feedback/FB-20260916-001.md) | feedback | Extraction ended without real user discussion | EXT-20260916-001, DSC-20260916-001 |
| [EVO-20260916-001](evolution/EVO-20260916-001.md) | evolution | Require a conversational handoff after extraction | FB-20260916-001, DSC-20260916-001 |
| [FB-20260917-001](feedback/FB-20260917-001.md) | feedback | Model-scoped token result was generalized | SRC-20260916-001, EXT-20260916-001 |
| [FB-20260917-002](feedback/FB-20260917-002.md) | feedback | Existing ChatGPT chat delegation worked but waiting and recovery need adaptation | chat-research-stand-in, DSC-20260917-003 |
| [FB-20260917-003](feedback/FB-20260917-003.md) | feedback | Treat the GPT chat as a research subagent to protect the Codex main context | chat-research-stand-in, FB-20260917-002 |
| [FB-20260917-004](feedback/FB-20260917-004.md) | feedback | Content polling replayed old answers into the coordinating context | chat-research-stand-in, EVO-20260917-003 |
| [FB-20260917-005](feedback/FB-20260917-005.md) | feedback | Deterministic pre-model filtering can reduce stand-in context cost | chat-research-stand-in, FB-20260917-004 |
| [FB-20260917-006](feedback/FB-20260917-006.md) | feedback | Pre-model filtering worked but desktop agentMessage extraction missed | chat-research-stand-in, EVO-20260917-005 |
| [FB-20260917-007](feedback/FB-20260917-007.md) | feedback | Receive over-budget answers once instead of forcing recompression | chat-research-stand-in, FB-20260917-006 |
| [FB-20260917-008](feedback/FB-20260917-008.md) | feedback | Single-turn recovery works but internal citation placeholders remain | chat-research-stand-in, EVO-20260917-006 |
| [FB-20260917-009](feedback/FB-20260917-009.md) | feedback | Pre-exposure citation cleanup succeeds in a single-turn recovery | chat-research-stand-in, EVO-20260917-007 |
| [FB-20260917-010](feedback/FB-20260917-010.md) | feedback | Main-task status polling should move into one bounded host call | chat-research-stand-in, FB-20260917-009 |
| [FB-20260917-011](feedback/FB-20260917-011.md) | feedback | Guide the user to create and return a desktop ChatGPT chat | chat-research-stand-in, EVO-20260917-008 |
| [FB-20260917-012](feedback/FB-20260917-012.md) | feedback | The web-task name no longer matches chat-based research delegation | chat-research-stand-in, EVO-20260917-009 |
| [DSC-20260917-001](discussions/DSC-20260917-001.md) | discussion | Preserve web-proxy design value without generalizing Astar results | SRC-20260916-001, EXT-20260916-001, FB-20260917-001 |
| [DSC-20260917-002](discussions/DSC-20260917-002.md) | discussion | Test a verifiable web task stand-in without Astra | SRC-20260916-001, EXT-20260916-001, DSC-20260917-001 |
| [DSC-20260917-003](discussions/DSC-20260917-003.md) | discussion | Route web stand-in work through desktop quick chats or existing chats | EXT-20260916-001, DSC-20260917-002 |
| [EVO-20260917-001](evolution/EVO-20260917-001.md) | evolution | Preserve empirical claim scope during extraction | FB-20260917-001, DSC-20260917-001 |
| [EVO-20260917-002](evolution/EVO-20260917-002.md) | evolution | Add deterministic task packaging and result cleaning helpers | FB-20260917-002, DSC-20260917-003 |
| [EVO-20260917-003](evolution/EVO-20260917-003.md) | evolution | Delegate bounded research autonomy and recover only decision packages | FB-20260917-003, FB-20260917-002 |
| [EVO-20260917-004](evolution/EVO-20260917-004.md) | evolution | Separate status waiting from one-shot bounded result recovery | FB-20260917-004, EVO-20260917-003 |
| [EVO-20260917-005](evolution/EVO-20260917-005.md) | evolution | Add pre-model probing, extraction, budgeting, and audit helpers | FB-20260917-005, FB-20260917-004 |
| [EVO-20260917-006](evolution/EVO-20260917-006.md) | evolution | Make receive budgeting advisory and harden desktop message extraction | FB-20260917-006, FB-20260917-007 |
| [EVO-20260917-007](evolution/EVO-20260917-007.md) | evolution | Remove internal citation placeholders before main-context exposure | FB-20260917-008 |
| [EVO-20260917-008](evolution/EVO-20260917-008.md) | evolution | Move status polling into a bounded host-side waiter | FB-20260917-010 |
| [EVO-20260917-009](evolution/EVO-20260917-009.md) | evolution | Add a manual bootstrap for a user-created ChatGPT chat | FB-20260917-011 |
| [EVO-20260917-010](evolution/EVO-20260917-010.md) | evolution | Rename web-task-stand-in to chat-research-stand-in | FB-20260917-012 |
