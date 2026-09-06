from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
FORBIDDEN = {
    "os.system(": "shell execution",
    "subprocess.Popen": "external process execution",
    "subprocess.run": "external process execution",
    "requests.": "network client",
    "urllib.request": "network client",
    "socket.socket": "raw network socket",
    "eval(": "dynamic evaluation",
    "exec(": "dynamic execution",
}
findings = []
for path in list((ROOT / "src").rglob("*.py")) + list((ROOT / "extension").rglob("*.js")):
    text = path.read_text(encoding="utf-8")
    for token, category in FORBIDDEN.items():
        if token in text:
            findings.append({"file": str(path.relative_to(ROOT)), "token": token, "category": category})
print(json.dumps({"files_scanned": len(list((ROOT / 'src').rglob('*.py'))) + len(list((ROOT / 'extension').rglob('*.js'))), "findings": findings}, indent=2))
raise SystemExit(1 if findings else 0)
