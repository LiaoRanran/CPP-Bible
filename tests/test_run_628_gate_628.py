"""628 E1 · 收工门禁 单测（6 例）。

注意：**不能在 pytest 里直接跑完整门禁**（门禁第 4 步会再跑 pytest → 无限递归），
所以递归安全的部分用 `--no-tests`（跳过第 4 步，其余 13 步真实执行），
pytest 步骤本身由 `tools/run_628_gate.py --check`（CLI 完整调用）验证并记录于验收报告。
"""
import json
import os
import subprocess
import sys
import textwrap

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import run_628_gate as G


def test_gate_constants_declared():
    assert len(G.NEW_TOOLS) == 12, f"门禁应覆盖 12 个本批工具，实际 {len(G.NEW_TOOLS)}"
    assert len(G.CORE_TOOLS) == 5 and "gate_engine.py" in G.CORE_TOOLS
    assert G.EXPECT_W2 == {"IN": 114, "OUT": 7, "UNDEC": 0}
    assert G.BATCH_BASE == "b913b0fe"
    assert all(not t.startswith("tools/") for t in G.CORE_TOOLS)


def test_gate_w2_v1_v2_consistency():
    v1, v2s = G.w2_summary(False), G.w2_summary(True)
    assert v1["w2"] == G.EXPECT_W2, "V1 模式（默认）W2 应为冻结口径"
    assert v2s["w2"] == G.EXPECT_W2, "V2 模式 W2 应与 V1 数字一致"
    assert v1["v2_mode"] is False and v2s["v2_mode"] is True
    assert os.environ.get("QUEYI_AUTHORITY_V2") is None, "子进程不得改变父进程 flag"


def test_imports_of_static_analyzer(tmp_path):
    local = os.path.join(os.path.dirname(G.__file__), "transparency_log_628.py")
    f = tmp_path / "probe.py"
    f.write_text(textwrap.dedent("""
        import json
        import transparency_log_628
        from run_628_gate import _run
    """), encoding="utf-8")
    found = G.imports_of(str(f))
    assert set(found) == {"json", "transparency_log_628", "run_628_gate"}
    # 与门禁相同的判定口径：只看命中的本地模块
    local_hits = [m for m in found if m in G._local_modules()]
    assert set(local_hits) == {"transparency_log_628", "run_628_gate"}
    assert os.path.exists(local)


def test_gate_source_has_no_local_imports():
    hits = [m for m in G.imports_of(G.__file__) if m in G._local_modules()]
    assert hits == [], f"门禁自身必须零 import 本项目工具（{hits}）"


def test_gate_other_steps_pass():
    """除 pytest 步骤外的 13 步在门禁子进程里全绿（只读，零副作用）。"""
    p = subprocess.run([sys.executable, G.__file__, "--check", "--no-tests"],
                       cwd=G.ROOT, capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout[-500:]
    assert "PASS" in p.stdout and "FAIL" not in p.stdout


def test_acceptance_report_exists_and_complete():
    assert os.path.exists(G.ACCEPT_MD), "验收报告必须存在"
    md = open(G.ACCEPT_MD, encoding="utf-8").read()
    for kw in ("技术债", "他验三件套", "门禁", "偏差", "局限"):
        assert kw in md, f"验收报告缺少章节：{kw}"
    status = json.load(open(os.path.join(G.ROOT, "_auto", "status.json"),
                            encoding="utf-8"))
    assert (status["batch"] == 628 and status["state"] == "awaiting_review"
            and status["last_completed_batch"] == 628 and status["next_batch"] == 629)
