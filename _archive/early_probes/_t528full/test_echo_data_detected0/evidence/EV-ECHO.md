---
id: EV-ECHO
serves: []
hypothesis: h
kind: run
command: 'g++ cat.cpp -o a.exe && ./a.exe'
fixture: cat.cpp
artifact: a.asm
artifact_sha256: 0000000000000000000000000000000000000000000000000000000000000000
verdict: confirm
falsification: f
---
