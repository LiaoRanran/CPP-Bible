#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_raii_676cC.py — 修复 032/034/036 三个 raii 样本。

原缺陷为 'if (0) throw 1;' 死代码 -> new[] 后正常路径 delete[] 执行，
实际无泄漏，检测器 correctly miss。改为真实可达的泄漏（LeakSanitizer 可抓）。
"""
import os, json

EXP = os.path.dirname(os.path.abspath(__file__))

NEW = {
    32: (
        "int main(){\n"
        "  int* p = new int[16];   // <<PLANTED-DEFECT>> 分配后从未释放 -> 内存泄漏\n"
        "  (void)p;\n"
        "  return 0;\n"
        "}\n",
        2, "main",
        "int* p = new int[16];   // <<PLANTED-DEFECT>> 分配后从未释放 -> 内存泄漏",
        "raii_violation 内存泄漏：new[] 分配后无任何释放路径，LeakSanitizer 在程序正常退出时抓泄漏。"
    ),
    34: (
        "int main(){\n"
        "  int* p = new int[16];\n"
        "  if (true) return 0;   // <<PLANTED-DEFECT>> 提前返回，p 未释放 -> 内存泄漏\n"
        "  delete[] p;\n"
        "  return 0;\n"
        "}\n",
        3, "main",
        "if (true) return 0;   // <<PLANTED-DEFECT>> 提前返回，p 未释放 -> 内存泄漏",
        "raii_violation 内存泄漏：分支提前 return，delete[] 不可达，LeakSanitizer 抓。"
    ),
    36: (
        "int main(){\n"
        "  int* p = new int[16];\n"
        "  try {\n"
        "    throw 1;\n"
        "  } catch (int) {\n"
        "    return 0;   // <<PLANTED-DEFECT>> 异常路径提前返回，p 未释放 -> 内存泄漏\n"
        "  }\n"
        "  delete[] p;\n"
        "  return 0;\n"
        "}\n",
        6, "main",
        "return 0;   // <<PLANTED-DEFECT>> 异常路径提前返回，p 未释放 -> 内存泄漏",
        "raii_violation 异常安全泄漏：throw 被 catch 后直接 return，delete[] 被跳过，LeakSanitizer 抓。"
    ),
}

for n, (cpp, ln, fn, dnote, notes) in NEW.items():
    p = os.path.join(EXP, f"sample_{n:03d}.cpp")
    open(p, "w", encoding="utf-8").write(cpp)
    jp = os.path.join(EXP, f"sample_{n:03d}.json")
    m = json.load(open(jp, encoding="utf-8"))
    m["expected_verdict"] = "catch"
    m["expected_detectors"] = ["asan"]
    m["defect_location"] = {"line": ln, "function": fn, "note": dnote}
    m["notes"] = notes
    # 移除旧的 verification（重验证时会重写）
    m.pop("verification", None)
    json.dump(m, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"sample_{n:03d} fixed: leak on line {ln}")
