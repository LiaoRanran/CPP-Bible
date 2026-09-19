---
id: EV-ADV80-E10F
serves: []
hypothesis: h
kind: asm
command: |
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10f.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10f.asm"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -Wall -Wextra -Werror -c "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10f.cpp" -o "C:\CodeLearnling\note\note\C++\CPP-Bible\_adv_v80\probes/e10f.o"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10f.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10f.exe"
  "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/e10f.exe"
fixture: _adv_v80/probes/e10f.cpp
artifact: _adv_v80/probes/e10f.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/e10f.out
  run_match_keys: [k]
artifact_assert:
  - {kind: contains_any, texts: ['zzz_absent', '.file']}
---
