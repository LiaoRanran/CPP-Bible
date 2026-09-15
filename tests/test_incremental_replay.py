"""增量 replay 回归锁（498 任务 5 / P0-1）。

选卡规则（逐条对应 498 §任务5 step3）：新卡 ⇒ 跑；指纹变 ⇒ 跑；指纹同 + confirm ⇒ skip；
上次非 confirm ⇒ 跑；指纹 MISSING ⇒ 跑。另锁 `card_fingerprint` 对 fixture/artifact 变化敏感、
清单更新会移除已删卡。**全走纯函数与 tmp_path**（不跑真编译）。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import atom_evidence_replay as rp


def _run(cards, manifest, fp_of):
    return rp.select_incremental(cards, manifest, calc=lambda c: fp_of[c.name])


def test_no_manifest_all_selected(tmp_path: Path):
    cards = [tmp_path / "EV-A.md", tmp_path / "EV-B.md"]
    to_run, to_skip = _run(cards, {}, {"EV-A.md": "f1", "EV-B.md": "f2"})
    assert to_run == cards and to_skip == []


def test_unchanged_confirm_skipped(tmp_path: Path):
    c = tmp_path / "EV-A.md"
    m = {rp._manifest_key(c): {"fingerprint": "f1", "verdict": "confirm"}}
    to_run, to_skip = _run([c], m, {"EV-A.md": "f1"})
    assert to_run == [] and to_skip == [c]


def test_changed_fingerprint_selected(tmp_path: Path):
    """夹具/工件/卡任一改动 ⇒ 指纹变 ⇒ 必须重跑。"""
    c = tmp_path / "EV-A.md"
    m = {rp._manifest_key(c): {"fingerprint": "OLD", "verdict": "confirm"}}
    to_run, to_skip = _run([c], m, {"EV-A.md": "NEW"})
    assert to_run == [c] and to_skip == []


def test_new_card_selected(tmp_path: Path):
    """清单里没有的卡（新卡）⇒ 跑，即使别的卡都命中。"""
    old, new = tmp_path / "EV-A.md", tmp_path / "EV-B.md"
    m = {rp._manifest_key(old): {"fingerprint": "f1", "verdict": "confirm"}}
    to_run, to_skip = _run([old, new], m, {"EV-A.md": "f1", "EV-B.md": "f2"})
    assert to_run == [new] and to_skip == [old]


def test_last_refute_selected(tmp_path: Path):
    """指纹未变但上次非 confirm ⇒ 重跑（失败卡每次重试，不静默沿用失败）。"""
    c = tmp_path / "EV-A.md"
    m = {rp._manifest_key(c): {"fingerprint": "f1", "verdict": "refute:run_mismatch"}}
    to_run, to_skip = _run([c], m, {"EV-A.md": "f1"})
    assert to_run == [c] and to_skip == []


def test_missing_fingerprint_selected(tmp_path: Path):
    """指纹 MISSING（fixture/artifact 读不到）⇒ 强制重跑，不得沿用旧结论。"""
    c = tmp_path / "EV-A.md"
    m = {rp._manifest_key(c): {"fingerprint": "MISSING", "verdict": "confirm"}}
    to_run, to_skip = _run([c], m, {"EV-A.md": "MISSING"})
    assert to_run == [c] and to_skip == []


def test_card_fingerprint_sensitive_to_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """真实文件路径：改夹具内容 ⇒ 指纹变；三者都不动 ⇒ 指纹稳定。"""
    (tmp_path / "evidence").mkdir()
    card = tmp_path / "evidence" / "EV-X.md"
    fixt = tmp_path / "fx.cpp"
    art = tmp_path / "a.asm"
    fixt.write_text("int main(){}\n", encoding="utf-8")
    art.write_text("\tret\n", encoding="utf-8")
    card.write_text("---\nid: EV-X\nfixture: fx.cpp\nartifact: a.asm\n---\n", encoding="utf-8")
    fp1 = rp.card_fingerprint(card, calc_root=tmp_path)
    assert fp1 == rp.card_fingerprint(card, calc_root=tmp_path), "同内容指纹必须稳定"
    fixt.write_text("int main(){return 1;}\n", encoding="utf-8")
    assert rp.card_fingerprint(card, calc_root=tmp_path) != fp1, "改夹具必须改变指纹"
    art.unlink()
    assert rp.card_fingerprint(card, calc_root=tmp_path) == "MISSING", "工件缺失 ⇒ MISSING"


def test_card_fingerprint_sensitive_to_out_530(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """530 任务1：.out 读数（actual.run_match_file）须进指纹。

    - 改 .out 一行内容前后指纹必须不同；
    - 删掉 .out ⇒ 指纹变 "MISSING"（强制重跑，与 fixture/artifact 同语义）；
    - 不带 run_match_file 的卡，指纹不受本次改动影响（旧形态逐字节一致）。
    """
    (tmp_path / "evidence").mkdir()
    out = tmp_path / "r.out"
    out.write_text("A=1\nB=2\n", encoding="utf-8")
    # 旧形态：无 run_match_file，只有 fixture/artifact
    card_old = tmp_path / "evidence" / "EV-OLD.md"
    fixt = tmp_path / "fx.cpp"
    art = tmp_path / "a.asm"
    fixt.write_text("int main(){}\n", encoding="utf-8")
    art.write_text("\tret\n", encoding="utf-8")
    card_old.write_text("---\nid: EV-OLD\nfixture: fx.cpp\nartifact: a.asm\n---\n",
                        encoding="utf-8")
    fp_old = rp.card_fingerprint(card_old, calc_root=tmp_path)
    assert fp_old == rp.card_fingerprint(card_old, calc_root=tmp_path), "旧形态指纹稳定"
    # 新形态：带 run_match_file
    card_new = tmp_path / "evidence" / "EV-NEW.md"
    card_new.write_text(
        "---\nid: EV-NEW\nfixture: fx.cpp\nartifact: a.asm\n"
        "actual:\n  run_match_file: r.out\n---\n", encoding="utf-8")
    fp1 = rp.card_fingerprint(card_new, calc_root=tmp_path)
    assert fp1 == rp.card_fingerprint(card_new, calc_root=tmp_path), "新形态同 .out 指纹稳定"
    assert fp1 != fp_old, "带 run_match_file 的卡指纹必须与旧形态不同（.out 已纳入）"
    # 改 .out 一行
    out.write_text("A=99\nB=2\n", encoding="utf-8")
    assert rp.card_fingerprint(card_new, calc_root=tmp_path) != fp1, "改 .out 必须改变指纹"
    # 删 .out
    out.unlink()
    assert rp.card_fingerprint(card_new, calc_root=tmp_path) == "MISSING", "缺 .out ⇒ MISSING"


def test_card_fingerprint_ignores_undeclared_out_530(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """530 任务1：未声明 run_match_file 的卡 ⇒ .out 不参与指纹（旧行为逐字节一致）。

    旧形态（actual 为标量 run_* 或缺失）下 .out 从不进 hash；本改动只在新声明
    run_match_file 时才读取。故无 run_match_file 的卡，即便仓库里存在同名 .out，
    其内容变动也不应改变指纹。
    """
    (tmp_path / "evidence").mkdir()
    out = tmp_path / "r.out"
    out.write_text("A=1\n", encoding="utf-8")
    card = tmp_path / "evidence" / "EV-S.md"
    fixt = tmp_path / "fx.cpp"
    art = tmp_path / "a.asm"
    fixt.write_text("int main(){}\n", encoding="utf-8")
    art.write_text("\tret\n", encoding="utf-8")
    card.write_text("---\nid: EV-S\nfixture: fx.cpp\nartifact: a.asm\n---\n", encoding="utf-8")
    fp1 = rp.card_fingerprint(card, calc_root=tmp_path)
    assert fp1 == rp.card_fingerprint(card, calc_root=tmp_path), "无 run_match_file 卡指纹稳定"
    out.write_text("A=999\n", encoding="utf-8")  # 改未声明的 .out
    assert rp.card_fingerprint(card, calc_root=tmp_path) == fp1, "未声明 run_match_file ⇒ .out 不参与指纹"


def test_update_manifest_keeps_skip_drops_deleted(tmp_path: Path,
                                                  monkeypatch: pytest.MonkeyPatch):
    """清单更新：本次实跑卡被记录；未跑的（skip）保留；文件已删的卡被移除。"""
    monkeypatch.setattr(rp, "ROOT", tmp_path)
    (tmp_path / "evidence").mkdir()
    kept = tmp_path / "evidence" / "EV-KEEP.md"
    gone = tmp_path / "evidence" / "EV-GONE.md"
    kept.write_text("---\nid: EV-KEEP\n---\n", encoding="utf-8")
    manifest = {
        rp._manifest_key(kept): {"fingerprint": "old", "verdict": "confirm"},
        rp._manifest_key(gone): {"fingerprint": "x", "verdict": "confirm"},   # 文件不存在
    }
    out = rp.update_manifest(manifest, [(kept, "refute:x")])
    assert rp._manifest_key(gone) not in out, "已删卡必须移除"
    assert out[rp._manifest_key(kept)]["verdict"] == "refute:x"
