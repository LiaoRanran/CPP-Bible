Set-Location "C:\CodeLearnling\note\note\C++\CPP-Bible"
$t = Measure-Command { .venv\Scripts\python.exe tools/golden_lock.py check *> _t2a568.log }
"GOLDEN-CHECK = $([int]$t.TotalSeconds)s" | Out-File -Append -Encoding utf8 _t2a568.out
