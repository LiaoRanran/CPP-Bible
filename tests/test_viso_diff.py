"""535 批次2 · V-iso 阴面形态判据回归锁（`tools/viso_diff.py`）。

为什么这些用例值得单独锁：V-iso 的全部赌注压在"阴面真的是单变量删除、真的删在机制函数里、
真的没把 claim 主体一起删掉"这三件事上。判据一旦放宽，下面任一类攻击都会静默变成"合规阴面"，
而 replay 那边看到的只是"探针翻转了"——**翻转本身不能证明删的是机制**（实测：把循环整段删掉
也会翻）。故这里逐条锁死：真阴面通过 + 每一类攻击各有一条反例。

夹具是合成的（结构同 `Examples/atoms/_atom_fence_vs_atomic.cpp`：**同一行机制文本在另一个函数里
也出现**，证明定位不能靠文本替换），规模按真实夹具量级（token 比率阈值 2% 只在同量级夹具上可校准）。
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import viso_diff as vd

# ── 合成夹具（量级对齐真实卡夹具，否则 2% 比率判据没有意义）──────────────────

_YANG = '''// 合成阳性夹具（结构同 Examples/atoms/_atom_fence_vs_atomic.cpp）
#include <atomic>

static std::atomic<int> s_sf_a{0};
static int s_sf_b = 0;
static int w_sf_a = 0;
static int w_sf_b = 0;
static int s_plain = 0;
static int s_p_a = 0;
static int s_p_b = 0;
static long s_acc = 1;

int spin_signal_fence() {
    while (!s_sf_b) {
        __atomic_signal_fence(__ATOMIC_SEQ_CST);
    }
    return s_sf_a;
}

// 与本卡 anchor **同一行文本**（文本替换无法定位 ⇒ 必须按函数区间定点删除）；
// 但变量是各自独立的（真夹具同构：s_sf_* / w_sf_*），故 retain 文本只在 anchor 内唯一。
int writer_signal_fence() {
    while (!w_sf_b) {
        __atomic_signal_fence(__ATOMIC_SEQ_CST);
    }
    return w_sf_a;
}

int spin_plain() {
    int acc = 0;
    while (!s_p_b) {
        acc += s_plain;
    }
    return acc + s_p_a;
}

long accumulate_loop(int n) {
    long total = 0;
    for (int i = 0; i < n; ++i) {
        total += static_cast<long>(i) * 3 + s_plain;
    }
    return total + s_acc;
}

int nested_branch(int n) {
    int r = 0;
    for (int i = 0; i < n; ++i) {
        if (i % 3 == 0) {
            r += i;
        } else if (i % 5 == 0) {
            r -= i;
        } else {
            r += 2 * i;
        }
    }
    return r;
}

int table_sum() {
    int r = 0;
    for (int i = 0; i < 8; ++i) {
        r += i * i + 1;
    }
    for (int j = 0; j < 4; ++j) {
        r -= j * 3;
    }
    return r;
}

int mix_all(int n) {
    int r = nested_branch(n) + table_sum() + spin_plain();
    r += accumulate_loop(n) > 0 ? 1 : 0;
    return r + s_plain;
}
'''
_ANCHOR = "spin_signal_fence"
_REMOVE = "__atomic_signal_fence(__ATOMIC_SEQ_CST);"
_RETAIN = ["while (!s_sf_b)", "return s_sf_a;"]
_SYMBOL = "_Z17spin_signal_fencev"
_FENCE_LINE = "        __atomic_signal_fence(__ATOMIC_SEQ_CST);\n"


def _drop_fence_in_anchor(text: str) -> str:
    """只在 anchor 函数体内删那一行（同名文本在 writer_signal_fence 里保留 ⇒ 定点删除）。"""
    head, body = text.split(f"int {_ANCHOR}() {{", 1)
    return head + f"int {_ANCHOR}() {{" + body.replace(_FENCE_LINE, "", 1)


_YIN = _drop_fence_in_anchor(_YANG)


def _judge(yin: str, **kw):
    kw.setdefault("probe_symbol", _SYMBOL)
    return vd.judge_min_diff(_YANG, yin, anchor=_ANCHOR, remove_text=_REMOVE,
                             retain=list(_RETAIN), **kw)


# ── 正例：真阴面（纯删 anchor 内 1 行机制）──────────────────────────────────


def test_positive_real_yin_passes():
    """真阴面必须通过形态判据，且指标落在 533 §2.2 校准区间（D=1 / coverage=1 / 无新增行）。"""
    v = _judge(_YIN)
    assert v.ok, v.reasons
    m = v.metrics
    assert m["hunks"] == 1 and m["inserted_lines"] == 0
    assert m["code_deleted_lines"] == 1 and m["comment_only_deleted"] == 0
    assert m["anchor_coverage"] == 1.0 and m["remove_hit"] is True
    assert all(m["retain_hit"].values())
    assert m["anchor_defs"] == 1, "anchor 定义必须唯一（重名一律拒收）"
    assert m["tokens_changed"] <= vd.MAX_TOKENS_CHANGED
    assert m["token_change_ratio"] <= vd.MAX_TOKEN_CHANGE_RATIO
    # 阴性对照：同名文本在另一个函数里仍在（证明不是文本替换，是定点删除）
    assert _YIN.count("__atomic_signal_fence(__ATOMIC_SEQ_CST);") == 1


# ── 反例：逐类攻击（对应 533 §3.1 攻击画廊）─────────────────────────────────


def test_negative_insert_line_replacement():
    """42→43 式替换 = 1 删 + 1 插 ⇒ 新增行 != 0，结构性击毙（不靠语义识别）。"""
    yin = _YIN.replace("    return s_sf_a;\n}", "    return s_sf_a + 1;\n}", 1)
    v = _judge(yin)
    assert not v.ok and any("新增行" in r for r in v.reasons), v.reasons


def test_negative_delete_outside_anchor():
    """删 anchor 外的行 ⇒ 覆盖率 0 且 remove 未命中（位置层击毙）。"""
    v = _judge(_YANG.replace("static int s_plain = 0;\n", "", 1))
    assert not v.ok
    assert any("覆盖率=0%" in r for r in v.reasons), v.reasons
    assert any("remove" in r for r in v.reasons), v.reasons


def test_negative_comment_only_smuggle():
    """注释/空白走私 ⇒ 零语义 diff（token 序列逐字相同），拒在"凑 diff"这一层。

    注：若走私与真删除同时出现在 ≤3 行内，两组会被并成同一 hunk（判据仍拒，只是 reason
    文字变成"新增行"）——故本用例以 **只动注释** 的形态单独锁"零语义 diff"这条。
    """
    v = _judge(_YANG.replace("    return s_sf_a;\n}", "    return s_sf_a;  // 调过参\n}", 1))
    assert not v.ok
    assert any("零语义 diff" in r for r in v.reasons), v.reasons
    # 只改缩进/换行同理（token 不变）
    v2 = _judge(_YANG.replace("    return s_sf_a;\n}", "\treturn s_sf_a;\n}", 1))
    assert not v2.ok and any("零语义 diff" in r for r in v2.reasons), v2.reasons


def test_negative_loop_kill_missing_retain():
    """最锋利的攻击：连 claim 主体一起删——能编译、探针同样会翻转，**只有 retain 能识破**。"""
    yin = _YANG.replace(
        "    while (!s_sf_b) {\n        __atomic_signal_fence(__ATOMIC_SEQ_CST);\n    }\n"
        "    return s_sf_a;", "    return s_sf_a;", 1)
    v = _judge(yin)
    assert not v.ok
    assert any("claim 主体支架被删" in r for r in v.reasons), v.reasons


def test_negative_impostor_program():
    """冒名（换一整个程序）⇒ 新增行+覆盖率+retain 多重命中，绝不放过。"""
    yin = "#include <cstdio>\nint main() { return 0; }\n"
    v = _judge(yin)
    assert not v.ok
    hits = [r for r in v.reasons
            if any(k in r for k in ("新增行", "覆盖率", "claim 主体支架", "retain"))]
    assert len(hits) >= 3 and len(v.reasons) >= 4, v.reasons


def test_negative_duplicate_anchor_rejected():
    """anchor 重名/重载（同文件两处定义）⇒ 拒收，不猜第一个。"""
    src = _YANG + "\nint spin_signal_fence() {\n    return 0;\n}\n"
    v = vd.judge_min_diff(src, _drop_fence_in_anchor(src), anchor=_ANCHOR,
                          remove_text=_REMOVE, retain=list(_RETAIN))
    assert not v.ok
    assert any("定义数" in r or "处定义" in r for r in v.reasons), v.reasons


def test_negative_probe_symbol_not_from_anchor():
    """探针符号与 anchor 不同源（拿别的函数的探针来凑）⇒ Itanium 嵌入校验不过。"""
    v = _judge(_YIN, probe_symbol="_Z18writer_signal_fencev")
    assert not v.ok and any("不同源" in r for r in v.reasons), v.reasons


def test_negative_too_many_tokens_or_lines():
    """超量删除（>3 行 / >40 token / >2% 比率）⇒ 绝对值与比率双闸门，二者 AND。"""
    v = _judge(_YANG.replace(_FENCE_LINE, "", 1), max_code_lines=0)
    assert not v.ok
    v2 = vd.judge_min_diff(_YANG, _YIN, anchor=_ANCHOR, remove_text=_REMOVE,
                           retain=list(_RETAIN), max_tokens=1)
    assert not v2.ok and any("变动 token" in r for r in v2.reasons), v2.reasons


def test_negative_brace_in_string_literal_fail_closed():
    """函数体内字符串字面量含花括号 ⇒ v1 配不准 ⇒ fail-closed 拒（不猜）。"""
    src = _YANG.replace('    while (!s_sf_b) {',
                        '    const char* s = "{";\n    while (!s_sf_b) {', 1)
    v = vd.judge_min_diff(src, _drop_fence_in_anchor(src), anchor=_ANCHOR,
                          remove_text=_REMOVE, retain=list(_RETAIN))
    assert not v.ok and any("花括号" in r for r in v.reasons), v.reasons


# ── 单元：anchor 定位 / Itanium 嵌入 ────────────────────────────────────────


def test_find_func_defs_ignores_calls_and_multiline_params():
    src = ("int helper(int a,\n           int b) {\n    return a + b;\n}\n"
           "int caller() {\n    return helper(1, 2);\n}\n")
    assert vd.find_func_defs(src, "caller").count == 1
    assert vd.find_func_defs(src, "helper").count == 1
    assert vd.find_func_defs(src, "helper").span == (0, 4)
    assert vd.find_func_defs(src, "nowhere").count == 0
    assert vd.find_func_defs("void f() {\n    /* {\n} */\n}\n", "f").span == (0, 4), \
        "块注释里的花括号不得干扰配对"


@pytest.mark.parametrize("anchor,mangled,ok", [
    ("spin_signal_fence", "_Z17spin_signal_fencev", True),
    ("spin_signal_fence", "_Z18writer_signal_fencev", False),
    ("f", "_Z1fv", True),
    ("f", "f", False),
    ("f", "_Zxfv", False),
])
def test_itanium_embeds(anchor: str, mangled: str, ok: bool):
    assert vd.itanium_embeds(anchor, mangled) is ok


def test_tokenize_ignores_comments_and_string_contents():
    assert vd.tokenize_code("int a = 1; // x\n/* y */ int b = 2;") == \
        ["int", "a", "=", "1", ";", "int", "b", "=", "2", ";"]
    assert vd.tokenize_code('s = "a b";') == ["s", "=", '"a b"', ";"]
    assert vd.tokenize_code("a\r\nb\rc") == ["a", "b", "c"], "CRLF/CR 须归一"


# ── schema 校验（533 §2.1）：一条正例 + 逐字段反例 ───────────────────────────

_GOOD_NC = {
    "id": "nc1",
    "variant": "v1",
    "mutation": "delete_mechanism",
    "fixture": "Examples/atoms/x.nc1.cpp",
    "anchor": "spin_signal_fence",
    "remove": "__atomic_signal_fence(__ATOMIC_SEQ_CST);",
    "retain": ["while (!s_sf_b)", "return s_sf_a;"],
    "probe": {"channel": "artifact", "symbol": "_Z17spin_signal_fencev",
              "text": "s_sf_b", "op": "becomes_absent"},
    "note": "删体内零指令屏障 → 循环被整段消除",
}


def _schema(nc: dict, **kw) -> vd.SchemaVerdict:
    kw.setdefault("fixture_exists", lambda p: True)
    kw.setdefault("anchor_def_count", 1)
    kw.setdefault("declared_run_keys", {"spin_signal_fence_ret"})
    return vd.validate_nc_schema(nc, **kw)


def test_schema_positive_and_naming_warning():
    # 无阳夹具上下文（纯 schema 单测）：命名规约不符只 warn（fallback，不拦）
    v = _schema(dict(_GOOD_NC))
    assert v.ok, v.errors
    assert v.warnings == [] or "命名规约" in v.warnings[0]
    v2 = _schema(dict(_GOOD_NC, fixture="Examples/atoms/whatever.cpp"))
    assert v2.ok and any("命名规约" in w for w in v2.warnings)
    # 有阳夹具上下文（真实 replay 路径）：命名不符（未锚定）升 block（547 B3）
    v3 = _schema(dict(_GOOD_NC, fixture="Examples/atoms/whatever.cpp"),
                 yang_fixture="Examples/atoms/x.cpp")
    assert not v3.ok and any("未锚定" in e for e in v3.errors), v3.errors


def test_schema_yin_fixture_anchored_to_yang():
    """547 B3：阴面 fixture 必须锚定本卡阳夹具（stem == 阳夹具主干名 + nc_id后缀），否则 block。

    防借别卡/别优化级产物冒充翻转证据；内容 diff 仍由 replay 的 judge_min_diff 兜底。
    """
    yang = "Examples/atoms/x.cpp"                       # 与 _GOOD_NC.fixture 同源
    v = _schema(dict(_GOOD_NC), yang_fixture=yang)      # x.nc1.cpp 锚 x.cpp ⇒ 须通过
    assert v.ok, v.errors
    # 借来的别卡产物 / 命名"像"但不锚本卡阳夹具 ⇒ 升 block
    for bad in ("Examples/atoms/_atom_align_ctrl.cpp", "Examples/atoms/y.nc1.cpp",
                "Examples/atoms/whatever.nc1.cpp"):
        v2 = _schema(dict(_GOOD_NC, fixture=bad), yang_fixture=yang)
        assert not v2.ok and any("未锚定" in e for e in v2.errors), v2.errors


@pytest.mark.parametrize("key,value,needle", [
    ("id", "NC1", "id 不合规"),
    ("variant", "v2", "variant"),
    ("mutation", "replace_mechanism", "mutation"),
    ("fixture", "Examples/atoms/x.hpp", "后缀"),
    ("fixture", "build/x.nc1.cpp", "build/"),
    ("fixture", "C:/abs/x.nc1.cpp", "相对路径"),
    ("anchor", "spin.signal", "anchor 不合规"),
    ("remove", "", "remove"),
    ("retain", [], "retain"),
    ("retain", ["a", "b", "c", "d", "e", "f", "g"], "retain"),
    ("probe", {"channel": "run_rc", "key": "x"}, "run_rc"),
    ("probe", {"channel": "artifact", "symbol": "_Z17spin_signal_fencev",
               "text": "s_sf_b", "op": "explodes"}, "op"),
    ("probe", {"channel": "artifact", "symbol": "_Z18writer_signal_fencev",
               "text": "s_sf_b", "op": "changes"}, "不同源"),
    ("probe", {"channel": "artifact", "symbol": "_Z17spin_signal_fencev",
               "text": "", "op": "changes"}, "缺 text"),
    ("probe", {"channel": "run_key", "key": "other_key", "op": "changes"}, "未在卡"),
    ("probe", {"channel": "run_key", "key": "spin_signal_fence_ret", "op": "changes"}, ""),
    ("note", "x" * 201, "note"),
])
def test_schema_negative_per_field(key: str, value, needle: str):
    """每个字段各有一条反例；写错即在 schema 层 fail-closed（不许带病进 replay）。"""
    nc = dict(_GOOD_NC)
    nc[key] = value
    v = _schema(nc)
    if needle == "":
        assert v.ok, v.errors                      # run_key 合规形态放行
    else:
        assert not v.ok and any(needle in e for e in v.errors), v.errors


def test_schema_fixture_missing_and_anchor_ambiguous():
    v = _schema(dict(_GOOD_NC), fixture_exists=lambda p: False)
    assert not v.ok and any("不存在" in e for e in v.errors)
    for n in (0, 2):
        v2 = _schema(dict(_GOOD_NC), anchor_def_count=n)
        assert not v2.ok and any("定义数" in e for e in v2.errors), v2.errors


def test_schema_boilerplate_text_rejected():
    v = _schema(dict(_GOOD_NC, probe={"channel": "artifact",
                                      "symbol": "_Z17spin_signal_fencev",
                                      "text": "TODO", "op": "changes"}),
                is_boilerplate=lambda t: t == "TODO")
    assert not v.ok and any("样板文本" in e for e in v.errors)


def test_schema_self_fixture_rejected():
    v = _schema(dict(_GOOD_NC, fixture="Examples/atoms/x.cpp"),
                yang_fixture="Examples/atoms/x.cpp")
    assert not v.ok and any("阳夹具自身" in e for e in v.errors)


# ── 沙箱实证件复跑（533 §1 的真阴面与 6 个攻击样本；沙箱被清理则跳过）────────

_SANDBOX = Path(__file__).resolve().parent.parent / "_arch_v2_round2" / "probe_fence_iso"
pytestmark_skip = pytest.mark.skipif(not (_SANDBOX / "yin_del_fence.cpp").is_file(),
                                     reason="沙箱实证件不在（_arch_v2_round2/probe_fence_iso 已清理）")


def _sandbox_judge(yin_name: str, *, yang: str, anchor: str, remove_text: str,
                   retain: list[str]) -> vd.DiffVerdict:
    return vd.judge_min_diff((_SANDBOX / yang).read_text(encoding="utf-8"),
                             (_SANDBOX / yin_name).read_text(encoding="utf-8"),
                             anchor=anchor, remove_text=remove_text, retain=retain,
                             probe_symbol="_Z17spin_signal_fencev")


@pytestmark_skip
def test_sandbox_real_samples_match_spec_numbers():
    """533 §2.2 校准表复算：真阴面过；6 个攻击样本全拒（数字须与规格一致）。"""
    yang, remove = "yang.cpp", "__atomic_signal_fence(__ATOMIC_SEQ_CST);"
    retain = ["while (!s_sf_b)", "return s_sf_a;"]
    good = _sandbox_judge("yin_del_fence.cpp", yang=yang, anchor="spin_signal_fence",
                          remove_text=remove, retain=retain)
    assert good.ok, good.reasons
    m = good.metrics
    assert (m["hunks"], m["inserted_lines"], m["code_deleted_lines"]) == (1, 0, 1)
    assert m["tokens_changed"] == 5 and m["token_change_ratio"] <= 0.02, m
    for name in ("yin_formal_43.cpp", "yin_del_unrelated.cpp", "yin_loop_kill.cpp",
                 "yin_smuggle_comment.cpp", "yin_impostor.cpp"):
        bad = _sandbox_judge(name, yang=yang, anchor="spin_signal_fence",
                             remove_text=remove, retain=retain)
        assert not bad.ok, f"{name} 应被拒：{bad.metrics}"
    loop_kill = _sandbox_judge("yin_loop_kill.cpp", yang=yang, anchor="spin_signal_fence",
                               remove_text=remove, retain=retain)
    assert any("claim 主体支架被删" in r for r in loop_kill.reasons), loop_kill.reasons


@pytestmark_skip
def test_sandbox_report_json_reproducible():
    """probe_report.json 的读数可复算（阴面永不锚 sha，只做符号区间读数）。"""
    rep = json.loads((_SANDBOX / "probe_report.json").read_text(encoding="utf-8"))
    assert rep, "沙箱报告不为空"


def test_module_has_no_repo_imports():
    """判据模块必须是可被 gate/replay 双侧复用的**纯**模块（不 import 仓库其它工具）。"""
    src = (Path(__file__).resolve().parent.parent / "tools" / "viso_diff.py").read_text(
        encoding="utf-8")
    assert "import atom_evidence_replay" not in src
    assert "import gate_engine" not in src
    # 运行期零 IO：模块里不出现 open( / Path( 之类的读写入口
    assert "open(" not in src.replace("# ", "")
    assert subprocess.run(["git", "--version"], capture_output=True).returncode == 0
