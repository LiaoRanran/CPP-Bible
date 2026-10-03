# -*- coding: utf-8 -*-
"""676c-G 验证驱动: Task B (编译门) + Task C (检测器复现)。
环境: WSL_UTF8=1 + WSLENV=WSL_UTF8/u (防 UTF-16LE 横幅污染, 见 AGENT 纪律)。
检测器: tools/holdout_reveal_661.py 零修改, 仅运行时 monkeypatch ATOMS。
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))      # 仓库根 (HERE 的上两级)
TOOLS = os.path.join(ROOT, "tools")
WSL_DIR = "/mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/expansion_676c_G"

os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"
PY = sys.executable

def wsl(cmd, timeout=150):
    r = subprocess.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True,
                       text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def local(cmd, timeout=90):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

manifest = json.load(open(os.path.join(HERE, "_manifest.json"), encoding="utf-8"))
samples = manifest["samples"]
only = set(sys.argv[1:]) if len(sys.argv) > 1 else None

results = {}
out_path = os.path.join(HERE, "verify_results.json")
if os.path.exists(out_path):
    results = json.load(open(out_path, encoding="utf-8"))

t0 = time.time()
for sid in samples:
    if only and sid not in only:
        continue
    name = "sample_" + sid
    cpp = os.path.join(HERE, name + ".cpp")
    meta = json.load(open(os.path.join(HERE, name + ".json"), encoding="utf-8"))
    if sid in results and results[sid].get("done"):
        continue

    rec = {"sample_id": name, "expected": meta["expected_verdict"],
           "detectors": meta["expected_detectors"], "done": False}

    # ---- Task B-1: 本地 MinGW 语法校验 ----
    rc, out = local(["g++", "-std=c++17", "-fsyntax-only", cpp])
    rec["syntax_mingw"] = "PASS" if rc == 0 else "FAIL:" + out.strip()[:200]

    if rc == 0:
        # ---- Task B-2: WSL 完整编译 (asan+ubsan; tsan 样本另跑 tsan) ----
        sans = ["address,undefined"]
        if "tsan" in meta["expected_detectors"]:
            sans.append("thread")
        comp_ok = True
        for san in sans:
            rc, out = wsl(f"cd {WSL_DIR} && g++ -std=c++17 -O0 -g -fsanitize={san} -pthread "
                          f"{name}.cpp -o /tmp/{name}_{san[:3]}.bin 2>&1 | head -5")
            ok = rc == 0 and "error" not in out.lower()
            rec[f"wsl_compile_{san[:3]}"] = "PASS" if ok else "FAIL:" + out.strip()[:200]
            comp_ok = comp_ok and ok
        # ---- Task B-3: WSL 运行 (timeout 10) ----
        if comp_ok:
            rc, out = wsl(f"cd {WSL_DIR} && timeout 10 /tmp/{name}_add.bin 2>&1 | tail -3; "
                          f"exit ${{PIPESTATUS[0]}}", timeout=60)
            rec["run_exit"] = rc
            rec["run_note"] = out.strip()[:150]
        else:
            rec["run_exit"] = None

        # ---- Task C: 检测器复现 (monkeypatch ATOMS, 零修改 detect()) ----
        sys.path.insert(0, TOOLS)
        import holdout_reveal_661 as hr
        hr.ATOMS = HERE
        verdicts = {}
        for kind in meta["expected_detectors"]:
            v, note = hr.detect(kind, [name + ".cpp"])
            if v == "unknown":                     # 环境抖动重试一次
                time.sleep(2)
                v, note = hr.detect(kind, [name + ".cpp"])
            verdicts[kind] = {"verdict": v, "note": note[:160]}
        rec["pooled_verdict"] = verdicts
        rec["match"] = all(vd["verdict"] == rec["expected"] for vd in verdicts.values())
    rec["done"] = True
    results[sid] = rec
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"[{sid}] syntax={rec['syntax_mingw'][:30]} run_exit={rec.get('run_exit')} "
          f"verdicts={ {k: v['verdict'] for k, v in rec.get('pooled_verdict', {}).items()} } "
          f"match={rec.get('match')} elapsed={int(time.time()-t0)}s", flush=True)

# 汇总
ok = sum(1 for r in results.values() if r.get("done") and r.get("match"))
done = sum(1 for r in results.values() if r.get("done"))
print(f"\nSUMMARY: done={done}/{len(samples)} match={ok}/{done}")
