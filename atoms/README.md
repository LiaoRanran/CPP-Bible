# atoms/ — L1 原子库

**这是什么**：以"原子论断"为单位的知识库。一个文件 = 一条可独立证伪的断言 + 五重剖面元数据。

**不是什么**：不是书的草稿，不是章节备份，不是笔记。凡不能写成"一断言 + 证据"的内容不许进这里。

## 准入规则（硬）

1. 文件命名 `ATOM-{DOMAIN}-{TOPIC}-{NNN}.md`，放对应域子目录（`mem/`、`ub/`、`stl/`…）。域名见 `docs/kernel/G1_knowledge_map.md`。
2. 必须带 YAML frontmatter，字段见 `docs/kernel/G1_layout.md` 第 3 节；五重剖面（`sources` / `evidence` / `superiority` / `depth` / `pedagogy`）缺一不可。
3. **新原子禁止停留在未验证状态**：`status: verified` 才允许进入学习路径与章节装配（DRQ-4 红线：新产出原子绝不出现 UNVERIFIED）。
4. **必须带反例**：每个原子都要有"让它失败的实验"一节；只演示成立的不合格。
5. ID 入库后永久不变；拆分/合并/改名只登记不改名，写进 `id_migrations.json`。

## 禁止

- 直接改 `Book/` 下的存量 md（存量走 L0 快照 → 萃取，不原地改）。
- 把原子文件放进 `Book/`（会被 mkdocs 扫进站点）。
- 在正文里写"据某博客说"而无独立源与一手实证。
