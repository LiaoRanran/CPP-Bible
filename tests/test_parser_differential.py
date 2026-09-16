"""554 T3：parser 差分 —— Hypothesis 生成多态/畸形 frontmatter，三解析器一致性。

三解析器（同一段 frontmatter 文本）：
  ① `atom_evidence_replay.parse_frontmatter`（自定义 replay 侧，= gate._meta 的权威实现）；
  ② `yaml.safe_load`（"天真消费者"视角）；
  ②' `yaml.load(..., Loader=UniqueKeyLoader)`（gate 实际路径 = safe + 重复键检测）；
  ③ gate 硬化层 `check_frontmatter_hardening`（**唯一入口读磁盘** ⇒ 测试用 tmp bay 重定向）。

铁律（554 §T3）：对"门禁关心的键"，三者要么判决一致，要么分歧被硬化层**显式 block**；
不允许"一个收下、另一个也收下但语义不同"或"硬化层沉默放行"（灰色态）。

553 已合入：flow 式 `negative_controls` 必落 `[nc-flow]` block（547 B5 根因 =
parse-diverge 的比对键不含 `negative_controls`，见 gate_engine L1355）。

标 fast（纯字符串解析 + 只写 tmp，不编译、不跑 replay）。
"""
from __future__ import annotations

import itertools
import re
from pathlib import Path

import atom_evidence_replay as rp
import gate_engine as ge
import pytest
import yaml
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from yaml.constructor import ConstructorError

# ── 三解析器口径常量 ───────────────────────────────────────────────────────
# gate parse-diverge 实际比对键（gate_engine L1355）；negative_controls 不在其中 ⇒ 这正是 B5 根因。
DIVERGE_KEYS = ("id", "verdict", "status", "artifact_sha256")
# 556：nc 形态硬化族从"只堵 flow"升级为"白名单块式序列" ⇒ nc-flow / nc-map / nc-scalar
# 三个子信号（统一带 [nc-form] 前缀）都算已知 block 信号。
KNOWN_BLOCK_TAGS = ("[indent-smuggle]", "[nc-flow]", "[nc-map]", "[nc-scalar]",
                    "[nc-form]", "[dup-key]", "[parse-diverge]")
ALL_TAGS = KNOWN_BLOCK_TAGS + ("[invalid]",)

FLOW_NC = ("negative_controls: [{id: nc1, variant: v1, mutation: fence, fixture: a.cpp, "
           "anchor: f, remove: x, retain: [y], "
           "probe: {channel: artifact, symbol: s, op: becomes_absent, text: t}}]")


class UniqueKeyLoader(yaml.SafeLoader):
    """gate_engine 内层 `_UniqueKeyLoader` 的测试侧等价物（局部类不可导入）。

    与裸 `safe_load` 语义不同：后者 after-wins、不报重复键 ⇒ 只跑 safe_load 会系统性漏掉
    整类 `[dup-key]`。
    """

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        seen: set = set()
        for key_node, _v in node.value:
            k = self.construct_object(key_node, deep=deep)
            if k in seen:
                raise ConstructorError(None, None, f"duplicate key: {k}", key_node.start_mark)
            seen.add(k)
        return mapping


