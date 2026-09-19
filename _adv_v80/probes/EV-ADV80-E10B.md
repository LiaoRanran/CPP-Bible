---
id: EV-ADV80-E10B
serves: []
hypothesis: h
kind: asm
command: |
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10b.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10b.asm"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -Wall -Wextra -Werror -c "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10b.cpp" -o "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10b.o"

fixture: _adv_v80/probes/e10b.cpp
artifact: _adv_v80/probes/e10b.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/e10b.out
  run_match_keys: [k]
---
