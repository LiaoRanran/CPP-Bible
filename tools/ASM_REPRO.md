# Examples/*.asm 复现性与版本一致化工作流

证据库 `Examples/*.asm` 由 MinGW GCC 生成（`g++ -S -masm=intel`，特性：
`.seh_proc` / `.def` / `__main` / `x86_64-posix-seh`）。因此本工作流**只能在
Windows + MinGW 下运行**，作为本地预推送自检；CI ubuntu gcc-15（CFI/AT&T/SysV）
无法复现 MinGW asm，故不进 CI。

## 工具
- `tools/asm_repro_spotcheck.py` —— 对抗式复现性审计（非零确认）
  - 对每个存储 .asm，用 MinGW 15.3.0 按可推断约定（`flags_for`：`c++23`，
    `_O0→O0`、`_O1→O1`、`_OS→Os`、`ch14→-g -O0`）重编其源（来自 `.file` 指令）
  - 归一化后做**双向符号集校验**（stored ⊆ fresh 且 fresh ⊆ stored），并比对函数体
  - 状态：MATCH（精确复现）/ DRIFT（符号集或体不一致，细分 STORED_EXTRA 伪造嫌疑方向、
    FRESH_EXTRA 版本漂移方向、LINES 仅体差异）/ COMPILE_FAIL（源无法 -S，如 modules）/
    NO_SOURCE（无 `.file` 源）
  - KEY 归一化：`.LFB394`→`.LFB`、`.L4`→`.L4`，消除编译期内部标号数字噪声
- `tools/asm_regen.py` —— 版本统一再生驱动器（13.1.0 → 15.3.0）
  - 仅替换「重编成功」且「用户级被定义函数符号集 ⊇ 原存储」的文件；丢符号则跳过
    （除非 `--force`），保留原 EOL 消伪 diff
  - 安全网：`verify_asm_evidence.py`（书内符号 ⊆ 真实产物，前缀匹配，对版本不敏感）

## 红线裁决方法论
1. **负控必做**：向真实样本追加 `.text` 内幽灵符号 → 须判 DRIFT[STORED_EXTRA]；
   篡改真实符号名 → 须判 DRIFT；真实样本 → 须 MATCH。三者全过才可信。
2. **法医分级**：STORED_EXTRA 先排除编译器/库内部符号（`.Frame.*`/`.part`/`.constprop`/
   `__gthread`/`printf`/`std::` 等），再对残留用户符号 demangle 取词元与源文件词元比对；
   零重叠且非库/编译器前缀 → 真伪造嫌疑。
3. **版本一致化**：有源必须真实重生（红line要求）；无源诚实标注（UNMARKED）。

## 当前状态（2026-07-20 治理后）
- 239/258 精确复现于 15.3.0（MATCH）
- 7 个书内锚定文件保留 13.1.0（其 mangled 名被书引用，跨 GCC 版本不稳定；回退以保书准确）
- 1 个 SIMD（`_ch99`）因 AVX 架构推断缺口良性 DRIFT
- 2 个 C++20 modules 无法 `-S` 重编（诚实跳过）
- 9 个无 `.file` 源（UNMARKED，诚实标注）

## 用法
```bash
GPP="C:/Qt/Tools/mingw1530_64/bin/g++.EXE"
# 复现性审计（全量）
python tools/asm_repro_spotcheck.py --gpp "$GPP" --examples Examples --out build/repro.json
# 版本统一再生（先 dry-run 评估，再 --apply --force）
python tools/asm_regen.py --gpp "$GPP" --examples Examples --only 13.1.0 --dry-run
python tools/asm_regen.py --gpp "$GPP" --examples Examples --only 13.1.0 --apply --force
# 书内符号真实性（再生后必跑，期望 0 DRIFT）
python tools/verify_asm_evidence.py --root Book --examples Examples
```
