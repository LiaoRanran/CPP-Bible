#!/usr/bin/env python3
"""616 D2 · 独立复核原型（**最小可行版本**：EV-MATRIX 独立复核 + HMAC VSA 凭证）。

做什么：
  1. 对一张证据卡，用**独立实现**（`ev_matrix_unbacked_v2.py`，不 import/copy `gate_engine`）复核
     `EV-MATRIX-UNBACKED`，产出 **VSA 验证凭证**（JSON：验证者 ID / 时间 / 结果 / 输入哈希 / 签名）；
  2. 用 **HMAC-SHA256** 签名（密钥取环境变量 `CPPBIBLE_VSA_KEY`，**缺省用测试密钥——非生产**）；
  3. `--verify` 验证凭证真实性（重算签名 + 校验输入哈希）；篡改后验证失败。

CLI：`--make <card>`（生成凭证）/ `--verify <vsa.json>` / `--samples`（对 3–5 张卡生成示例）/
      `--check`（原型逻辑自验证）。
铁律：原型非生产；HMAC 测试密钥；不改任何现有工具；不自动接受任何判决（人审权力）。
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402

KEY_ENV = "CPPBIBLE_VSA_KEY"
DEFAULT_KEY = b"cppbible-616-test-key-NOT-FOR-PRODUCTION"
SAMPLES = ROOT / "data" / "independent_verifier_samples_616"
VERIFIER_ID = "ev_matrix_unbacked_v2"
SAMPLE_CARDS = ["evidence/conc/EV-CONC-001.md", "evidence/conc/EV-CONC-002.md",
                "evidence/mem/EV-MEM-001.md", "evidence/hist/EV-HIST-001.md",
                "evidence/lang/EV-LANG-001.md"]


def _key() -> bytes:
    env = os.environ.get(KEY_ENV, "")
    return env.encode("utf-8") if env else DEFAULT_KEY


def _keyid(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()[:16]


def _payload(vsa: dict) -> bytes:
    """签名载荷 = VSA 去掉 `signature` 字段后的 canonical JSON。"""
    body = {k: v for k, v in vsa.items() if k != "signature"}
    return json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sign(vsa: dict, key: bytes) -> str:
    return hmac.new(key, _payload(vsa), hashlib.sha256).hexdigest()


def make_vsa(card_rel: str, key: bytes | None = None) -> dict:
    """对一张卡生成 VSA 凭证。"""
    k = key or _key()
    p = ROOT / card_rel
    if not p.is_file():
        raise FileNotFoundError(card_rel)
    text = p.read_text(encoding="utf-8", errors="replace")
    j = v2.judge(text, strip_sha=True)
    verdict = j["verdict"] if j else "NOT_APPLICABLE"
    vsa: dict[str, Any] = {
        "vsa_version": "1.0",
        "verifier_id": VERIFIER_ID,
        "verified_at": datetime.now().isoformat(timespec="seconds"),
        "input": {"path": card_rel, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()},
        "result": {"rule": "EV-MATRIX-UNBACKED", "verdict": verdict,
                   "anchors": (j or {}).get("anchors")},
        "signature": {"scheme": "hmac-sha256", "keyid": _keyid(k)},
    }
    vsa["signature"]["sig"] = _sign(vsa, k)
    return vsa


def verify_vsa(vsa: dict, key: bytes | None = None) -> tuple[bool, str]:
    """验证凭证：签名一致 **且** 输入哈希与当前卡内容一致。"""
    k = key or _key()
    sig = (vsa.get("signature") or {}).get("sig")
    if not sig:
        return False, "缺签名"
    if (vsa.get("signature") or {}).get("keyid") != _keyid(k):
        return False, "keyid 不匹配（密钥不同）"
    expect = _sign(vsa, k)
    if not hmac.compare_digest(str(sig), expect):
        return False, "签名不符（凭证被篡改）"
    rel = str((vsa.get("input") or {}).get("path") or "")
    p = ROOT / rel
    if p.is_file():
        cur = hashlib.sha256(p.read_text(encoding="utf-8", errors="replace").encode("utf-8")).hexdigest()
        if cur != (vsa.get("input") or {}).get("sha256"):
            return False, "输入哈希不符（卡已变更）"
    return True, "ok"


def write_samples() -> int:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    n = 0
    for rel in SAMPLE_CARDS:
        if not (ROOT / rel).is_file():
            continue
        vsa = make_vsa(rel)
        out = SAMPLES / (Path(rel).stem + ".vsa.json")
        out.write_text(json.dumps(vsa, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        n += 1
    return n


def check() -> list[str]:
    problems: list[str] = []
    rel = SAMPLE_CARDS[0]
    if not (ROOT / rel).is_file():
        return [f"示例卡不存在：{rel}"]
    vsa = make_vsa(rel)
    ok, why = verify_vsa(vsa)
    if not ok:
        problems.append(f"合法凭证应验证通过（{why}）")
    # 篡改检测
    tampered = json.loads(json.dumps(vsa))
    tampered["result"]["verdict"] = "BACKED" if vsa["result"]["verdict"] != "BACKED" else "UNBACKED"
    ok2, _ = verify_vsa(tampered)
    if ok2:
        problems.append("篡改后的凭证不应验证通过")
    # 换密钥应失败
    ok3, _ = verify_vsa(vsa, key=b"another-key")
    if ok3:
        problems.append("用错密钥不应验证通过")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="independent_verifier_prototype",
                                 description="616 D2 独立复核原型（HMAC VSA 凭证）")
    ap.add_argument("--make", default=None, help="对指定卡生成凭证（打印 JSON）")
    ap.add_argument("--verify", default=None, help="验证凭证文件")
    ap.add_argument("--samples", action="store_true", help="对 3-5 张卡生成示例凭证")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[D2] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[D2] ✅ 原型自验证通过：生成/签名验证/篡改检测/换密钥检测（keyid {_keyid(_key())}）")
        return 0
    if a.make:
        print(json.dumps(make_vsa(a.make), ensure_ascii=False, indent=1))
        return 0
    if a.verify:
        vsa = cast("dict[str, Any]", json.loads(Path(a.verify).read_text(encoding="utf-8")))
        ok, why = verify_vsa(vsa)
        print(f"[D2] {'✅ 凭证有效' if ok else '❌ 凭证无效'}：{why}")
        return 0 if ok else 1
    if a.samples:
        n = write_samples()
        print(f"[D2] 已写 {n} 份示例凭证 → {SAMPLES.relative_to(ROOT).as_posix()}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
