/**
 * Bounded host-side waiter for a GPT/Codex desktop conversation.
 *
 * The desktop host must inject `readThread`; this module never calls the
 * network or a desktop API by itself. The caller must emit only the returned
 * object, never the intermediate read results.
 */

const CONTENT_REFERENCE_RE = /:chatgpt-content-reference\{[^{}]*\}/g;
const URL_RE = /https?:\/\/[^\s<>\]\[)]+/g;

function parsePayload(result) {
  if (result && typeof result === "object" && result.structuredContent) {
    return result.structuredContent;
  }
  if (result && Array.isArray(result.content)) {
    for (const item of result.content) {
      if (!item || item.type !== "text" || typeof item.text !== "string") continue;
      try {
        const parsed = JSON.parse(item.text);
        if (parsed && typeof parsed === "object") return parsed;
      } catch {
        // Ignore non-JSON text blocks; the host may include unrelated content.
      }
    }
  }
  if (result && typeof result === "object") return result;
  throw new Error("readThread returned no supported conversation payload");
}

function turnsFrom(payload) {
  if (Array.isArray(payload.turns)) return payload.turns;
  if (payload.thread && Array.isArray(payload.thread.turns)) return payload.thread.turns;
  return [];
}

function threadStatus(payload) {
  const status = payload.status || (payload.thread && payload.thread.status);
  return status && typeof status === "object" ? status.type : status || null;
}

function itemRole(item) {
  if (!item || typeof item !== "object") return null;
  if (["agentMessage", "assistantMessage"].includes(item.type)) return "assistant";
  if (["agent", "assistant"].includes(item.role)) return "assistant";
  if (item.type === "userMessage" || item.role === "user") return "user";
  return null;
}

function itemText(item) {
  if (typeof item.text === "string") return item.text;
  if (typeof item.content === "string") return item.content;
  if (Array.isArray(item.content)) {
    return item.content
      .filter((part) => part && typeof part.text === "string")
      .map((part) => part.text)
      .join("\n");
  }
  return "";
}

function turnText(turn, role) {
  return (Array.isArray(turn.items) ? turn.items : [])
    .filter((item) => itemRole(item) === role)
    .map(itemText)
    .filter(Boolean)
    .join("\n")
    .trim();
}

function sanitizeAnswer(raw) {
  const matches = raw.match(CONTENT_REFERENCE_RE) || [];
  const answer = raw
    .replace(CONTENT_REFERENCE_RE, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/ {2,}/g, " ")
    .trim();
  return { answer, placeholdersRemoved: matches.length };
}

function estimateTokens(value) {
  const cjk = (value.match(/[\u3400-\u9fff]/g) || []).length;
  const nonCjk = value.replace(/[\s\u3400-\u9fff]/g, "").length;
  return cjk + Math.ceil(nonCjk / 4);
}

function completedResult(turn, taskId, probes) {
  const raw = turnText(turn, "assistant");
  const { answer, placeholdersRemoved } = sanitizeAnswer(raw);
  const links = [...new Set(answer.match(URL_RE) || [])];
  return {
    status: "completed",
    task_id: taskId,
    turn_id: turn.id || turn.turnId || null,
    probes,
    characters: answer.length,
    estimated_tokens: estimateTokens(answer),
    estimate_is_heuristic: true,
    link_count: links.length,
    internal_placeholders_removed: placeholdersRemoved,
    missing_signals: links.length ? [] : ["links"],
    answer,
    raw_envelope_suppressed: true,
  };
}

export async function waitForStandIn({
  readThread,
  sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds)),
  now = () => Date.now(),
  threadId,
  baselineTurnId,
  taskId,
  timeoutMs = 55000,
  initialDelayMs = 10000,
  intervalMs = 10000,
  maxOutputCharsPerItem = 5000,
}) {
  if (typeof readThread !== "function") throw new TypeError("readThread must be a function");
  if (!threadId || !taskId) throw new TypeError("threadId and taskId are required");
  if (timeoutMs < 1000 || timeoutMs > 300000) throw new RangeError("timeoutMs must be 1000..300000");
  if (intervalMs < 1000) throw new RangeError("intervalMs must be at least 1000");

  const deadline = now() + timeoutMs;
  let probes = 0;
  let newestTurnId = baselineTurnId || null;

  if (initialDelayMs > 0) await sleep(Math.min(initialDelayMs, timeoutMs));

  while (now() <= deadline) {
    const rawResult = await readThread({
      threadId,
      turnLimit: 2,
      includeOutputs: false,
      maxOutputCharsPerItem,
    });
    probes += 1;
    const payload = parsePayload(rawResult);
    const status = threadStatus(payload);
    const turns = turnsFrom(payload);
    if (turns.length) newestTurnId = turns[0].id || turns[0].turnId || newestTurnId;

    if (status === "failed") {
      return { status: "failed", task_id: taskId, probes, newest_turn_id: newestTurnId };
    }

    for (const turn of turns) {
      const turnId = turn.id || turn.turnId || null;
      if (baselineTurnId && turnId === baselineTurnId) break;
      if (turn.status !== "completed") continue;
      const assistant = turnText(turn, "assistant");
      const user = turnText(turn, "user");
      if (!assistant || (!assistant.includes(taskId) && !user.includes(taskId))) continue;
      return completedResult(turn, taskId, probes);
    }

    const remaining = deadline - now();
    if (remaining <= 0) break;
    await sleep(Math.min(intervalMs, remaining));
  }

  return {
    status: "pending",
    task_id: taskId,
    probes,
    newest_turn_id: newestTurnId,
    raw_envelope_suppressed: true,
  };
}
