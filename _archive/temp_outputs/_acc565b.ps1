$ErrorActionPreference = "Continue"
Write-Output "=== GATE ==="
& .venv\Scripts\python.exe tools/gate_engine.py --check 2>&1 | Select-String -Pattern "规则" | Select-Object -Last 1
Write-Output "=== POISON ==="
& .venv\Scripts\python.exe tools/poison_drill.py 2>&1 | Select-String -Pattern "/1[0-9][0-9] ——|双指标" | Select-Object -Last 2
Write-Output "=== REPLAY ==="
& .venv\Scripts\python.exe tools/atom_evidence_replay.py --check 2>&1 | Select-String -Pattern "confirm=" | Select-Object -Last 1
Write-Output "=== FAST PYTEST ==="
& .venv\Scripts\python.exe -m pytest -m "not slow" -n auto -q 2>&1 | Select-String -Pattern "passed|failed|error|FAILED" | Select-Object -Last 3
Write-Output "=== DONE ==="
