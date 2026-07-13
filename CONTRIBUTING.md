# CONTRIBUTING — 贡献指南

> 参照: GOVERNANCE.md / CONVENTIONS.md / knowledge_graph.json

## 快速开始

```bash
git clone <repo>
make.bat full          # 验证当前状态
make.bat check         # 仅门禁
```

## 贡献章节

### 新建章
1. 从 `tools/chapter_template.md` 克隆骨架
2. 填充 20 圈码内容，≥30 独立可编译 cpp 块
3. `python tools/chapter_compile_check.py Book/partXX/chYY_xxx.md` → 0 fail
4. `make.bat check` → 0 ERROR
5. 更新 `PROGRESS.md`、`knowledge_graph.json`、`TASKS.md`

### 修复章
1. 定位问题（`python tools/consistency_check.py` 输出）
2. 修改后跑 `python tools/chapter_compile_check.py <target>`
3. `make.bat check`

### 代码规范
- 每个 ```cpp 块必须独立可编译（#include + int main）
- 禁用: `<print>` `<mdspan>` `<flat_map>` `<flat_set>`（GCC13 未实现）
- UDL 空格: `operator"" _x`
- ⑳ 标题禁止: "推荐阅读" "参考文献" "延伸阅读"
- 立场标签: `[标准]` `[实现·GCC13]` `[平台·x86-64]` `[经验]`

## 禁止操作

- ❌ 覆盖已有章节文件
- ❌ 删除 `_legacy_*` 目录
- ❌ 修改章节编号
- ❌ 重命名 part 目录
- ❌ 手动编辑 `glossary.json`（用脚本追加）
