# 634 A2 · 79 个无 --check 老工具批补

- 目标工具数：**79**（来自 633 B2 登记口径，复算）
- 分组：**4** 组（每组 ~20）

| 组 | 数量 | 示例 |
|---|---|---|
| 0 | 20 | adversarial_regression.py, artifact_version_stamp.py, asm_prepush_guard.py … |
| 1 | 20 | d5_gap_scanner.py, dangling_ref_linter.py, data_sanity_audit.py … |
| 2 | 20 | human_review_confirm.py, human_review_pre_annotate.py, hy3_check.py … |
| 3 | 19 | review_triage.py, round3_mutator_623.py, run_cpp_assertions.py … |

## 守卫范式

```python
if "--check" in sys.argv:
    print("OK: <name> --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)
```

## 诚实登记

1. `--check` 语义为「**加载即校验**」：跑工具时先执行全部顶层代码（import/常量/
   函数定义），能无错到达守卫 ⇒ 证明工具可加载；**不跑业务逻辑、不写盘**；
2. **无 `__main__` 守卫**的工具（纯库/无 CLI）→ 登记例外，不强行加；
3. 守卫在**顶层**拦截，对以 `import` 方式调用该工具的测试无影响（仅 `__main__` 时生效）；
4. 本批**只加守卫**，不改任何业务逻辑（§零.5）。
