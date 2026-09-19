---
id: EV-ADV80-N3
serves: []
hypothesis: h
kind: asm
command: |
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n3.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n3.asm"
  "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n3.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n3.exe"
  "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n3.exe"
fixture: _adv_v80/probes/n3.cpp
artifact: _adv_v80/probes/n3.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/n3.out
  run_match_keys: [k]
artifact_assert:
  - {kind: contains_any, texts: ['zzz_absent', '.file']}
---
