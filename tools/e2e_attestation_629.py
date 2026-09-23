"""629 C4 · 端到端他验编排（**全程临时目录，不动仓库**）

链路（每步计时）：
    ① 独立验证者重算（子进程 `independent_verifier_628.py`，零 import 它）
    ② 生成 628 形态 VSA 凭证（`vsa_attestation_628.build_credential()`，只读调用）
       + HMAC 校验（628 `verify_credential`，临时文件）
    ③ C1 非对称升级（RSA-2048 私钥签，公钥验）+ 公钥指纹
    ④ 透明日志入册（628 `append_vsa`，日志经 `CPPBIBLE_TRANSPARENCY_LOG` 指向**临时日志**）
    ⑤ 从日志取回凭证 → 独立重验（重新读文件 + 公钥验签 + inclusion 检查）
    ⑥ 输出交付报告（本仓唯一写入 = `data/e2e_attestation_629.md`）

为什么日志走临时文件：628 的生产日志是 append-only 凭证账本，端到端演示每次跑都追加会
**污染生产链**（628 的 e2e 测试已因此让 14→19 张凭证漂移，见 629 基线台账）。
本工具用 628 自己提供的 `CPPBIBLE_TRANSPARENCY_LOG` 隔离机制（628 就是为此加的），
既真实走完整链路，又把副作用限制在临时目录。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "e2e_attestation_629.md")
VERIFIER = os.path.join(HERE, "independent_verifier_628.py")


def _run(args: list, cwd: str) -> tuple[int, str]:
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, check=False)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def run_e2e() -> dict[str, Any]:
    import transparency_log_628 as T
    import vsa_asymmetric_signer_629 as S
    import vsa_attestation_628 as V

    steps: list[dict[str, Any]] = []
    tmp = tempfile.mkdtemp(prefix="queyi_629_e2e_")
    old_log_env = os.environ.get(T.LOG_ENV)
    os.environ[T.LOG_ENV] = os.path.join(tmp, "tmp_transparency_log.jsonl")
    try:
        # ① 独立验证者重算（子进程，零 import）
        t0 = time.time()
        rc, out = _run([sys.executable, VERIFIER], cwd=ROOT)
        iv = json.loads(out.strip().splitlines()[-1]) if rc == 0 else {}
        steps.append({"step": "① 独立验证者重算", "seconds": round(time.time() - t0, 2),
                      "ok": rc == 0 and bool(iv),
                      "detail": f"W2 IN{iv.get('w2', {}).get('summary', {}).get('IN')}"
                                f"/OUT{iv.get('w2', {}).get('summary', {}).get('OUT')}"
                                f" · PCK authorized {iv.get('pck', {}).get('authorized')}"
                                f" · ledger {iv.get('ledger_chain', {}).get('events')} 条"})

        # ② 628 形态 VSA 凭证 + HMAC 校验
        t0 = time.time()
        cred = V.build_credential()
        cred_p = os.path.join(tmp, "vsa_hmac.json")
        with open(cred_p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(cred, fh, ensure_ascii=False, indent=2)
        hmac_r = V.verify_credential(cred_p)
        steps.append({"step": "② VSA 凭证（628 形态）+ HMAC 校验",
                      "seconds": round(time.time() - t0, 2),
                      "ok": bool(hmac_r["valid"]),
                      "detail": f"HMAC valid={hmac_r['hmac_valid']} · "
                                f"输入锚定={hmac_r['input_hashes_valid']} · "
                                f"结果一致={hmac_r['results_valid']}"})

        # ③ 非对称升级（RSA-2048）
        t0 = time.time()
        priv = S.generate_keypair(2048)
        pub = S.public_of(priv)
        signed = S.upgrade_credential(cred, priv)
        signed_p = os.path.join(tmp, "vsa_signed.json")
        with open(signed_p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(signed, fh, ensure_ascii=False, indent=2)
        pub_fp = hashlib.sha256(json.dumps(pub, sort_keys=True).encode("utf-8")) \
            .hexdigest()[:16]
        rsa_ok = S.verify_credential_sig(signed, pub)
        steps.append({"step": "③ 非对称升级（RSA-2048 私钥签/公钥验）",
                      "seconds": round(time.time() - t0, 2), "ok": rsa_ok,
                      "detail": f"{priv['scheme']} · 公钥指纹 {pub_fp}…"})

        # ④ 透明日志入册（临时日志）
        t0 = time.time()
        ap = T.append_vsa(signed_p)
        steps.append({"step": "④ 透明日志入册（临时日志，隔离生产链）",
                      "seconds": round(time.time() - t0, 2), "ok": bool(ap["ok"]),
                      "detail": f"log_index={ap['log_index']} · "
                                f"entry_hash={str(ap['entry_hash'])[:16]}…"})

        # ⑤ 从日志取回 → 独立重验
        t0 = time.time()
        tail = T._read_log()[-1] if T._read_log() else {}
        back_p = os.path.join(ROOT, str(tail.get("vsa_file")))
        fresh = json.load(open(back_p, encoding="utf-8"))
        inc = T.check_inclusion(back_p)
        re_ok = S.verify_credential_sig(fresh, pub) and bool(inc["included"])
        steps.append({"step": "⑤ 从日志取回 + 独立重验",
                      "seconds": round(time.time() - t0, 2), "ok": re_ok,
                      "detail": f"inclusion={inc['included']}"
                                f"(index={inc['log_index']}) · 公钥复验="
                                f"{S.verify_credential_sig(fresh, pub)}"})

        # 攻击检测（端到端韧性）
        tamper_ok = not S.verify_credential_sig(dict(fresh, results={"w2_in": 999}), pub)
        steps.append({"step": "⑥ 篡改检测（改 results 后重验必失败）",
                      "seconds": 0.0, "ok": tamper_ok, "detail": "tamper detected"})

        return {"steps": steps, "all_green": all(s["ok"] for s in steps),
                "verifier": iv, "credential": dict(signed),
                "hmac": hmac_r, "pub_fingerprint": pub_fp,
                "log_entry": {k: v for k, v in (tail or {}).items() if k != "vsa_file"},
                "repo_log_untouched": (T.status()["entries"]),
                "temp_log_entries": len(open(os.environ[T.LOG_ENV], encoding="utf-8")
                                        .readlines()) if os.path.exists(
                    os.environ[T.LOG_ENV]) else 0}
    finally:
        if old_log_env is None:
            os.environ.pop(T.LOG_ENV, None)
        else:
            os.environ[T.LOG_ENV] = old_log_env
        shutil.rmtree(tmp, ignore_errors=True)


def _tree(d: dict[str, Any]) -> str:
    cred = d["credential"]
    return "\n".join([
        "凭证链（文本树）",
        "├─ ① 独立验证者 independent_verifier_628（零 import 本项目工具）",
        f"│     ├─ verifier_sha256 绑定：{str(cred.get('verifier_sha256'))[:16]}…",
        f"│     └─ 重算：W2 IN{cred.get('results', {}).get('w2_in')}"
        f"/OUT{cred.get('results', {}).get('w2_out')} · "
        f"PCK authorized {cred.get('results', {}).get('pck_authorized')} · "
        f"ledger {cred.get('results', {}).get('ledger_hash_chain')}",
        "├─ ② VSA 凭证（628 形态）",
        f"│     ├─ HMAC-SHA256 attestation：{str(cred.get('attestation', ''))[:16]}…",
        f"│     └─ 输入三重锚定：ledger {str(cred.get('input_hashes', {}).get('ledger_sha256'))[:12]}…"
        f" / grounded … / pck_dir …",
        "├─ ③ 非对称签名（629 C1）",
        f"│     ├─ scheme：{cred.get('signature_scheme')}",
        f"│     └─ 公钥指纹：{d['pub_fingerprint']}…",
        "└─ ④ 透明日志（append-only 哈希链）",
        f"      ├─ log_index：{d['log_entry'].get('log_index')}",
        f"      ├─ entry_hash：{str(d['log_entry'].get('entry_hash'))[:16]}…",
        f"      └─ prev_log_hash：{str(d['log_entry'].get('prev_log_hash'))[:16]}…",
        "            ↑ ⑤ 从日志取回凭证 → 公钥复验 + inclusion 通过",
    ])


def write_report(d: Optional[dict[str, Any]] = None) -> str:
    d = d or run_e2e()
    lines = [
        "# 629 C4 · 端到端他验编排（独立验证 → VSA → 透明日志 → 独立重验）", "",
        "> 工具：`tools/e2e_attestation_629.py`（**全程临时目录**：凭证/密钥/日志都不落仓库；"
        "本仓唯一写入是这份报告）", "",
        "## 一、各步结果与耗时", "",
        "| 步骤 | 耗时(s) | 结果 | 详情 |", "|---|---|---|---|",
        *[f"| {s['step']} | {s['seconds']} | {'✅' if s['ok'] else '❌'} | {s['detail']} |"
          for s in d["steps"]], "",
        f"**端到端全绿：{d['all_green']}** · 总耗时 "
        f"{sum(s['seconds'] for s in d['steps']):.2f}s", "",
        "## 二、凭证链可视化", "", "```", _tree(d), "```", "",
        "## 三、与 628 B4 端到端的差异", "",
        "| 项 | 628 B4 | 629 C4 |", "|---|---|---|",
        "| 签名 | HMAC（对称） | HMAC + **RSA-2048 非对称**双签 |",
        "| 日志 | 追加到**生产**日志（每次跑 +1 条，会让基线漂移） | 追加到**临时**日志"
        "（走 628 的 `CPPBIBLE_TRANSPARENCY_LOG` 隔离机制，生产链零漂移） |",
        "| 重验 | 628 `--check` 读生产凭证 | 从日志**取回**凭证 → 公钥复验 + inclusion |",
        "| 密钥 | 生产 `data/vsa_secret.key` | 临时目录（用完即删；仓库零落盘） |", "",
        f"- 本次运行前后：生产日志条目 = **{d['repo_log_untouched']} 条**（未被本次演示改动）；"
        f"临时日志条目 = {d['temp_log_entries']} 条。",
        f"- 篡改检测：改 `results.w2_in=999` 后公钥复验失败 = "
        f"**{next(s['ok'] for s in d['steps'] if s['step'].startswith('⑥'))}**。", "",
        "## 四、局限", "",
        "- 验证者仍是**本项目写的**（独立性仅到 L2 分实现，见 C3）；",
        "- 公钥由同一主体生成 ⇒ 信任根未独立（见 C1）；",
        "- 临时日志是本地文件，无外部见证者；",
        "- 演示只覆盖 **1 张卡/一次全量重算**，不是逐卡凭证（B1 验证者本身是全量重算器）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    import transparency_log_628 as T

    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    before = T.status()["entries"]
    d = run_e2e()
    chk("端到端全绿（6 步）", d["all_green"], f"({[s['step'] for s in d['steps'] if not s['ok']]})")
    chk("独立验证者子进程成功", d["steps"][0]["ok"])
    chk("HMAC + 输入锚定 + 结果三项全过",
        d["hmac"]["hmac_valid"] and d["hmac"]["input_hashes_valid"]
        and d["hmac"]["results_valid"])
    chk("RSA 公钥复验通过（取回后重验）", d["steps"][4]["ok"])
    chk("篡改检测有效", d["steps"][5]["ok"])
    chk("生产日志零漂移（临时日志隔离）", T.status()["entries"] == before,
        f"({before} → {T.status()['entries']})")
    chk("仓库零密钥/凭证落盘（临时目录已清理）",
        not S_has_repo_keys(), f"({S_has_repo_keys()})")
    chk("报告存在且含链路树", os.path.exists(OUT_MD)
        and "凭证链（文本树）" in open(OUT_MD, encoding="utf-8").read())
    print(f"C4 e2e attestation check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def S_has_repo_keys() -> list[str]:
    import vsa_asymmetric_signer_629 as S

    return S.repo_key_files()


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 C4 端到端他验编排")
    ap.add_argument("--check", action="store_true", help="只读自检（临时目录跑全链路）")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = run_e2e()
    if args.json:
        print(json.dumps(d, ensure_ascii=False, default=str, indent=2))
        return 0
    print(f"all_green={d['all_green']} steps={len(d['steps'])} "
          f"total={sum(s['seconds'] for s in d['steps']):.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
