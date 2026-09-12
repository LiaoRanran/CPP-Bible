# ADR-0002：原子库落盘位置与形态

- 状态：**已接受**（2026-09-10，G1）
- 决策人：人（DRQ-2 选 A），执行：架构师

## 背景

原子库需要一个落盘位置与文件形态，且不能污染现有发布链（mkdocs 站点 / PDF / EPUB）。

## 候选

**A. 仓库根 `atoms/`（与 `Book/` 平级）**，MD 正文 + YAML frontmatter；证据另放仓库根 `evidence/`。
**B. `Book/_atoms/`**，JSON 记录 + 同目录 MD。

## 取舍

选 **A**。理由：
1. **原子不是"书的一页"**。它是生产资料，不是出版内容。放在 `Book/` 里会让人误以为它直接参与渲染，也会让"章 = 装配视图"的关系变模糊。
2. `Book/` 目前被大量工具按"147 章 + 固定编号"假设扫描（compile_all、consistency_check、density_audit…）。往里塞 `_atoms/` 子目录，风险是这些扫描器把它当章处理（已有 `iter_md_files` 会 rglob 所有 md）。放外面零风险。
3. md + YAML frontmatter 与全书技术栈一致（`comment_blocks`/`patch_blocks`/各类 audit 都在解析 md 围栏与 YAML 风格元数据），无需引入 JSON 解析新路径。
4. 证据独立放 `evidence/`，物理隔离保证 L2"证据与断言多对多分离"不被偷懒合并。

## 否决理由

- 否 B：`Book/` 内新建目录会进入现有 md 扫描器的 rglob 范围，需要逐工具加 exclude，成本高且易漏；JSON+MD 双文件增加同步负担。

## 后果

- 正面：不触碰 `Book/` 与现有工具，发布链零改动风险。
- 负面/待办：必须在 `mkdocs.yml` 显式 exclude `atoms/`、`evidence/`、`sources/`（**G5 试点时执行并验证站点构建**，本轮不改发布配置）。
- 约束：新目录需要被 `.gitignore` 之外的卫生门禁认知（根级产物清理脚本按扩展名 `*.cpp/*.exe/*.o` 工作，不受影响）。
