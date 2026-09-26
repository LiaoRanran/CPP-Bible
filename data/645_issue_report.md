# 645 问题发现报告（A1，真实数据 Top10）

- 真实命中规则数：10
- 真实盲区规则数：54
- 产出问题数：10

### ISSUE-ATOM-CLAIM-CONCEPT-NORMALIZED（low, score=231.0）
- 根因：规则 ATOM-CLAIM-CONCEPT-NORMALIZED 当前真实命中 77 次（gate_engine.run 真实产出）
- 证据：rule:ATOM-CLAIM-CONCEPT-NORMALIZED, hits:77
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-MATRIX-UNBACKED（low, score=48.0）
- 根因：规则 EV-MATRIX-UNBACKED 当前真实命中 16 次（gate_engine.run 真实产出）
- 证据：rule:EV-MATRIX-UNBACKED, hits:16
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-OBSERVATION-LIVENESS（low, score=24.0）
- 根因：规则 OBSERVATION-LIVENESS 当前真实命中 8 次（gate_engine.run 真实产出）
- 证据：rule:OBSERVATION-LIVENESS, hits:8
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-OUT-UNDECLARED-KEY（low, score=18.0）
- 根因：规则 EV-OUT-UNDECLARED-KEY 当前真实命中 6 次（gate_engine.run 真实产出）
- 证据：rule:EV-OUT-UNDECLARED-KEY, hits:6
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-FALSIFICATION-QUANT（low, score=12.0）
- 根因：规则 EV-FALSIFICATION-QUANT 当前真实命中 4 次（gate_engine.run 真实产出）
- 证据：rule:EV-FALSIFICATION-QUANT, hits:4
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-ASSERT-SYMBOL-MAPPED（high, score=9.0）
- 根因：规则 EV-ASSERT-SYMBOL-MAPPED 当前真实命中 3 次（gate_engine.run 真实产出）
- 证据：rule:EV-ASSERT-SYMBOL-MAPPED, hits:3
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-OUT-STALE-MTIME（low, score=6.0）
- 根因：规则 EV-OUT-STALE-MTIME 当前真实命中 2 次（gate_engine.run 真实产出）
- 证据：rule:EV-OUT-STALE-MTIME, hits:2
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-ATOM-REL-TARGET（low, score=6.0）
- 根因：规则 ATOM-REL-TARGET 当前真实命中 2 次（gate_engine.run 真实产出）
- 证据：rule:ATOM-REL-TARGET, hits:2
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-EV-ENV-DEPENDENT-KEY（high, score=6.0）
- 根因：规则 EV-ENV-DEPENDENT-KEY 当前真实命中 2 次（gate_engine.run 真实产出）
- 证据：rule:EV-ENV-DEPENDENT-KEY, hits:2
- 建议：复核命中是否真问题；高严重度优先人审
### ISSUE-ATOM-STATUS-VALUE（critical, score=5.0）
- 根因：规则 ATOM-STATUS-VALUE（block）在全库 0 命中 → 覆盖盲区（真实盲区）
- 证据：rule:ATOM-STATUS-VALUE, blind_spot
- 建议：补充该规则能命中的卡片/证据，或评估是否退役
