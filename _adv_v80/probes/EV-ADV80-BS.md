---
id: EV-ADV80-BS
serves: []
hypothesis: h
kind: asm
command: |
  python -c "print(1)"  # C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/bs.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/bs.asm"

fixture: _adv_v80/probes/bs.cpp
artifact: _adv_v80/probes/bs.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/bs.out
  run_match_keys: [k]
---
