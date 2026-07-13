#!/usr/bin/env python3
"""snapshot.py — 质量快照管理

用法:
  python3 tools/snapshot.py save              → 保存快照到 build/snapshots/
  python3 tools/snapshot.py list              → 列出所有快照
  python3 tools/snapshot.py compare S1 S2     → 对比两个快照

快照包含: 门禁分数、扩张审计数据、代码质量指标
"""
import json, pathlib, subprocess, sys, time
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYTHON = r"C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"
SNAPDIR = ROOT / "build" / "snapshots"


def save():
    SNAPDIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap = {"timestamp": datetime.now().isoformat(), "ts_short": ts}

    # expansion audit
    r = subprocess.run([PYTHON, str(ROOT/"tools"/"expansion_audit.py"), "--json"],
                       capture_output=True, text=True, timeout=60, cwd=str(ROOT))
    exp = json.loads(r.stdout)

    snap["total_shallow"] = sum(c["shallow_blocks"] for c in exp)
    snap["total_self"] = sum(c["self_contained"] for c in exp)
    snap["total_blocks"] = sum(c["cpp_blocks"] for c in exp)
    snap["total_tilde"] = sum(c["tilde_claims"] for c in exp)
    snap["zero_ind"] = sum(1 for c in exp if c["industry_refs"] == 0)
    snap["total_deep"] = sum(c["deep_blocks"] for c in exp)
    snap["chapters"] = len(exp)
    snap["self_pct"] = round(100 * snap["total_self"] / max(1, snap["total_blocks"]), 1)
    snap["shallow_pct"] = round(100 * snap["total_shallow"] / max(1, snap["total_blocks"]), 1)
    snap["exp_data"] = exp

    # gate
    r2 = subprocess.run([PYTHON, str(ROOT/"tools"/"consistency_check.py")],
                        capture_output=True, text=True, timeout=30, cwd=str(ROOT))
    snap["gate_ok"] = "ERROR=0 WARN=0" in r2.stdout and "100/100" in r2.stdout

    outpath = SNAPDIR / f"snap_{ts}.json"
    outpath.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ 快照已保存: {outpath.name}")
    print(f"     浅块={snap['total_shallow']}({snap['shallow_pct']}%)  自含={snap['total_self']}({snap['self_pct']}%)")
    print(f"     估算={snap['total_tilde']}  零工业={snap['zero_ind']}/{snap['chapters']}")
    print(f"     门禁={'PASS' if snap['gate_ok'] else 'FAIL'}")


def list_snapshots():
    if not SNAPDIR.exists():
        print("  无快照")
        return
    snaps = sorted(SNAPDIR.glob("snap_*.json"))
    if not snaps:
        print("  无快照")
        return
    print(f"\n  {'快照':<24} {'浅块%':>6} {'自含%':>6} {'估算':>5} {'零工业':>7} {'门禁':>5}")
    print(f"  {'─'*24} {'─'*6} {'─'*6} {'─'*5} {'─'*7} {'─'*5}")
    for sp in snaps:
        s = json.loads(sp.read_text(encoding="utf-8"))
        print(f"  {sp.stem:<24} {s['shallow_pct']:>5.1f}% {s['self_pct']:>5.1f}% {s['total_tilde']:>5} {s['zero_ind']:>4}/{s['chapters']:<2} {'✅' if s['gate_ok'] else '❌':>4}")
    print()


def compare(s1_name: str, s2_name: str):
    f1 = SNAPDIR / f"{s1_name}.json" if not s1_name.endswith(".json") else SNAPDIR / s1_name
    f2 = SNAPDIR / f"{s2_name}.json" if not s2_name.endswith(".json") else SNAPDIR / s2_name
    if not f1.exists():
        print(f"  快照 '{s1_name}' 不存在"); return
    if not f2.exists():
        print(f"  快照 '{s2_name}' 不存在"); return

    a = json.loads(f1.read_text(encoding="utf-8"))
    b = json.loads(f2.read_text(encoding="utf-8"))

    def delta(key, flip=False):
        d = b[key] - a[key]
        if d == 0: return "—"
        good = d < 0 if flip else d > 0
        arrow = "↑" if d > 0 else "↓"
        return f"{arrow}{abs(d)} {'✅' if good else '⚠️'}"

    print(f"\n  对比: {f1.stem} → {f2.stem}")
    print(f"  {'指标':<12} {'旧':>8} {'新':>8} {'变化':>10}")
    print(f"  {'─'*12} {'─'*8} {'─'*8} {'─'*10}")
    print(f"  {'浅块':<12} {a['total_shallow']:>8} {b['total_shallow']:>8} {delta('total_shallow', flip=True):>10}")
    print(f"  {'自含':<12} {a['total_self']:>8} {b['total_self']:>8} {delta('total_self'):>10}")
    print(f"  {'深块':<12} {a['total_deep']:>8} {b['total_deep']:>8} {delta('total_deep'):>10}")
    print(f"  {'估算':<12} {a['total_tilde']:>8} {b['total_tilde']:>8} {delta('total_tilde', flip=True):>10}")
    print(f"  {'零工业':<12} {a['zero_ind']:>8} {b['zero_ind']:>8} {delta('zero_ind', flip=True):>10}")
    print()

    # Per-chapter detail for big changes
    a_exp = {c["stem"]: c for c in a["exp_data"]}
    b_exp = {c["stem"]: c for c in b["exp_data"]}
    big_deltas = []
    for stem in set(a_exp) & set(b_exp):
        ac = a_exp[stem]; bc = b_exp[stem]
        da = bc["scores"]["total"] - ac["scores"]["total"]
        if abs(da) >= 5:
            big_deltas.append((stem, da, ac["scores"]["total"], bc["scores"]["total"]))
    if big_deltas:
        big_deltas.sort(key=lambda x: -abs(x[1]))
        print(f"  显著变化章 (Δ≥5分):")
        for stem, da, old, new in big_deltas[:10]:
            arrow = "↑" if da > 0 else "↓"
            tag = "⚠️" if da < -5 else "✅"
            print(f"    {stem}: {old:.0f} → {new:.0f} ({arrow}{abs(da):.0f}) {tag}")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "save"
    if cmd == "save":
        save()
    elif cmd == "list":
        list_snapshots()
    elif cmd == "compare":
        if len(sys.argv) < 4:
            print("用法: python3 tools/snapshot.py compare snap_20260711_120000 snap_20260711_180000")
            return
        compare(sys.argv[2], sys.argv[3])
    else:
        print(f"未知命令: {cmd}")
        print("可用: save | list | compare S1 S2")


if __name__ == "__main__":
    main()
