# ENVIRONMENT · Queyi 复现环境锁定（693-B3）

> **这份文档回答一个问题：论文的每个数字，是在什么机器上、用什么版本算出来的？**
> 所有版本号均为**本机实测**（标注了采集命令），不是抄来的。
> 采集时间：2026-10-08（693 批次执行期间）。

---

## 1. 三套环境画像

论文里的数字分布在三套环境里。**混用会直接导致数字不可比** —— 这是本项目的头号复现风险。

| 画像 ID | 用途 | 在哪些数字里出现 |
|---|---|---|
| `wsl-gcc-13.3` | 全部 **sanitizer 资产**（asan / ubsan / tsan）+ 运行期行为 | A5 主端点、盲区地图、1147×8 冻结矩阵 |
| `windows-native-mingw` | **compiler-warn / cross-compile / linker** + 外部工具公平对比 | 692-D 公平对比（clang-tidy / cppcheck）、cross-compile 资产 |
| `docker-ubuntu-22.04` | 693-B1 新增的复现镜像（**未实测构建**） | 目前**不承载任何已发表数字** |

---

## 2. `wsl-gcc-13.3`（sanitizer 主环境）

| 项 | 版本 / 值 | 采集命令 |
|---|---|---|
| OS | Ubuntu 24.04.4 LTS (WSL2) | `wsl -e bash -lc "lsb_release -d"` |
| 内核 | `6.18.33.2-microsoft-standard-WSL2` | `wsl -e bash -lc "uname -r"` |
| 架构 | x86_64 | `uname -m` |
| 编译器 | `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` | `wsl -e bash -lc "g++ --version"` |
| stdlib | libstdc++ (GCC 13.3) | — |
| libc | glibc 2.39-0ubuntu8.9 | `ldd --version` |
| sanitizer 运行时 | `libasan.so` / `libubsan.so` / `libtsan.so`（GCC 13，`/usr/lib/gcc/x86_64-linux-gnu/13/`） | 见 `data/692_environment_paired_experiment.json::environment_profiles` |
| 链接器 | GNU ld (GNU Binutils for Ubuntu) 2.42 | `ld --version` |
| 编译旗标 | `-std=c++17 -g -fsanitize=<asset> -fno-omit-frame-pointer` | 692 协议 |
| 优化档 | `-O0` 与 `-O2` **双档** | 692 协议 |
| 超时 | 60 s（进程内） | 692 协议 |
| 支持资产 | asan / ubsan / tsan / compiler-warn / cross-compile / linker | 692 协议 |

> ⚠ **本项目本机测量环境的头号坑（必读）**
> WSL 2.7.10 + 开启 Windows 系统代理时，每次 `wsl.exe` 调用都会向 **stderr** 写一条
> **UTF-16LE 横幅** ⇒ Python `subprocess.run(text=True)` 解码抛异常 ⇒ `stderr` 变 `None`
> ⇒ **走 stderr 的报告（ASan/UBSan）全部丢失** ⇒ 系统性假 miss。
> **解法**：调用前 `export WSL_UTF8=1` 且 `export WSLENV=WSL_UTF8/u`。
> `unset HTTP(S)_PROXY` **没有用**（横幅来自注册表代理配置）。
> 该适配层存在于 673r；`holdout_reveal_3_665 / 4_671a / 5_672h` **没有**，重跑它们前必须先 export。
> 反向坑：ambient `WSL_UTF8=1` 会让 `detect_for_assets.py --check` 的"env 已还原"断言红
> （跑 pytest 时不要带这个变量）。

---

## 3. `windows-native-mingw`（告警 / 交叉编译 / 外部对比）

