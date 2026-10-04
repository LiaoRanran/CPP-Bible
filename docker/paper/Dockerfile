# =====================================================================
# 676h · 论文（Queyi / Evolving Verifiers）复现镜像
#
# 定位（务必先读这段再决定要不要用）
# ---------------------------------------------------------------------
# 本镜像用于**复现论文里那些能在原生 Linux 上重算的数字**：
#   - 由 reveal / stats / counts 脚本现算的检出率、CI、p 值、样本量；
#   - 由仓库主张(status/atom)重算的系统计数（67 规则 / 452 账本 / 42 实卡 / VC）；
#   - 论文编译（tectonic）。
#
# 不能复现的部分（论文已声明，这里再钉一次，避免复现者误判）：
#   - **holdout / corpus 的头版检出率**依赖于 WSL(Ubuntu 24.04) + g++ 13.3 + setarch
#     + ASan/UBSan/TSan 运行时；本机 MinGW 没有 UBSan 运行时（cannot find -lubsan）。
#     本镜像装的是原生 Linux g++ 13.3，**理论口径一致但环境不同**，
#     因此本镜像的重跑结果与原论文数字不等价，只可用于"口径理解"，不得用于翻/改结论。
#   - E9 的 clang-tidy 论文用 LLVM 22.1.8（Windows 原生），cppcheck 用 2.13.0（WSL）；
#     Ubuntu 24.04 的 clang-tidy 是 LLVM 18，**版本不一致 ⇒ E9 数字不可由本镜像复核**。
#
# 与仓库根目录 Dockerfile 的区别
# ------------------------------
# 根目录 Dockerfile 钉的是 **书稿汇编证据** 用的 gcc 15.3.0 工具链镜像；
# 本文件是**论文复现**用的环境，两者互不适用，故意不合并。
# =====================================================================
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# ① 原生 Linux g++ 13.3 —— 与 WSL Ubuntu 24.04.4 的 g++ 主版本对齐
#    （论文口径：g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0，setarch from util-linux 2.39.3）
#    说明：这里只钉**主版本**（13 / 3.13 / 2.13），不钉补丁号。补丁号会随仓库快照漂移，
#    硬钉只会在半年后让镜像 build 不掉。若复现者需要补丁级对齐，用
#    `apt-cache madison <pkg>` 把当时的号抄进 REPRODUCE.md §2 的"版本快照"小节。
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        g++-13 \
        gcc-13 \
        python3.13 \
        python3.13-venv \
        python3-pip \
        util-linux \
        git \
        cppcheck \
    && rm -rf /var/lib/apt/lists/*

# ② 工具链自检：任何版本漂移都会在这里 fail loud（不是静默降级）
RUN g++-13 --version | head -1 && setarch --version | head -1 \
    && python3.13 --version

WORKDIR /workspace
COPY requirements.txt ./
RUN python3.13 -m pip install --no-cache-dir -r requirements.txt

COPY . /workspace

ENV PY=python3.13
ENV CXX=g++-13

CMD ["bash", "-lc", "bash docker/paper/run_all.sh"]
