---
id: EV-ADV80-N2
serves: []
hypothesis: h
kind: asm
command: "C:/Qt/Tools/mingw1530_64/bin/g++.exe" -std=c++17 -S "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n2.cpp" -o "C:/CodeLearnling/note/note/C++/CPP-Bible/_adv_v80/probes/n2.asm"
fixture: _adv_v80/probes/n2.cpp
artifact: _adv_v80/probes/n2.asm
artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111
artifact_compiler: Clang 19.0.0 (Linux)
verdict: confirm
falsification: f
expected: any
actual:
  run_match_file: _adv_v80/probes/n2.out
  run_match_keys: [k]
artifact_assert:
  - {kind: contains_any, texts: ['zzz_not_there', '.file']}
---
