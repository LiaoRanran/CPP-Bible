#!/usr/bin/env python3
# 585 只读探针：仅 import 读取，零写盘。验证几个关键断言（带磁盘实证锚点）。
# 运行：.venv\Scripts\python.exe _arch_v10\probes\probe_trust_root.py
import sys, inspect
ROOT = r"C:\CodeLearnling\note\note\C++\CPP-Bible"
sys.path.insert(0, ROOT + r"\tools")

import gate_engine as ge
import tool_integrity as ti

print("RULES_count =", len(ge.RULES))
print("CORE_TOOLS =", ti.CORE_TOOLS)
bl = ti.load_baseline()
print("checksums_self_included =", ".tool_checksums" in bl)
print("checksums_covered_files =", sorted(bl.keys()))
# gate 入口是否自检
src_main = inspect.getsource(ge.main)
print("gate_main_calls_enforce =", ("tool_integrity" in src_main) and ("enforce" in src_main))
# slash 风格：main 首句是否为 enforce
import re
first_calls = [l.strip() for l in src_main.splitlines() if l.strip()][:6]
print("gate_main_first_lines =", first_calls)
# 规则空返回是否静默放过：run() 对 check 返回 [] 的处理
src_run = inspect.getsource(ge.run)
print("run_extends_hits_only =", "out.extend(hits)" in src_run)
# 是否存在“规则函数返回空列表即静默失效”的结构风险
print("run_try_check =", "hits = r.check()" in src_run)
