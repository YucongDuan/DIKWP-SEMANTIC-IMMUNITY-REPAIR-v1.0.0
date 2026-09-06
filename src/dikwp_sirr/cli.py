from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import analyze
from .formatters import to_markdown
from .ledger import ResponsibilityLedger
from .models import SemanticCase
from .provenance import c2pa_style_reference
from .server import serve


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_outputs(result: dict, output: str | None, ledger_path: str | None) -> None:
    if output:
        out = Path(output)
        out.mkdir(parents=True, exist_ok=True)
        (out / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "analysis.md").write_text(to_markdown(result), encoding="utf-8")
        (out / "provenance-reference.json").write_text(json.dumps(c2pa_style_reference(result), ensure_ascii=False, indent=2), encoding="utf-8")
    if ledger_path:
        ResponsibilityLedger(ledger_path).append("semantic_analysis", {"case_digest": result["case_digest"], "decision": result["decision"]})


def cmd_analyze(args: argparse.Namespace) -> int:
    case = SemanticCase.from_dict(_read_json(args.input))
    result = analyze(case).to_dict()
    _write_outputs(result, args.output, args.ledger)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    cases = [
        SemanticCase(
            text="女性要先好好照顾自己才能照顾孩子，真正觉醒的妈妈都应该马上报名这门课程。",
            domain="family_parenting",
            content_role="marketing",
            audience_context=["caregiver_fatigue", "low_domain_literacy"],
            monetized=True,
            paid_funnel=True,
            evidence_quality=0.15,
            source_traceability=0.1,
            reach=0.7,
        ),
        SemanticCase(
            text="这份事故报告令人不安，但日志和内部文件显示系统没有按承诺执行。请独立复核。",
            domain="general",
            content_role="whistleblowing",
            evidence_quality=0.75,
            source_traceability=0.8,
        ),
    ]
    results = [analyze(c).to_dict() for c in cases]
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "demo-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    for idx, result in enumerate(results, start=1):
        (out / f"demo-{idx}.md").write_text(to_markdown(result), encoding="utf-8")
    print(json.dumps({"cases": len(results), "output": str(out), "decisions": [r["decision"] for r in results]}, ensure_ascii=False, indent=2))
    return 0


def cmd_verify_ledger(args: argparse.Namespace) -> int:
    result = ResponsibilityLedger(args.path).verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 2


def cmd_serve(args: argparse.Namespace) -> int:
    serve(args.host, args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sirr", description="DIKWP Semantic Immunity & Repair OS")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Analyze a semantic case JSON file")
    p_analyze.add_argument("input")
    p_analyze.add_argument("--output")
    p_analyze.add_argument("--ledger")
    p_analyze.set_defaults(func=cmd_analyze)

    p_demo = sub.add_parser("demo", help="Run built-in demonstration cases")
    p_demo.add_argument("--output", default=".sirr-demo")
    p_demo.set_defaults(func=cmd_demo)

    p_verify = sub.add_parser("verify-ledger", help="Verify a responsibility ledger")
    p_verify.add_argument("path")
    p_verify.set_defaults(func=cmd_verify_ledger)

    p_serve = sub.add_parser("serve", help="Run the local loopback JSON API")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8765)
    p_serve.set_defaults(func=cmd_serve)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