| 项 | 版本 / 值 | 采集命令 |
|---|---|---|
| OS | Windows 11 (10.0.26200) | `python -c "import platform;print(platform.platform())"` |
| 编译器 A | `g++.exe (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0` | `g++ --version` |
| 编译器 B | `clang version 22.1.8`（MSYS2 mingw64） | `clang++ --version` |
| clang-tidy | LLVM **22.1.8** | `clang-tidy --version` |
| cppcheck | **2.21.0** | `cppcheck --version` |
| cmake | **未安装** | `cmake --version` → command not found |
| valgrind | **未安装**（Windows 无原生支持） | `valgrind --version` → command not found |
| stdlib | libstdc++ (MinGW 13.1.0) | — |
| libc | msvcrt（target `x86_64-w64-mingw32`） | — |
| sanitizer 运行时 | **无**（MinGW 不带 ASan 动态运行时；clang 缺 `libclang_rt.asan_dynamic`，689 已实测登记） | — |
| 编译旗标 | `-std=c++17 -Wall` | 692 协议 |
| 支持资产 | compiler-warn / cross-compile / linker | 692 协议 |

> ⚠ **第二个已知坑**
> **MinGW g++ 13.1 不认 `-Wunsequenced`**（那是 clang 的选项）⇒ 任何用字符串匹配
> `unsequenced` 判定命中的代码都会**恒真**。**已于 673u 批次修复**
> （`holdout_reveal_661.detect` 前置 unrecognized-option ⇒ unknown 拦截）。
> 写新的检测器判据时仍该用 clang++ 或只认 `warning:` 行。

---

## 4. Python 与 pip 包

| 项 | 版本 | 备注 |
|---|---|---|
| 产物生成环境 Python | **3.13.13**（`.venv`） | `requirements.txt` 以此为钉版本口径 |
| 本机系统 Python | 3.13.14 | 与 3.13.13 同为 3.13.x，数字一致 |
| ruff | 0.16.5 | `.venv/Scripts/ruff.exe` |
| mypy | 2.3.1 | `.venv/Scripts/mypy.exe` |

**pip 包全表（`.venv` 实际 freeze，2026-10-08 快照）**

```
appdirs==1.4.4              GitPython==3.1.62          pytest==9.1.1
ast_serialize==0.8.0        hypothesis==6.168.0        pytest-xdist==3.8.0
babel==2.18.0               idna==3.19                 python-bitcoinlib==0.12.2
backrefs==8.0               iniconfig==2.3.0           python-dateutil==2.9.0.post0
beautifulsoup4==4.15.0      Jinja2==3.1.6              PyYAML==6.0.3
certifi==2026.7.22          jsbeautifier==2.0.3        pyyaml_env_tag==1.1
charset-normalizer==3.5.1   librt==0.15.0              requests==2.34.2
click==8.5.0                Markdown==3.10.3           ruff==0.16.5
colorama==0.4.6             MarkupSafe==3.0.3          setuptools==84.0.0
EditorConfig==0.17.1        mergedeep==1.3.4           six==1.17.0
execnet==2.1.2              mkdocs==1.6.1              smmap==5.0.3
ghp-import==2.1.0           mkdocs-get-deps==0.2.2     sortedcontainers==2.4.0
gitdb==4.0.12               mkdocs-material==9.7.7     soupsieve==2.9.2
                            mkdocs-material-extensions==1.3.1   syrupy==6.1.1
                            mkdocs-mermaid2-plugin==1.2.3       typing_extensions==4.16.0
                            mypy==2.3.1                urllib3==2.7.0
                            mypy_extensions==1.1.0     watchdog==6.0.0
                            opentimestamps==0.4.5      Pygments==2.21.0
                            opentimestamps-client==0.7.2        platformdirs==4.11.5
                            packaging==26.3            pluggy==1.6.0
                            paginate==0.5.7            pycryptodomex==3.23.0
                            pathspec==1.1.1            pypdf==6.19.0
                            PySocks==1.7.1             pymdown-extensions==11.0.2
```

