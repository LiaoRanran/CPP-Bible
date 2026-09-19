---
id: EV-ADV80-E05C
serves: []
hypothesis: h
kind: asm
command: |
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e05c.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e05c.asm"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e05c.cpp" -o "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e05c.exe"
  "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e05c.exe"

fixture: _adv_v80/probes/e05c.cpp
artifact: _adv_v80/probes/e05c.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/e05c.out
  run_match_keys: [result]
---
