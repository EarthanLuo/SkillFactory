#!/usr/bin/env python3
"""Prepare, filter, extract, budget, clean, and audit stand-in tasks."""

from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TASK_ID_RE = re.compile(r"\bWST-\d{8}(?:-\d{6})?(?:-[A-Za-z0-9]+)?\b")
CONTENT_REFERENCE_RE = re.compile(r':chatgpt-content-reference\{[^{}]*\}')
URL_RE = re.compile(r"https?://[^\s<>\]\[\)]+")
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
DEFAULT_DELEGATED_AUTHORITY = [
    "Choose and refine search queries within the stated scope.",
    "Select, replace, deduplicate, and compare relevant sources.",
    "Decide when the available evidence is sufficient for a bounded conclusion.",
    "Synthesize findings and identify conflicts, limitations, and uncertainty.",
]


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def as_list(data: dict, key: str) -> list[str]:
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def bullet_section(title: str, items: list[str]) -> list[str]:
    if not items:
        return []
    return [f"## {title}", "", *[f"- {item}" for item in items], ""]


def generate_task_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"WST-{stamp}-{secrets.token_hex(2).upper()}"


def read_json(path: str) -> object:
    return json.loads(read_text(path))


def unwrap_conversation_payload(value: object) -> dict:
    """Accept a direct thread response or a CallToolResult-like JSON envelope."""
    if isinstance(value, dict) and isinstance(value.get("thread"), dict):
        return value
    if isinstance(value, dict) and isinstance(value.get("content"), list):
        for item in value["content"]:
            if not isinstance(item, dict) or item.get("type") != "text":
                continue
            candidate = item.get("text")
            if not isinstance(candidate, str):
                continue
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict) and isinstance(parsed.get("thread"), dict):
                return parsed
    raise ValueError("input does not contain a supported conversation response")


def conversation_payload(path: str) -> dict:
    return unwrap_conversation_payload(read_json(path))


def item_role(item: dict) -> str | None:
    item_type = item.get("type")
    role = item.get("role")
    if item_type in {"agentMessage", "assistantMessage"} or role in {"agent", "assistant"}:
        return "assistant"
    if item_type == "userMessage" or role == "user":
        return "user"
    return None


def item_text(item: dict) -> str:
    if isinstance(item.get("text"), str):
        return item["text"]
    content = item.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            part["text"]
            for part in content
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        )
    return ""


def turn_text(turn: dict, role: str) -> str:
    pieces: list[str] = []
    for item in turn.get("items", []):
        if not isinstance(item, dict) or item_role(item) != role:
            continue
        text = item_text(item)
        if text:
            pieces.append(text)
    return "\n".join(pieces).strip()


