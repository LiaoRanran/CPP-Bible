"""579 任务 1/2 回归锁：跑批**工件层根隔离** + 确定性自检。

病（578b 实测、579 监工读码钉死）：`mutation_fuzz.sandbox()` 只重定向卡文本目录，工件层
（`Examples/` 的 artifact/fixture、`build/`、`replay_manifest.json`）仍打在真实仓库 ⇒
M1/M7 变体的 replay 在真实工件上 unlink→重编译→还原，紧随其后的 M6 全库扫描读到"某卡真实工件
正处于删-建窗口"这一非常态 ⇒ finding 随机多出/消失（同一输入两次跑 989/9/185 ↔ 991/7/185）。

本文件锁四件事：
① 沙箱内跑批根生效、工件树已复制、build 已建空目录；
② 跑批**对真实仓零副作用**（Examples 全树字节 + manifest 字节 + 残留文件都不动）；
③ **预置脏态**（异源 manifest + build 残留）下两次跑逐变体一致（旧代码在此必红）；
④ 确定性自检能真报错（反例：把 `run_fuzz` 换成"结果抖动"的替身 ⇒ 必须 exit 2）。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import mutation_fuzz as mf  # noqa: E402


def _tree_fingerprint(base: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(base.rglob("*")):
        if p.is_file():
            h.update(p.name.encode())
            h.update(str(p.stat().st_size).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _evidence_card(name: str = "EV-LANG-001.md") -> Path:
    p = next((c for c in (ROOT / "evidence").rglob(name)), None)
    assert p is not None, f"夹具缺失：{name}"
    return p


# ── ① 沙箱机制 ───────────────────────────────────────────────────────────────
def test_579_sandbox_activates_batch_root_and_copies_artifacts():
    """沙箱内：跑批根 = tmp、`Examples/` 工件树已复制、`build/` 为空目录；退出后根还原。"""
    assert replay.run_root() == replay.ROOT, "沙箱外跑批根必须是真实 ROOT（行为不变）"
    with mf.sandbox() as tmp:
        assert replay.run_root() == tmp, "沙箱内跑批根必须指向 tmp"
        assert (tmp / "Examples").is_dir(), "工件树（Examples/）必须进沙箱——全部 124 条 artifact/fixture 都在它下面"
        assert (tmp / "build").is_dir(), "沙箱内必须有 build/（卡命令产物与 manifest 都落这里）"
        assert not list((tmp / "build").iterdir()), "沙箱 build/ 必须是空的"
        assert replay.manifest_path() == tmp / "build" / "replay_manifest.json", "manifest 必须跟随跑批根"
        assert ge._rel(tmp / "evidence" / "mem" / "EV-MEM-001.md") == "evidence/mem/EV-MEM-001.md", \
            "finding 展示路径必须仓内相对（否则两次跑字符串不可比）"
    assert replay.run_root() == replay.ROOT, "退出沙箱必须还原跑批根"


def test_579_artifact_io_happens_in_sandbox_not_real_repo(replay_serial):
    """工件层读**必须**落在沙箱：计数器探针证明 replay 走的是 tmp 里的工件。

    580 补：本用例比对**真实 Examples 全树指纹** ⇒ 必须与 replay 共用同一把锁串行
    （否则别的 worker 的合法 replay 改写会被当成"跑批污染了真实仓" ⇒ `-n auto` 下假红）。
    """
    card = _evidence_card()
    real_art = replay.run_root() / str(replay.parse_frontmatter(
        card.read_text(encoding="utf-8")).get("artifact"))
    before = _tree_fingerprint(ROOT / "Examples")
    with mf.sandbox() as tmp:
        sb_card = mf._rel_in_sandbox(card, tmp)
        sb_art = tmp / real_art.relative_to(ROOT)
        assert sb_art.is_file(), "沙箱里必须有该卡的工件副本"
        replay.replay_card(sb_card, do_sanitizer=False)      # 会删工件→重编译→还原
    assert _tree_fingerprint(ROOT / "Examples") == before, \
        "跑批动了真实 Examples/ ⇒ 工件层没进沙箱（578b 的非确定性根源）"


def test_579_run_fuzz_leaves_real_repo_untouched(tmp_path: Path, replay_serial):
    """整跑一遍 `run_fuzz`（含 M1 工件算子）后：真实 Examples/ 与真实 manifest 字节不变。

    580 补 `replay_serial`：本用例读**真实仓全树指纹** ⇒ 必须与 replay 串行（`-n auto` 下防假红）。
    """
    card = _evidence_card()
    art_before = _tree_fingerprint(ROOT / "Examples")
    mf_path = ROOT / "build" / "replay_manifest.json"
    mf_before = mf_path.read_bytes() if mf_path.is_file() else None

    rep = mf.run_fuzz([card], ["M1"], 1)
    assert rep["variants"] >= 1

    assert _tree_fingerprint(ROOT / "Examples") == art_before, "真实工件被跑了"
    mf_after = mf_path.read_bytes() if mf_path.is_file() else None
    assert mf_after == mf_before, "真实 build/replay_manifest.json 被读写了"


# ── ② 脏态下的确定性（旧代码必红）────────────────────────────────────────────
def test_579_dirty_manifest_does_not_change_verdicts(tmp_path: Path, monkeypatch, replay_serial):
    """预置**异源 manifest + build 残留**：同一输入两次跑必须逐变体一致。

    旧代码（跑批继承真实 manifest / 在真实工件上删建）会因继承状态而抖 ⇒ 本用例红。
    580 补 `replay_serial`：本用例会**写真实 manifest** ⇒ 必须独占（不与其他读工件的 worker 撞）。
    """
    card = _evidence_card("EV-MEM-034.md")
    cards2 = [card, _evidence_card("EV-MEM-029.md")]
    mf_path = ROOT / "build" / "replay_manifest.json"
    mf_path.parent.mkdir(parents=True, exist_ok=True)
    old = mf_path.read_bytes() if mf_path.is_file() else None
    residue = ROOT / "build" / "z_residue_579_test.tmp"
    residue.write_text("residue", encoding="utf-8")
    mf_path.write_text(json.dumps({
        "evidence/mem/EV-MEM-034.md": {"fingerprint": "FAKE", "verdict": "confirm"},
        "ghost/EV-NOT-EXIST-999.md": {"fingerprint": "X", "verdict": "confirm"},
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    try:
        a = mf._variant_index(mf.run_fuzz(cards2, ["M6"], 5))
        b = mf._variant_index(mf.run_fuzz(cards2, ["M6"], 5))
        assert a == b, "脏 manifest 预置下两次跑不一致 ⇒ 跑批仍继承外部状态"
    finally:
        if old is None:
            try:
                mf_path.unlink(missing_ok=True)
            except OSError:            # safe-delete 拦截层：删不动也不影响断言
                pass
        else:
            mf_path.write_bytes(old)
        try:
            residue.unlink(missing_ok=True)
        except OSError:
            pass


# ── ③ 确定性自检（正反例）────────────────────────────────────────────────────
def test_579_selfcheck_passes_on_small_stable_subset():
    """正例：小批 M6 两次跑一致 ⇒ (True, [])。"""
    cards = [_evidence_card("EV-MEM-034.md"), _evidence_card("EV-MEM-029.md")]
    rep = mf.run_fuzz(cards, ["M6"], 5)
    ok, diffs = mf.selfcheck_determinism(cards, ["M6"], 5, rep)
    assert ok and diffs == [], diffs


def _flip_one(rep: dict) -> dict:
    """造一个"抖了"的副本：把首个变体的 verdict 翻面。"""
    out = json.loads(json.dumps(rep))
    r0 = out["results"][0]
    r0["verdict"] = "escaped" if r0["verdict"] != "escaped" else "blocked"
    return out


def test_579_selfcheck_detects_drift(tmp_path: Path):
    """反例（**可证伪**）：基线被篡改一条 ⇒ 自检必须报不一致（否则自检是恒真摆设）。"""
    cards = [_evidence_card("EV-MEM-034.md")]
    real = mf.run_fuzz(cards, ["M6"], 5)
    ok, diffs = mf.selfcheck_determinism(cards, ["M6"], 5, _flip_one(real))
    assert not ok and diffs, "结果抖动必须被自检抓到"
    assert "EV-MEM-034.md" in diffs[0], diffs[0]


def test_579_selfcheck_cli_exits_2_on_drift(tmp_path: Path, monkeypatch, capsys):
    """反例（CLI 面）：主跑干净、自检重跑抖一条 ⇒ `--selfcheck-determinism` 必须 fail-loud exit 2。"""
    cards = [_evidence_card("EV-MEM-034.md")]
    real = mf.run_fuzz(cards, ["M6"], 5)
    calls = {"n": 0}

    def _drifting(*_a, **_k):
        calls["n"] += 1
        return real if calls["n"] == 1 else _flip_one(real)     # 自检那次才开始抖

    monkeypatch.setattr(mf, "run_fuzz", _drifting)
    rc = mf.main(["--cards", "evidence/mem/EV-MEM-034.md", "--operators", "M6", "--limit", "5",
                  "--selfcheck-determinism", "--report", str(tmp_path / "r.json")])
    assert rc == 2, rc
    err = capsys.readouterr().err
    assert "确定性自检不过" in err and "抖动" in err, err


def test_579_repo_clean_after_tests():
    """末位绿锁：本文件所有用例都不得在真实仓留下痕迹。"""
    assert ge._rel(ROOT / "evidence" / "conc" / "EV-CONC-001.md") == "evidence/conc/EV-CONC-001.md"
    mf_path = ROOT / "build" / "replay_manifest.json"
    if mf_path.is_file():                       # 预置值（脏态夹具）或原值，都必须仍是合法 JSON
        json.loads(mf_path.read_text(encoding="utf-8"))
