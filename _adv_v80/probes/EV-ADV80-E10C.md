---
id: EV-ADV80-E10C
serves: []
hypothesis: h
kind: asm
command: |
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10c.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10c.asm"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -Wall -c "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10c.cpp" -o "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10c.o"

fixture: _adv_v80/probes/e10c.cpp
artifact: _adv_v80/probes/e10c.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: 零诊断（编译无警告）
actual:
  run_match_file: _adv_v80/probes/e10c.out
  run_match_keys: [k]
---
