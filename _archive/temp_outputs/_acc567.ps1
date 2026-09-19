$ErrorActionPreference = "Continue"
Set-Location "C:\CodeLearnling\note\note\C++\CPP-Bible"
$py = ".venv\Scripts\python.exe"
"=== INTEGRITY --check ==="
& $py tools/tool_integrity.py --check 2>&1 | Select-Object -First 2
"exit=$LASTEXITCODE"
"=== GATE ==="
& $py tools/gate_engine.py --check 2>&1 | Select-String "规则 61|命中"
"=== POISON ==="
& $py tools/poison_drill.py 2>&1 | Select-String "107/107|双指标"
"=== REPLAY ==="
& $py tools/atom_evidence_replay.py --check 2>&1 | Select-String "confirm="
"=== FAST PYTEST ==="
& $py -m pytest -m "not slow" -n auto -q -p no:cacheprovider 2>&1 | Select-String "passed|failed" | Select-Object -Last 2
"=== SLOW PYTEST ==="
& $py -m pytest -m "slow" -n0 -q -p no:cacheprovider 2>&1 | Select-String "passed|failed" | Select-Object -Last 2
"=== INTEGRITY after all ==="
& $py tools/tool_integrity.py --check 2>&1 | Select-Object -First 2
"exit=$LASTEXITCODE"
"=== DONE ==="