> **重要边界**：论文头版数字的**重算**（reveal / stats / counts / 卡计数 / CI）
> **全部只用 Python 标准库**。上面这张表里**没有任何一项是复现论文数字所必需的**；
> 它们服务于测试、类型检查、文档站与时间戳公证。最小复现集合其实是空的。

---

## 5. 已知环境敏感性（哪些实验依赖特定环境）

| 实验 / 数字 | 依赖 | 换环境会怎样 |
|---|---|---|
| asan / ubsan / tsan 检出率 | WSL 的 sanitizer 运行时 | **Windows native 直接系统性假 miss**（MinGW 无运行时） |
| `-Wunsequenced` 资产 | clang 的该选项 | MinGW g++ 恒 `unknown`（673u 已登记，属预期不是 bug） |
| compiler-warn 检出率 | 具体编译器与 `-Wall -Wextra` 档 | 换 GCC 大版本告警集合就变，κ 会漂 |
| cross-compile 资产 | **两个**编译器都存在 | 只有一个 ⇒ 恒 `miss` |
| 优化消除类缺陷（693-A 发现的 C07/C08 型） | `-O0` vs `-O2` | 折叠/死代码删除会让 UBSan/ASan 检查点消失 ⇒ `-O2` 下反而静默 |
| Examples/*.asm 证据 | Windows MinGW GCC **15.3.0**（Intel 语法 / Win64 ABI） | 容器/Linux GCC 产出 AT&T 语法 / Linux ABI，**不可互替** |
| 外部工具公平对比（692-D） | clang-tidy 22.1.8 + cppcheck 2.21.0 on Windows native | 换版本则与论文不可比 |

---

## 6. WSL 配置说明

```bash
# 1) 发行版与内核
wsl -l -v                       # 确认 Ubuntu 为默认发行版、版本为 2
wsl -e bash -lc "uname -r"      # 期望 6.x-microsoft-standard-WSL2

# 2) 工具链
wsl -e bash -lc "sudo apt-get update && sudo apt-get install -y g++ gdb"

# 3) 必做的 UTF-8 横幅规避（否则 ASan/UBSan 报告会静默丢失）
export WSL_UTF8=1
export WSLENV=WSL_UTF8/u

# 4) 自检
bash scripts/verify_environment.sh --profile=wsl-gcc-13.3
```

---

## 7. Docker 复现（**未实测**）

| 项 | 状态 |
|---|---|
| 本机是否安装 Docker | **否**（`docker --version` → `command not found`） |
| `docker/reproduce/Dockerfile` | 已编写，**从未构建过** |
| `docker/reproduce/docker-compose.yml` | 已编写，**从未运行过** |
| `.dockerignore` | 已编写 |
| 校验程度 | 逐行包名核对（Ubuntu 22.04 jammy 仓库存在性）+ 与本文版本表一致性核对 |
| **缺失的证据** | 没有 `docker build` / `docker compose build` 的任何实际输出 |

首次在有 Docker 的机器上执行时请按此顺序：

```bash
bash scripts/verify_environment.sh --profile=docker-ubuntu-22.04   # 先体检
docker compose -f docker/reproduce/docker-compose.yml build
docker compose -f docker/reproduce/docker-compose.yml run --rm verify-env
docker compose -f docker/reproduce/docker-compose.yml run --rm reproduce
```

若构建失败，**请把失败输出原样贴进 issue**，不要改 Dockerfile 里的版本号来"让它过"——
那会把环境锁定文档变成谎言。

---

## 8. 版本采集命令一览（可复算）

```bash
# 本机 Windows
g++ --version | head -1
clang++ --version | head -1
cppcheck --version
clang-tidy --version | head -2
python --version

# WSL
wsl -e bash -lc 'lsb_release -d; uname -r; g++ --version | head -1; ldd --version | head -1; ld --version | head -1'

# 容器（需要 Docker）
docker run --rm queyi-reproduce:693 bash -lc 'gcc --version|head -1; clang --version|head -1; cppcheck --version; valgrind --version'
```
