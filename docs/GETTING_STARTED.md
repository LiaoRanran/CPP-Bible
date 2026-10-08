# GETTING_STARTED · 30 分钟从零到跑出论文数字

> 面向**第一次打开这个仓库的人**。目标不是读完，是**跑通**。
> 环境细节的权威版本见 [`ENVIRONMENT.md`](ENVIRONMENT.md)；实验复现见 [`EXPERIMENTS.md`](EXPERIMENTS.md)。

---

## 0. 先确认你来这里要什么

| 你可能想做的事 | 需要的环境 | 去哪 |
|---|---|---|
| 只想核对论文里的数字 | **只要 Python**（无编译器依赖） | §1 |
| 想跑完整检测链（真实编译/运行） | WSL Ubuntu 24.04 + g++ 13.3 **且** MinGW g++ 13.1 + clang++ | §2 |
| 想在容器里复现 | Docker（**693 执行环境未装，镜像未实测**） | §3 |
| 想给数据集做人类标注 | 只要能读 C++ | `data/693_annotation_guide.md` |
| 想看书（147 章教程） | Python + 浏览器 | README §7 |

---

## 1. 五分钟：纯 Python 数据链（推荐先跑这个）

```bash
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible

# ① 环境体检 —— 会明确告诉你哪些资产在本机不可用（不做静默降级）
bash Scripts/verify_environment.sh --report

# ② 冻结产物完整性（14 项权威产物 sha256）
python tools/gen_693_manifest.py --check
#   期望：[693-B2] 校验完成：14 项，失配 0 项，缺失 0 项

# ③ 论文数字 vs 权威源（fail-closed：任何硬不一致都退出非 0）
python tools/verify_paper_numbers.py

# ④ 论文门禁（页数 / 摘要词数 / TODO 占位）
python tools/paper_quality_gate_670c2.py
```

这四个命令**只用 Python 标准库**，不需要装任何包，也不需要编译器。
跑完你就已经验证了"仓库里的数字和论文里的数字是一致的"。

再进一步（仍然纯 Python）：

```bash
python tools/analyze_683_oc.py --stage all    # operator 16+16 配置消融 + 7 基线
python tools/site_683_data.py                 # 再生成 docs/ 站上数据（同源校验）
python tools/annotate_693_b.py --csv          # 重算 AI 双标 + 人类裁决表
python tools/compute_693_iaa.py               # 人类裁决回来后算 κ（现在会是 pending）
```

---

## 2. 三十分钟：完整检测链（需要 WSL + MinGW + clang）

**为什么必须两套环境**：sanitizer 运行时（libasan/libubsan/libtsan）只在
WSL/Linux 的 g++ 13.3 里有；MinGW g++ 13.1 负责 compiler-warn / cross-compile / linker。
两套装的资产不同，**混用会直接让数字不可比**——这是本项目的头号复现风险。

### 2.1 WSL 侧（必须做的 UTF-8 横幅规避）

```bash
# ⚠ 这两行不是可选项：开启 Windows 系统代理时，wsl.exe 会向 stderr 写一条
#    UTF-16LE 横幅 ⇒ Python 解码失败 ⇒ ASan/UBSan 报告全部静默丢失（系统性假 miss）
export WSL_UTF8=1
export WSLENV=WSL_UTF8/u

wsl -e bash -lc 'sudo apt-get update && sudo apt-get install -y g++ gdb'
wsl -e bash -lc 'g++ --version | head -1'      # 期望 13.3.0
```

### 2.2 Windows 侧

```bash
g++ --version     | head -1   # 期望 13.1.0（MinGW-Builds x86_64-posix-seh-rev1）
clang++ --version | head -1   # 期望 22.1.8（MSYS2 mingw64）
cppcheck --version            # 期望 2.21.0（692-D 公平对比用）
```

### 2.3 跑真实靶场

```bash
python tools/collect_realworld_683.py --stage verify   # NVD API 在线验证（需网络）
python data/realworld_683_runner.py --stage detect     # 110 × 8 真实检测（增量 checkpoint）
python data/realworld_683_runner.py --stage merge
```

---

## 3. 容器复现（需要 Docker）

```bash
docker compose -f docker/reproduce/docker-compose.yml build
docker compose -f docker/reproduce/docker-compose.yml run --rm verify-env
docker compose -f docker/reproduce/docker-compose.yml run --rm reproduce
```

> ⚠ **693 执行环境未安装 Docker**，上面三条命令**一次都没跑过**。
> 镜像内的 `RUN` 已内置版本自检（gcc 12.3.0 / clang 14.0 / cppcheck 2.7 / valgrind 3.18 /
> python 3.10），装错会在**构建期**失败而不是运行期静默给错数。
> 首次构建失败请把日志原样贴进 issue。

---

## 4. 常见失败与对策

| 症状 | 原因 | 对策 |
|---|---|---|
| `-fsanitize=address 不可用` | MinGW 无 ASan 运行时（**已知预期**，不是配置错误） | 在 WSL 里跑 sanitizer 资产；`verify_environment.sh` 对 windows-native 画像只 WARN |
| `-Wunsequenced 不被接受` | 那是 clang 的选项，MinGW g++ 13.1 不认（673u 已登记） | 预期行为；该资产恒 `unknown` |
| WSL 里 ASan 一条报告都没有 | UTF-16LE 横幅吞掉了 stderr | `export WSL_UTF8=1` + `WSLENV=WSL_UTF8/u` |
| `sha256 校验失配` | `data/` 下冻结产物被改动 | **不要**改清单去"让它过"；先查是谁改的、为什么改 |
| fast_gate 报 `No module named pytest` | 用的解释器不对（`fast_gate` 用 `sys.executable`） | 用 `.venv/Scripts/python.exe` 跑 |
| 论文数字对账失败 | `data/` 与 tex 不同步 | `tools/verify_paper_numbers.py` 会指出具体是哪一条 |

---

## 5. 下一步

- 想知道**每个实验怎么复现**：[`EXPERIMENTS.md`](EXPERIMENTS.md)
- 想知道**数据文件长什么样**：[`DATA_FORMAT.md`](DATA_FORMAT.md)
- 想知道**系统怎么组织的**：[`ARCHITECTURE.md`](ARCHITECTURE.md)
- 想贡献代码：[`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- 想做人类标注：[`../data/693_annotation_guide.md`](../data/693_annotation_guide.md)
