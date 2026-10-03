# -*- coding: utf-8 -*-
"""676c-G 构建器: 汇总 spec_partN.py → 生成 sample_GXXX.cpp/.json 并校验结构标记。"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load_parts():
    entries = []
    files = sorted(glob.glob(os.path.join(HERE, "spec_part*.py")),
                   key=lambda p: int(re.search(r"spec_part(\d+)", p).group(1)))
    for f in files:
        ns = {}
        with open(f, encoding="utf-8") as fh:
            exec(compile(fh.read(), f, "exec"), ns)
        for label, meta, cpp in ns["PART"]:
            entries.append((label, meta, cpp))
    return entries

def build():
    entries = load_parts()
    problems = []
    records = []
    for i, (label, meta, cpp) in enumerate(entries, start=1):
        sid = "G%03d" % i
        sample_id = "sample_" + sid
        src = meta["src"]
        header = (
            f"// {sample_id}\n"
            f"// defect_type: {meta['defect_type']}\n"
            f"// severity: {meta['severity']}\n"
            f"// planted: {str(bool(meta['planted'])).lower()}\n"
            f"// expected_verdict: {meta['verdict']}\n"
            f"// expected_detectors: {','.join(meta['detectors'])}\n"
            f"// source: {src['id']} ({src['url']}) [{src['project']}]\n"
            f"// (authoritative annotation in {sample_id}.json)\n"
        )
        final_cpp = header + cpp.strip("\n") + "\n"

        # 校验
        if "/* DEFECT */" not in final_cpp:
            problems.append(f"{sid}: 缺少 /* DEFECT */ 标记")
        if "int main(" not in final_cpp:
            problems.append(f"{sid}: 缺少 main 函数")
        n_lines = final_cpp.count("\n")
        if n_lines > 200:
            problems.append(f"{sid}: 行数 {n_lines} > 200")

        line = 0
        for no, ln in enumerate(final_cpp.split("\n"), start=1):
            if "/* DEFECT */" in ln:
                line = no
                break

        cpp_path = os.path.join(HERE, sample_id + ".cpp")
        with open(cpp_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(final_cpp)

        j = {
            "sample_id": sample_id,
            "defect_type": meta["defect_type"],
            "defect_location": {
                "line": line,
                "function": meta["func"],
                "description": meta["notes"],
            },
            "severity": meta["severity"],
            "planted": bool(meta["planted"]),
            "source": {
                "type": src["type"],
                "id": src["id"],
                "url": src["url"],
                "project": src["project"],
                "commit": src["commit"],
                "simplification": src["simplification"],
            },
            "expected_verdict": meta["verdict"],
            "expected_detectors": meta["detectors"],
            "trigger_condition": meta["trigger"],
            "notes": meta["notes"],
        }
        with open(os.path.join(HERE, sample_id + ".json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(j, fh, ensure_ascii=False, indent=2)
        records.append(sid)

    with open(os.path.join(HERE, "_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"samples": records, "problems": problems}, fh, ensure_ascii=False, indent=2)

    planted_false = sum(1 for sid in records
                        if json.load(open(os.path.join(HERE, "sample_" + sid + ".json"), encoding="utf-8"))["planted"] is False)
    print(f"generated={len(records)} planted_false={planted_false} planted_true={len(records)-planted_false}")
    print(f"problems={len(problems)}")
    for p in problems:
        print("  !!", p)
    return len(problems) == 0

if __name__ == "__main__":
    sys.exit(0 if build() else 1)
