# 652 M4 · 挑战者（对已通过卡反向生成更难变体）

- 卡 10｜变体 50｜检出 50｜漏 0｜**逃逸率 0.0**

| 卡 | 算子 | 已变 | 读取面OK | 缺字段 | MDL代理 | 检出 |
|---|---|---|---|---|---|---|
| ATOM-LANG-DECAY-001 | M1_delete_boundary | True | False | claim_boundary | 2454 | True |
| ATOM-LANG-DECAY-001 | M2_weaken_claim | True | True |  | 2557 | True |
| ATOM-LANG-DECAY-001 | M3_drop_liveness | True | False | liveness | 2514 | True |
| ATOM-LANG-DECAY-001 | M4_drop_evidence | True | True |  | 2565 | True |
| ATOM-LANG-DECAY-001 | M5_status_flip | True | True |  | 2581 | True |
| ATOM-MEM-MALLOC-001 | M1_delete_boundary | True | False | claim_boundary | 2483 | True |
| ATOM-MEM-MALLOC-001 | M2_weaken_claim | True | True |  | 2566 | True |
| ATOM-MEM-MALLOC-001 | M3_drop_liveness | True | False | liveness | 2539 | True |
| ATOM-MEM-MALLOC-001 | M4_drop_evidence | True | True |  | 2595 | True |
| ATOM-MEM-MALLOC-001 | M5_status_flip | True | True |  | 2610 | True |
| ATOM-MEM-STRBOUND-001 | M1_delete_boundary | True | False | claim_boundary | 2465 | True |
| ATOM-MEM-STRBOUND-001 | M2_weaken_claim | True | True |  | 2515 | True |
| ATOM-MEM-STRBOUND-001 | M3_drop_liveness | True | False | liveness | 2529 | True |
| ATOM-MEM-STRBOUND-001 | M4_drop_evidence | True | True |  | 2577 | True |
| ATOM-MEM-STRBOUND-001 | M5_status_flip | True | True |  | 2592 | True |
| ATOM-LANG-FNPTR-001 | M1_delete_boundary | True | False | claim_boundary | 2146 | True |
| ATOM-LANG-FNPTR-001 | M2_weaken_claim | True | True |  | 2245 | True |
| ATOM-LANG-FNPTR-001 | M3_drop_liveness | True | False | liveness | 2213 | True |
| ATOM-LANG-FNPTR-001 | M4_drop_evidence | True | True |  | 2257 | True |
| ATOM-LANG-FNPTR-001 | M5_status_flip | True | True |  | 2273 | True |
| ATOM-LANG-VOLATILE-001 | M1_delete_boundary | True | False | claim_boundary | 2247 | True |
| ATOM-LANG-VOLATILE-001 | M2_weaken_claim | True | True |  | 2320 | True |
| ATOM-LANG-VOLATILE-001 | M3_drop_liveness | True | False | liveness | 2311 | True |
| ATOM-LANG-VOLATILE-001 | M4_drop_evidence | True | True |  | 2358 | True |
| ATOM-LANG-VOLATILE-001 | M5_status_flip | True | True |  | 2374 | True |
| ATOM-LANG-SETJMP-001 | M1_delete_boundary | True | False | claim_boundary | 2374 | True |
| ATOM-LANG-SETJMP-001 | M2_weaken_claim | True | True |  | 2462 | True |
| ATOM-LANG-SETJMP-001 | M3_drop_liveness | True | False | liveness | 2440 | True |
| ATOM-LANG-SETJMP-001 | M4_drop_evidence | True | True |  | 2485 | True |
| ATOM-LANG-SETJMP-001 | M5_status_flip | True | True |  | 2501 | True |
| ATOM-LANG-INTPROMO-001 | M1_delete_boundary | True | False | claim_boundary | 2510 | True |
| ATOM-LANG-INTPROMO-001 | M2_weaken_claim | True | True |  | 2577 | True |
| ATOM-LANG-INTPROMO-001 | M3_drop_liveness | True | False | liveness | 2574 | True |
| ATOM-LANG-INTPROMO-001 | M4_drop_evidence | True | True |  | 2621 | True |
| ATOM-LANG-INTPROMO-001 | M5_status_flip | True | True |  | 2637 | True |
| ATOM-LANG-BITFIELD-001 | M1_delete_boundary | True | False | claim_boundary | 2370 | True |
| ATOM-LANG-BITFIELD-001 | M2_weaken_claim | True | True |  | 2429 | True |
| ATOM-LANG-BITFIELD-001 | M3_drop_liveness | True | False | liveness | 2434 | True |
| ATOM-LANG-BITFIELD-001 | M4_drop_evidence | True | True |  | 2481 | True |
| ATOM-LANG-BITFIELD-001 | M5_status_flip | True | True |  | 2497 | True |

> V2=门禁读取面代表性子集；V1 真机编译见 648 manifest；critic=MDL代理+校准(651 M3)。
