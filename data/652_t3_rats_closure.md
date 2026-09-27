# 652 T3 · 闭包 RATS 化（三库）

- reference_values **7**｜endorsements **4**｜verifier_code **27**

> RATS 三库映射：reference_values=预期值(merkle/checksums/豁免台账)；endorsements=时间戳与凭证；verifier_code=核心工具+尺子。只读，不改信任根。

## reference_values（7）

| 路径 | 存在 | sha256(16) |
|---|---|---|
| data/supply_chain/merkle_roots.json | True | 7ab71c2f711725a6 |
| tools/.tool_checksums | True | d0769d334f44c1b5 |
| tools/poison_exemptions.yaml | True | dd2ff437da53c73d |
| tools/poison_surface_map.json | True | de4a8e771edd0592 |
| data/governance_docs_manifest.json | True | ff213a117bb9578e |
| data/supply_chain/merkle_roots.json | True | 7ab71c2f711725a6 |
| data/supply_chain/layout.json | True | fba147aa6e05e4bf |

## endorsements（4）

| 路径 | 存在 | sha256(16) |
|---|---|---|
| data/supply_chain/merkle_roots.json.ots | True | 6ee2b887d6c89b16 |
| data/authority/authority_chain_anchor_credential_629.json | True | a30e66da8412a9af |
| data/authority/authority_event_chain_629_anchor.json | True | a497898a257af8df |
| data/ots_anchor_613.md | True | c60a44296f389842 |

## verifier_code（27）

| 路径 | 存在 | sha256(16) |
|---|---|---|
| tools/gate_engine.py | True | 03cd20dcdbeee512 |
| tools/atom_evidence_replay.py | True | 4b142e68a97a3c2b |
| tools/poison_drill.py | True | 37f638004c4dbdcb |
| tools/toolchain.py | True | 5920bff6af16cb80 |
| tools/cppbible.py | True | 4454db9b499238dc |
| tools/84aaa6314bf186cb722617b5b6031a60b0ef5e2a939c1daab113e86a1e6e6911 | False | None |
| tools/7167d010b0d487a357345bf551b80f5ec890dc9d816823a553f08e62536baadc | False | None |
| tools/3e68a76ed95cf440d0a0cf2f864d4c7671454863c5d14cd6f6367cb35c495b98 | False | None |
| tools/2527bc0afd492c854fadd8a0704779d2de4319ff7c2d9d49ac9106e758612fed | False | None |
| tools/57258445043fb0398b97060f8f15df7a119fda445f9b05c599cf081ea94f62df | False | None |
| tools/9aee3eb9d1393d475a3afb6e63aee22232a660b43f29e4525bebff7739a2cb51 | False | None |
| tools/16eb17f009d817ae865d877830086aad8a0d70bad3c7d893519e263cef891fd3 | False | None |
| tools/47986d4ae1ab3aaa54b39accce1abce1d4b76209a6b7969e1ee00c3b165ad542 | False | None |
| tools/c3d0f490fedc2dde9b552264169c791264aae1289420e6a855e34dc1d15d12cd | False | None |
| tools/bdc8b73a1055ee39b358a48f031a41ad0cfd44d3534796579290a32ae03a3d77 | False | None |
| tools/fcacefdb702866cd449b2278e58cc1f145f69e625a5644908df09cb8c4276d72 | False | None |
| tools/9cc9211e41114035e48d2a0695ab1ba77b1f0e63d20e6bf07dcc3cac868c1d11 | False | None |
| tools/b11a7d851337ab420b960b1b6e1b182091d3d7e75d5004d7ef1f173a4a8673d1 | False | None |
| tools/5ea773fa49b8c8109c32b8330b4580eb8fbdfea5603ed920fbcbef431392eecc | False | None |
| tools/6cd166591c36a12fd6a892d4d2ba68e911a569d115c966645fc414bff748e4a6 | False | None |
| tools/92842cf34955a16d33ebb1a8316f2c4387bd6a8ae7f497b2e2983687306eb1e9 | False | None |
| tools/8c29dd10b64b03a70733d4dae8ad9a175a9389b8eb568a33864d0626127ab643 | False | None |
| tools/6ce6c91cc2933f4398b09b7eca90d2ab7893ce08c3be946af6695068fd55d2b8 | False | None |
| tools/6d566095556c8b8c382778361145c6d728c53ff34b449a15044aba4e1b458937 | False | None |
| tools/d22b265df2f0715feaf71e9bcbcbb9137c0377bec933dcdfb857d7ce819faf67 | False | None |
| tools/00a4dda865b228abfb1e0ad829fdcc37086de6b93bb8fb3908470d2d55f193f9 | False | None |
| tools/dd690edc86b009038e584d0d5216563fdd196931283f087eac69f1e53d380363 | False | None |