def probe(args: argparse.Namespace) -> dict:
    data = conversation_payload(args.input)
    thread = data.get("thread", {})
    turns = data.get("turns", [])
    newest = turns[0] if isinstance(turns, list) and turns and isinstance(turns[0], dict) else {}
    result = {
        "mode": "probe",
        "thread_id": thread.get("id"),
        "thread_status": (thread.get("status") or {}).get("type"),
        "newest_turn_id": newest.get("id"),
        "newest_turn_status": newest.get("status"),
        "has_more": (data.get("page") or {}).get("hasMore"),
    }
    if args.output:
        write_text(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


def extract(args: argparse.Namespace) -> dict:
    data = conversation_payload(args.input)
    turns = data.get("turns", [])
    if not isinstance(turns, list):
        raise ValueError("conversation turns must be a list")

    selected: dict | None = None
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        if args.after_turn and turn.get("id") == args.after_turn:
            break
        agent_text = turn_text(turn, "assistant")
        user_text = turn_text(turn, "user")
        if turn.get("status") != "completed" or not agent_text:
            continue
        if args.task_id not in agent_text and args.task_id not in user_text:
            continue
        selected = turn
        break

    if selected is None:
        raise ValueError("no completed turn matching task_id after the baseline turn")

    raw_answer = turn_text(selected, "assistant").strip()
    placeholder_count = len(CONTENT_REFERENCE_RE.findall(raw_answer))
    answer = CONTENT_REFERENCE_RE.sub("", raw_answer)
    answer = re.sub(r"[ \t]+\n", "\n", answer)
    answer = re.sub(r" {2,}", " ", answer).strip() + "\n"
    links = set(URL_RE.findall(answer))
    missing_signals = []
    if not links:
        missing_signals.append("links")
    write_text(args.output, answer)
    return {
        "mode": "extract",
        "task_id": args.task_id,
        "turn_id": selected.get("id"),
        "characters": len(answer),
        "link_count": len(links),
        "internal_placeholders_removed": placeholder_count,
        "missing_signals": missing_signals,
        "output": str(Path(args.output)),
    }


def estimate_tokens(text: str) -> int:
    cjk = len(re.findall(r"[\u3400-\u9fff]", text))
    non_cjk = len(re.sub(r"[\s\u3400-\u9fff]", "", text))
    return cjk + (non_cjk + 3) // 4


def budget(args: argparse.Namespace) -> dict:
    content = read_text(args.input)
    characters = len(content)
    links = len(set(URL_RE.findall(content)))
    estimated_tokens = estimate_tokens(content)
    exceeded = []
    if args.max_chars is not None and characters > args.max_chars:
        exceeded.append("characters")
    if args.max_links is not None and links > args.max_links:
        exceeded.append("links")
    if args.max_estimated_tokens is not None and estimated_tokens > args.max_estimated_tokens:
        exceeded.append("estimated_tokens")
    report = {
        "mode": "budget",
        "within_budget": not exceeded,
        "receive_policy": "accept_and_report",
        "characters": characters,
        "link_count": links,
        "estimated_tokens": estimated_tokens,
        "estimate_is_heuristic": True,
        "exceeded": exceeded,
    }
    write_text(args.report, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if exceeded and args.compression_output:
        request = (
            f"The returned answer for `{args.task_id}` exceeds the requested complete-payload budget "
            f"({', '.join(exceeded)}). Compress it in this same conversation. Keep the task ID, core "
            "conclusions, only the essential evidence links, material limitations, and at most three "
            "verification targets. Do not repeat the research process.\n"
        )
        write_text(args.compression_output, request)
        report["compression_output"] = str(Path(args.compression_output))
        report["compression_requires_explicit_request"] = True
    return report


def ledger(args: argparse.Namespace) -> dict:
    path = Path(args.file)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("events", []), list):
            raise ValueError("ledger must be a JSON object with an events list")
    else:
        data = {"events": []}
    event = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "task_id": args.task_id,
        "event": args.event,
    }
    for key in ("conversation_id", "route", "baseline_turn", "latest_turn", "note"):
        value = getattr(args, key)
        if value:
            event[key] = value
    data["events"].append(event)
    write_text(args.file, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return {
        "mode": "ledger",
        "task_id": args.task_id,
        "event": args.event,
        "event_count": len(data["events"]),
        "file": str(path),
    }


def prepare(args: argparse.Namespace) -> dict:
    data = json.loads(read_text(args.input))
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")

    objective = data.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective is required and must be a non-empty string")

    task_id = args.task_id or data.get("task_id") or generate_task_id()
    if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
        raise ValueError("task_id must match WST-YYYYMMDD[-HHMMSS][-SUFFIX]")

    research_scope = data.get("research_scope")
    if research_scope is not None and not isinstance(research_scope, str):
        raise ValueError("research_scope must be a string when provided")

    research_mode = data.get("research_mode", "decision-focused research")
    return_budget = data.get(
        "return_budget",
        "Return only a compact decision package; the complete payload, including headings, Markdown, citations, and URLs, must remain within the stated budget. Do not return a full research transcript or exhaustive table.",
    )
    evidence_budget = data.get(
        "evidence_budget",
        "Include only the key sources needed to support the returned conclusions.",
    )
    for key, value in (
        ("research_mode", research_mode),
        ("return_budget", return_budget),
        ("evidence_budget", evidence_budget),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")

    delegated_authority = data.get("delegated_authority", DEFAULT_DELEGATED_AUTHORITY)
    if not isinstance(delegated_authority, list) or not all(
        isinstance(item, str) for item in delegated_authority
    ):
        raise ValueError("delegated_authority must be a list of strings")
    delegated_authority = [item.strip() for item in delegated_authority if item.strip()]

    lines = [f"# Stand-in Task {task_id}", "", "## Objective", "", objective.strip(), ""]
    lines += bullet_section("Acceptance Criteria", as_list(data, "acceptance_criteria"))
    lines += bullet_section("Authoritative Materials", as_list(data, "materials"))
    lines += bullet_section("Constraints", as_list(data, "constraints"))
    if research_scope:
        lines += ["## Research Scope", "", research_scope.strip(), ""]
    lines += ["## Research Mode", "", research_mode.strip(), ""]
    lines += bullet_section("Delegated Research Authority", delegated_authority)
    lines += ["## Return Budget", "", return_budget.strip(), ""]
    lines += ["## Evidence Budget", "", evidence_budget.strip(), ""]
    lines += bullet_section("Output Requirements", as_list(data, "output_requirements"))
    lines += bullet_section("Forbidden Actions", as_list(data, "forbidden_actions"))
    lines += [
        "## Return Contract",
        "",
        f"Start the final answer with `{task_id} completed`. Return a decision package containing the core conclusions, a compact evidence map, material conflicts or counterexamples, limitations and uncertainty, and one to three claims the coordinating task should verify. Apply the return budget to the complete payload, including headings, Markdown, citations, and URLs. Keep detailed search steps and exhaustive working material in this conversation unless explicitly requested. Use ordinary Markdown links and do not emit internal citation placeholders.",
        "",
    ]

    content = "\n".join(lines)
    write_text(args.output, content)
    return {"mode": "prepare", "task_id": task_id, "output": str(Path(args.output))}


def clean_url(url: str) -> tuple[str, int]:
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    kept = []
    removed = 0
    for key, value in query:
        if key.lower().startswith("utm_") or key.lower() in TRACKING_KEYS:
            removed += 1
        else:
            kept.append((key, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), parts.fragment)), removed


def clean(args: argparse.Namespace) -> dict:
    original = read_text(args.input).replace("\r\n", "\n")
    placeholder_count = len(CONTENT_REFERENCE_RE.findall(original))
    text = CONTENT_REFERENCE_RE.sub("", original)

    tracking_removed = 0

    def replace_url(match: re.Match[str]) -> str:
        nonlocal tracking_removed
        cleaned, count = clean_url(match.group(0))
        tracking_removed += count
        return cleaned

    text = URL_RE.sub(replace_url, text)
    paragraphs = re.split(r"\n{2,}", text)
    seen: set[str] = set()
    kept: list[str] = []
    duplicates_removed = 0
    for paragraph in paragraphs:
        normalized = re.sub(r"\s+", " ", paragraph).strip()
        if not normalized:
            continue
        if normalized in seen:
            duplicates_removed += 1
            continue
        seen.add(normalized)
        kept.append(paragraph.strip())

    cleaned_text = "\n\n".join(kept).strip() + "\n"
    write_text(args.output, cleaned_text)

    task_ids = sorted(set(TASK_ID_RE.findall(cleaned_text)))
    links = sorted(set(URL_RE.findall(cleaned_text)))
    lower = cleaned_text.lower()
    missing = []
    if not task_ids:
        missing.append("task_id")
    if not links:
        missing.append("links")
    if not any(term in lower for term in ("limitation", "uncertaint", "限制", "不确定")):
        missing.append("limitations_or_uncertainty")

    report = {
        "mode": "clean",
        "input": str(Path(args.input)),
        "output": str(Path(args.output)),
        "task_ids": task_ids,
        "links": links,
        "internal_placeholders_removed": placeholder_count,
        "tracking_parameters_removed": tracking_removed,
        "duplicate_paragraphs_removed": duplicates_removed,
        "missing_signals": missing,
    }
    write_text(args.report, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return {
        "mode": "clean",
        "task_ids": task_ids,
        "link_count": len(links),
        "internal_placeholders_removed": placeholder_count,
        "tracking_parameters_removed": tracking_removed,
        "duplicate_paragraphs_removed": duplicates_removed,
        "missing_signals": missing,
        "output": str(Path(args.output)),
        "report": str(Path(args.report)),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="build a Markdown task package from JSON")
    prepare_parser.add_argument("--input", required=True, help="UTF-8 JSON task specification")
    prepare_parser.add_argument("--output", required=True, help="Markdown package output")
    prepare_parser.add_argument("--task-id", help="optional explicit WST task ID")
    prepare_parser.set_defaults(handler=prepare)

    probe_parser = subparsers.add_parser("probe", help="reduce a conversation response to status metadata")
    probe_parser.add_argument("--input", required=True, help="JSON conversation response")
    probe_parser.add_argument("--output", help="optional JSON status output")
    probe_parser.set_defaults(handler=probe)

    extract_parser = subparsers.add_parser("extract", help="extract one completed task answer")
    extract_parser.add_argument("--input", required=True, help="JSON conversation response")
    extract_parser.add_argument("--output", required=True, help="Markdown answer output")
    extract_parser.add_argument("--task-id", required=True, help="expected WST task ID")
    extract_parser.add_argument("--after-turn", help="optional baseline turn ID")
    extract_parser.set_defaults(handler=extract)

    budget_parser = subparsers.add_parser("budget", help="measure and report returned payload variance")
    budget_parser.add_argument("--input", required=True, help="returned Markdown response")
    budget_parser.add_argument("--report", required=True, help="JSON budget report")
    budget_parser.add_argument("--task-id", required=True, help="WST task ID")
    budget_parser.add_argument("--max-chars", type=int)
    budget_parser.add_argument("--max-links", type=int)
    budget_parser.add_argument("--max-estimated-tokens", type=int)
    budget_parser.add_argument(
        "--compression-output",
        help="write an optional follow-up only when explicitly requested; never send automatically",
    )
    budget_parser.set_defaults(handler=budget)

    clean_parser = subparsers.add_parser("clean", help="clean a returned Markdown response")
    clean_parser.add_argument("--input", required=True, help="UTF-8 raw response")
    clean_parser.add_argument("--output", required=True, help="cleaned Markdown output")
    clean_parser.add_argument("--report", required=True, help="JSON cleaning report")
    clean_parser.set_defaults(handler=clean)

    ledger_parser = subparsers.add_parser("ledger", help="append a task-local audit event")
    ledger_parser.add_argument("--file", required=True, help="JSON event ledger")
    ledger_parser.add_argument("--task-id", required=True, help="WST task ID")
    ledger_parser.add_argument("--event", required=True, help="observed event; no transition is inferred")
    ledger_parser.add_argument("--conversation-id")
    ledger_parser.add_argument("--route")
    ledger_parser.add_argument("--baseline-turn")
    ledger_parser.add_argument("--latest-turn")
    ledger_parser.add_argument("--note")
    ledger_parser.set_defaults(handler=ledger)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
