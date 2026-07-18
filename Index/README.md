# 索引体系说明（Index/ 与全书索引分工）

> 本文件说明《现代 C++ 终极圣经》中**所有索引类文件**的定位、生成方式与维护责任，
> 目的是消除"手工策展索引"与"自动生成索引"被误判为重复件而引发的误删/误合。
> 建立背景：阶段0 轻量整理（验证汇报 §6.1 N2 误判 `Index/CROSSREF.md` 为 192KB 重复件，
> 实地复核实为 26 行手工概念映射）。

## 一、总览：三类索引，三种来源

| 文件 | 位置 | 来源 | 维护方式 | 计入一致性门禁 | 用途 |
|------|------|------|----------|----------------|------|
| `CROSSREF.md` | 仓库根 | `tools/gen_crossref.py` 自动生成 | **禁止手改**；重生成：`python tools/gen_crossref.py` | 否（独立导航件） | 全局章节依赖图（732 条依赖边），含枢纽章 Top10 与孤立章清单，用于导航速查 |
| `Index/CROSSREF.md` | `Index/` | **手工策展** | 随章节推进手动补 `A ⇄ B` | 否 | 知识点双向概念映射（作者挑选的核心链，如 RAII⇄智能指针⇄异常安全） |
| `Index/GLOSSARY.md` | `Index/` | **手工策展** | 按 CONVENTIONS 持续补术语定义+章节+关联术语 | 否 | 人工术语库（带解释性文字） |
| `Index/MISCONCEPTIONS.md` | `Index/` | **手工策展** | 持续补「误区→真相→章节」 | 否 | 误区数据库（目标 1000+ 条），独有内容 |
| `Book/GLOSSARY.md` | `Book/` | `tools/gen_indexes.py` 自动生成 | **禁止手改**；CI 以 `gen_indexes --check` 校验 | 否（自动件） | 术语 → 讲解该主题的章节（机械抽取，仅收录能匹配真实章节的术语） |
| `Book/SUMMARY.md` | `Book/` | `tools/gen_indexes.py` 自动生成 | **禁止手改** | 否 | 全书目录（16 部分 / 147 章，相对路径链接），即「全文章目」 |
| `Book/PREREQUISITES.md` | `Book/` | `tools/gen_indexes.py` 自动生成 | **禁止手改** | 否 | 逐章显式前置依赖建议 |
| `INDEX.md` | 仓库根 | **手工策展** | 手动维护 | 否 | 项目总索引 / 接手地图（阅读顺序 AGENT→HANDOVER→…），**非**章节书目录 |

## 二、关键澄清（消除「双索引重复 / 漂移」误解）

1. **`Index/CROSSREF.md` 与根 `CROSSREF.md` 不是同一文件、不是重复。**
   - 根 `CROSSREF.md`：机器从各章内嵌 `⟶` / Markdown 交叉引用抽取的**全量依赖图**（732 边），用于导航速查。
   - `Index/CROSSREF.md`：作者**人工挑选**的「核心概念链」双向映射，是策展视角，非全量。
2. **`Index/GLOSSARY.md` 与 `Book/GLOSSARY.md` 不是重复。**
   - `Index/GLOSSARY.md`：人工撰写的定义 + 关联术语（带解释性文字）。
   - `Book/GLOSSARY.md`：机器抽取的「术语→章节」清单（仅收录能匹配真实章节的术语），由 CI `--check` 校验一致性。
3. **`Index/MISCONCEPTIONS.md` 为独有内容**，无任何自动件对应，不可删。
4. **`INDEX.md`（根）是接手地图**，不是章节书目录；全书章节书目录是 `Book/SUMMARY.md`。

## 三、为何不存在「两套索引各自漂移」

- 手工策展件（`Index/*`、`INDEX.md`）与自动生成件（`Book/*`、根 `CROSSREF.md`）**职责正交**：
  前者补解释性 / 策展内容，后者提供机械一致的导航，二者不互为真相源。
- 交叉引用门禁（`tools/xref_check.py`）实测：**0 断链 / 0 孤儿 / 0 孤岛**，
  说明正文章节间的引用网自洽；索引件是引用网的「视图」，不是第二套真相源。
- 自动件均由脚本从正文单一真相源生成，CI 门禁保证其与正文一致（`gen_indexes --check` PASS）。

## 四、维护守则

- 改**正文章节**后：跑 `python tools/gen_indexes.py` 与 `python tools/gen_crossref.py` 重生成自动件；
  勿手改 `Book/GLOSSARY.md`、`Book/SUMMARY.md`、`Book/PREREQUISITES.md`、根 `CROSSREF.md`。
- 新增**术语 / 误区 / 核心概念链**：手动补 `Index/GLOSSARY.md` / `Index/MISCONCEPTIONS.md` / `Index/CROSSREF.md`。
- 接手新人：先读根 `INDEX.md` 的阅读顺序表，再按 `Book/SUMMARY.md` 浏览章节。