@pytest.fixture()
def fmbay(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """把 gate 的扫描根重定向到 tmp（硬化层没有字符串入口，只能落盘后再扫）。"""
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    return tmp_path


_counter = itertools.count()


def _run_hardening(bay: Path, fm_text: str) -> list:
    """每调用一个**独立目录 + 唯一文件**再跑硬化层。

    两个必须的隔离：① 目录独立 ⇒ 不累加历史样本（否则 check_frontmatter_hardening 的
    全目录扫描会把上一条的命中混进来、且 O(n²)）；② 唯一文件 + 清缓存 ⇒ 杜绝
    `(str(p), st_mtime_ns, st_size)` 键碰撞导致读到陈旧命中（假反例）。
    """
    ge.clear_meta_cache()
    fm_cache = getattr(ge, "_FM_CACHE", None)
    if fm_cache is not None:
        fm_cache.clear()
    d = bay / f"case{next(_counter)}"
    ev, at = d / "evidence", d / "atoms"
    ev.mkdir(parents=True)
    at.mkdir()
    (ev / "EV-HYP.md").write_text("---\n" + fm_text + "\n---\n正文\n", encoding="utf-8")
    old_a, old_e = ge.ATOMS, ge.EVIDENCE
    ge.ATOMS, ge.EVIDENCE = at, ev
    try:
        return ge.check_frontmatter_hardening()
    finally:
        ge.ATOMS, ge.EVIDENCE = old_a, old_e
        ge.clear_meta_cache()


def _shape(v):
    """结构归一（比较两解析器对同一值的"形状"）：scalar 归到 str().strip()，map/seq 递归。

    只用于判断**分歧**，不用于判合法性——语义合法与否是别的门禁规则的职责。
    """
    if v is None:
        return None
    if isinstance(v, dict):
        return ("map", tuple(sorted((str(k), _shape(vv)) for k, vv in v.items())))
    if isinstance(v, (list, tuple)):
        return ("seq", tuple(_shape(x) for x in v))
    return ("scalar", str(v).strip())


def _parse_three(fm: str, bay: Path):
    """跑齐三解析器，返回 (自定义 dict, safe 结果, 是否重复键, hits, blocked, tags)。"""
    try:
        custom = rp.parse_frontmatter("---\n" + fm + "\n---\n正文\n")
    except ValueError:
        custom = {}                       # 复刻 gate._meta：ValueError -> {}
    try:
        safe = yaml.safe_load(fm)
    except yaml.YAMLError:
        safe = None
    dup_key = False
    try:
        yaml.load(fm, Loader=UniqueKeyLoader)
    except ConstructorError:
        dup_key = True
    except yaml.YAMLError:
        pass
    hits = _run_hardening(bay, fm)
    blocked = any(f.severity == "block" for f in hits)
    tags = {t for t in ALL_TAGS if any(t in f.message for f in hits)}
    return custom, safe, dup_key, hits, blocked, tags


# ── Hypothesis 生成器：多态/畸形 frontmatter（裸 fm 文本，不含 ---）──────────
_GATE_KEYS = st.sampled_from(["id", "verdict", "status", "artifact_sha256", "negative_controls"])
_SCALAR = st.sampled_from([
    "EV-HYP-1", "confirm", "refute", "draft", "machine-verified", "0" * 8,
    '"quoted: colon"', "'single'", "3", "true", "no", "null", "~", "[]", "{}",
    "a # trailing comment", "`backtick start", "全角：值", "a:b", "|x", ">-",
])
_FRAG = st.one_of(
    st.builds(lambda k, v: f"{k}: {v}", _GATE_KEYS, _SCALAR),                 # 普通标量对
    st.builds(lambda k, a, b: f"{k}: {a}\n{k}: {b}", _GATE_KEYS, _SCALAR, _SCALAR),  # 顶层重复键
    st.just("actual: {run_match_file: x.out, run_match_file: y.out}"),        # flow-map 重复键
    st.builds(lambda k, k2: f"{k}: f.cpp &x\n  {k2}: injected", _GATE_KEYS, _GATE_KEYS),  # 缩进走私
    st.builds(lambda k: f"{k}:\n  compiler: [GCC 15.3.0]\n  std: [c++17]", _GATE_KEYS),    # 阴性块
    st.builds(lambda k: f"{k}:   # 注释\n  sub: v", _GATE_KEYS),              # 阴性：注释后块
    st.builds(lambda k, b: f"{k}: |\n  {b}", _GATE_KEYS, st.text(max_size=20)),   # block scalar
    st.builds(lambda k, b: f"{k}: >-\n  {b}", _GATE_KEYS, st.text(max_size=20)),
    st.just(FLOW_NC),                                                        # flow nc（B5 原样）
    st.just("negative_controls:\n  - id: nc1\n    variant: v1\n    fixture: a.nc1.cpp"),  # block nc
    st.just("  negative_controls: [{id: nc1}]"),                             # 缩进 flow nc
    st.builds(lambda k: f"\t{k}: v", _GATE_KEYS),                            # 制表符缩进
    st.just("全角键：值"),
    st.text(max_size=30, alphabet=st.characters(blacklist_categories=("Cs", "Cc"))),  # 垃圾行
)

FRONTMATTER = (
    st.lists(_FRAG, max_size=8).map("\n".join)
    .filter(lambda s: "\n---" not in s and "\r" not in s)
)

_SETTINGS = settings(
    max_examples=200,
    deadline=None,
    suppress_health_check=(HealthCheck.function_scoped_fixture,
                           HealthCheck.too_slow,
                           HealthCheck.filter_too_much),
)


# ── 差分主测：不允许灰色态 ─────────────────────────────────────────────────
@_SETTINGS
@given(fm=FRONTMATTER)
def test_no_gray_state_between_parsers(fmbay: Path, fm: str):
    custom, safe, dup_key, hits, blocked, tags = _parse_three(fm, fmbay)

    # P1 核心：门禁关心的键，要么一致，要么被硬化层显式 block（复刻 L1357-1358 的 None-skip）
    if isinstance(safe, dict):
        for k in DIVERGE_KEYS:
            a, b = custom.get(k), safe.get(k)
            if a is None or b is None:
                continue
            assert str(a).strip() == str(b).strip() or blocked, (
                f"两解析器在 {k!r} 分歧但硬化层放行（灰色态）："
                f"custom={a!r} safe={b!r}；fm={fm!r}")

    # P2：nc 是 B5 的根（gate parse-diverge 的比对键不含它）⇒ 两解析器对 nc **分歧**时
    # 硬化层必须显式 block（否则门禁虚假干净）。两侧任一为 None 则跳过（复刻 L1357-1358）。
    # 注意：只在“形状分歧”时要求 block；两侧都收下同一形态（哪怕 schema 非法）不属差分灰色态，
    # 那由 gate 的 check_negative_controls 等规则负责。
    a_nc = custom.get("negative_controls")
    b_nc = safe.get("negative_controls") if isinstance(safe, dict) else None
    if a_nc is not None and b_nc is not None and _shape(a_nc) != _shape(b_nc):
        assert blocked, (
            f"两解析器对 negative_controls 分歧但硬化层放行（灰色态）："
            f"custom={_shape(a_nc)!r} safe={_shape(b_nc)!r}；fm={fm!r}")

    # P3（547 B5 + 556）决定性保证：nc 的一切非块式形态（flow/map/标量）必落对应 [nc-*] 信号
    for ln in fm.splitlines():
        m = re.match(r"^\s*negative_controls\s*:\s*(.*)$", ln)
        if not m:
            continue
        val = m.group(1).strip()
        if not val or val.startswith("#"):
            continue                       # 键行无值 / 仅注释 = 合法块式起点
        want = ("[nc-flow]" if val.startswith("[")
                else "[nc-map]" if val.startswith("{") else "[nc-scalar]")
        assert want in tags, f"nc 非块式形态未落 {want}；fm={fm!r}"

    # P4：block 必须"有理有据"（落已知信号，防无关规则偶然 block 掩盖真分歧）
    if blocked:
        assert tags & set(KNOWN_BLOCK_TAGS), (
            "硬化层 block 但无已知信号标签：" + repr([f.message for f in hits
                                                      if f.severity == "block"]))

    # P5：UniqueKeyLoader 报重复键 ⇒ 必落 [dup-key]（裸 safe_load 不报，故单独断言）
    if dup_key:
        assert "[dup-key]" in tags, f"重复键未被 [dup-key] 拦下；fm={fm!r}"


# ── 确定性回归（shrink 出的反例不可读 ⇒ 关键几格另钉死）─────────────────────
def test_flow_nc_is_gray_state_caught_by_hardening(fmbay: Path):
    """547 B5 决定性回归：flow 式 nc 让 safe_load/自定义都"收下"（无异常），
    唯独硬化层 [nc-flow] 显式 block —— 灰色态被 hardening 兜住的样例（与
    test_p0d_hardening.test_nc_flow_rejected 互补，勿删其一）。"""
    _custom, safe, _dup_key, hits, blocked, tags = _parse_three(FLOW_NC, fmbay)
    assert isinstance(safe, dict) and safe.get("negative_controls") is not None, "safe_load 应收下"
    assert blocked and "[nc-flow]" in tags, [f.message for f in hits]


def test_block_nc_not_flow_flagged(fmbay: Path):
    """阴性：block 式 nc 三解析器都不该触发 [nc-flow]（存量卡零误伤）。"""
    _custom, _safe, _dup, hits, _blocked, tags = _parse_three(
        "id: EV-X\nnegative_controls:\n  - id: nc1\n    variant: v1", fmbay)
    assert "[nc-flow]" not in tags, [f.message for f in hits]


def test_unclosed_frontmatter_raises_value_error():
    """诚实记录：未闭合 frontmatter ⇒ 自定义解析器抛 ValueError（gate 语义 = 无 metadata）。"""
    with pytest.raises(ValueError):
        rp.parse_frontmatter("---\nid: EV-X\n")


# ── 已知分歧登记（556 §问题1-3）：本批**不**扩大硬化改动面 ────────────────────
# YAML 1.1 陷阱词会让自定义解析器（纯字符串子集）与 PyYAML（safe_load）对同一标量给出不同
# 类型/字面：前导零（`00000000`→int 0）、布尔陷阱（`yes/no/on/off/y/n`）、其它隐式类型
# （`~`/八进制/时间戳）。对**门禁关心的键**，这类分歧已闭合：
#   - DIVERGE_KEYS（id/verdict/status/artifact_sha256）⇒ gate 的 [parse-diverge] block；
#   - negative_controls ⇒ 556 补齐的 [nc-form] block。
# 但**其余键**（如 hypothesis/自定义字段）的同类分歧目前**无硬化信号**，属已知未覆盖面——
# 是否扩到其他键的硬化**另开任务**（556 §问题1-3 明示不在本批扩大改动面）。
_KNOWN_YAML11_TRAPS = ("前导零（00000000 → int 0）", "布尔陷阱（yes/no/on/off/y/n）",
                       "其它 YAML 1.1 隐式类型（~ / 八进制 / 时间戳）")


@pytest.mark.xfail(strict=False,
                   reason="556 §问题1-3 已知未覆盖：非门禁键的 YAML 1.1 陷阱分歧暂无硬化信号")
def test_non_gate_key_yaml11_trap_should_block(fmbay: Path):
    """登记未覆盖面（**非修复**）：`hypothesis: 00000000` 自定义='00000000' vs safe=0 分歧，
    理想应被硬化层拦，现状该键不在 gate 关心集合、亦非 nc ⇒ 沉默。

    标 xfail 记录；未来若扩硬化到其他键，本用例自然 XPASS（strict=False 不红），届时转正式断言。
    """
    fm = "id: EV-X\nhypothesis: 00000000"
    custom, safe, *_rest, blocked, _tags = _parse_three(fm, fmbay)
    assert str(custom.get("hypothesis")).strip() != str(safe.get("hypothesis")).strip(), "应分歧"
    assert blocked, "理想：非门禁键分歧也应被硬化层拦（现状未覆盖）"
