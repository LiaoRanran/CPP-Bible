---
id: EV-E1
serves: []
hypothesis: h
kind: run
command: g++ fx.cpp -o a.exe
fixture: fx.cpp
artifact: a.asm
artifact_sha256: 0000000000000000000000000000000000000000000000000000000000000000
verdict: confirm
falsification: f
actual:
  run_match_file: e.out
  run_match_keys: [nproc, result]
---
