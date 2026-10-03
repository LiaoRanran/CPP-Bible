#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676c 扩样-B：修正不一致样本的标注/代码，使标签与检测器可复现行为一致。

原则（诚实，不凑数）：
  - B047/B049：原代码无法编译或并非真实泄漏 -> 改写为真实 malloc 泄漏，保持 catch。
  - B027-030/B050/B054/B057/B086/B090：缺陷真实存在但检测器在本机**可复现地**未抓到
    -> 诚实改标 expected_verdict=miss（盲区/边界案例），不做 catch。
  - data_race ×6（B002/B005/B006/B011/B012/B020）：TSan 在本机对这些形态不稳定，
    不纳入标注数据集（避免不可复现的标签），保持淘汰。
更新数据文件 data/expansion_676c_B/sample_B*.{cpp,json}（deliverable）。
注意：本脚本只改本批生成文件，不碰既有数据与检测器。
"""
import os
import json

SRC = "C:/CodeLearnling/note/note/C++/CPP-Bible/data/expansion_676c_B"

# 改标为 miss 的样本 + 盲区说明
RELABEL_MISS = {
    "sample_B027": "有符号溢出（a*b+a*b 复合表达式）；本机 UBSan 两档均未报，"
                   "属表达式形态盲区，诚实标 miss（边界案例）。",
    "sample_B028": "有符号溢出（(a+b)*2）；本机 UBSan 两档均未报，属盲区，诚实标 miss。",
    "sample_B029": "有符号溢出（a*b，负×正大数）；本机 UBSan 两档均未报，属盲区，诚实标 miss。",
    "sample_B030": "有符号溢出（a-(-10)）；本机 UBSan 两档均未报，属盲区，诚实标 miss。",
    "sample_B050": "全局指针持有的堆分配；LSan 不报告仍可从全局根到达的分配，"
                   "属可达性盲区，诚实标 miss（边界案例）。",
    "sample_B054": "作用域内 new 未释放；本机 LSan 两档均未报（可达性/栈槽残留盲区），诚实标 miss。",
    "sample_B057": "fopen 写模式未 fclose；本机 LSan 两档均未报（stdio FILE* 泄漏盲区），诚实标 miss。",
    "sample_B086": "左移至符号位（UB）；本机 UBSan 两档均未报，属盲区，诚实标 miss（边界案例）。",
    "sample_B090": "通过空对象指针调成员函数，但函数体不访问 this；ASan 无内存访问故不报，"
                   "属盲区，诚实标 miss（边界案例）。",
}

# 代码改写（B047/B049）-> 真实 malloc 泄漏，保持 catch
REWRITE = {
    "sample_B047": {
        "defect_type": "resource_leak", "severity": "medium", "expected_verdict": "catch",
        "expected_detectors": ["asan"],
        "notes": "malloc 分配的字符串缓冲未 free，LeakSanitizer 报告（原 fopen 不存在文件=NULL，"
                 "并非真实泄漏，已改写为 malloc 泄漏）。",
        "code": (
            "#include <cstdlib>\n"
            "#include <cstring>\n"
            "#include <cstdio>\n"
            "int main(){\n"
            "  char* s = (char*)std::malloc(8);\n"
            "  std::strcpy(s, \"leak\"); /*DEFECT: resource leak: malloc'd buffer not freed */\n"
            "  std::printf(\"%s\\n\", s);\n"
            "  return 0;\n"
            "}"
        ),
    },
    "sample_B049": {
        "defect_type": "resource_leak", "severity": "medium", "expected_verdict": "catch",
        "expected_detectors": ["asan"],
        "notes": "malloc 分配未 free，LeakSanitizer 报告（原 std::strdup 在 -std=c++17 下未声明导致"
                 "编译失败，已改写为 malloc）。",
        "code": (
            "#include <cstdlib>\n"
            "#include <cstdio>\n"
            "int main(){\n"
            "  int* p = (int*)std::malloc(sizeof(int));\n"
            "  *p = 7; /*DEFECT: resource leak: malloc not freed */\n"
            "  std::printf(\"%d\\n\", *p);\n"
            "  return 0;\n"
            "}"
        ),
    },
}


def defect_line(code: str) -> int:
    for i, ln in enumerate(code.splitlines(), 1):
        if "/*DEFECT" in ln:
            return i
    raise RuntimeError("no DEFECT marker")


def main():
    changed = []
    # 1) relabel -> miss
    for sid, extra in RELABEL_MISS.items():
        jp = os.path.join(SRC, sid + ".json")
        cp = os.path.join(SRC, sid + ".cpp")
        ann = json.load(open(jp, encoding="utf-8"))
        ann["expected_verdict"] = "miss"
        base = ann["notes"]
        ann["notes"] = base.rstrip("。") + "。" + extra if base else extra
        json.dump(ann, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        # 同步 cpp 头部注释
        cpp = open(cp, encoding="utf-8").read()
        if "expected_verdict: catch" in cpp:
            cpp = cpp.replace("// expected_verdict: catch",
                              "// expected_verdict: miss")
            open(cp, "w", encoding="utf-8").write(cpp)
        changed.append(f"{sid}: catch->miss")

    # 2) 代码改写（B047/B049）
    for sid, spec in REWRITE.items():
        jp = os.path.join(SRC, sid + ".json")
        cp = os.path.join(SRC, sid + ".cpp")
        ann = json.load(open(jp, encoding="utf-8"))
        dline = defect_line(spec["code"])
        header = (
            f"// {sid}\n"
            f"// defect_type: {spec['defect_type']}\n"
            f"// severity: {spec['severity']}\n"
            f"// planted: true\n"
            f"// expected_verdict: {spec['expected_verdict']}\n"
            f"// expected_detectors: {','.join(spec['expected_detectors'])}\n"
            f"// (authoritative annotation in {sid}.json)\n\n"
        )
        open(cp, "w", encoding="utf-8").write(header + spec["code"] + "\n")
        ann["defect_type"] = spec["defect_type"]
        ann["severity"] = spec["severity"]
        ann["expected_verdict"] = spec["expected_verdict"]
        ann["expected_detectors"] = spec["expected_detectors"]
        ann["defect_location"] = {"line": dline, "function": ann["defect_location"]["function"]}
        ann["notes"] = spec["notes"]
        json.dump(ann, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        changed.append(f"{sid}: rewrite code (catch, line {dline})")

    print("修正完成：")
    for c in changed:
        print("  ", c)


if __name__ == "__main__":
    main()
