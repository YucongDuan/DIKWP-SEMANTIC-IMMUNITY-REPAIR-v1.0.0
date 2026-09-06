import json

from dikwp_sirr.ledger import ResponsibilityLedger


def test_ledger_detects_tampering(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = ResponsibilityLedger(path)
    ledger.append("analysis", {"x": 1})
    ledger.append("analysis", {"x": 2})
    assert ledger.verify()["valid"]
    lines = path.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[0])
    event["payload"]["x"] = 99
    lines[0] = json.dumps(event, ensure_ascii=False, sort_keys=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert not ledger.verify()["valid"]
