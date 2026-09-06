import json
import os
import subprocess
import sys


def test_cli_analyze(tmp_path):
    case_path = tmp_path / "case.json"
    case_path.write_text(json.dumps({"text": "可能对部分人有效，需要结合具体情况。"}, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "out"
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([os.path.join(os.path.dirname(__file__), "..", "src"), env.get("PYTHONPATH", "")])
    proc = subprocess.run(
        [sys.executable, "-m", "dikwp_sirr", "analyze", str(case_path), "--output", str(out)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (out / "analysis.json").exists()
    assert (out / "analysis.md").exists()
