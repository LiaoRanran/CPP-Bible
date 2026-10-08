# docker/reproduce/Dockerfile — 693-B1：Queyi 全链复现镜像（多阶段构建）
#
# 定位
# ====
# 在一个**与宿主机无关**的 Linux 容器里复现 Queyi 论文的全部**可容器化**实验：
#   * 八资产检测矩阵重算（asan / ubsan / tsan / compiler-warn / cross-compile / linker）
#   * 纯 Python 口径的数字对账（verify_paper_numbers / paper_quality_gate）
#   * 外部工具公平对比（clang-tidy / cppcheck / valgrind）
#
# 明确**不能**在容器内复现的部分（诚实边界，见 docs/ENVIRONMENT.md §5）
# ------------------------------------------------------------------
#   1. Windows-native（MinGW g++ 13.1 / clang 22.1.8）那一支：容器内是 Linux 工具链，
#      环境画像 `windows-native-mingw` 只能在 Windows 宿主机上取。
#   2. `-Wunsequenced` 资产：那是 clang 的选项，且本项目已在 673u 登记
#      "MinGW g++ 不认 -Wunsequenced ⇒ 恒 unknown"；容器内 clang-14 认该选项，
#      因此**容器内该资产的结果与论文口径不可比**，reproduce_all.sh 会默认跳过它。
#   3. Examples/*.asm：由 Windows MinGW GCC 15.3.0 生成（Intel 语法 / Win64 ABI），
#      容器内 Linux GCC 产物为 AT&T 语法 / Linux ABI，不可互替。
#
# ⚠ 未实测登记（693 红线 7）
# -------------------------
# 693 执行环境（Windows 11）**未安装 Docker**（`docker --version` → command not found），
# 因此本 Dockerfile **从未被实际构建过**。它经过：
#   * 逐行包名核对（Ubuntu 22.04 jammy 官方仓库存在性）；
#   * 与 docs/ENVIRONMENT.md 的版本表一致性核对；
# 但**没有** `docker build` 的实际证据。首次构建请先看 `scripts/verify_environment.sh`。
#
# 为什么放 docker/reproduce/ 而不是仓库根
# ---------------------------------------
# 仓库根 `Dockerfile` 已存在且被 CI 引用（gcc:15.3.0 工具链镜像，钉 digest 用于 compile job）。
# 693 不覆写它，避免破坏既有门禁；本镜像独立放在 docker/reproduce/。

# ── Stage 1：toolchain（装编译器与分析器，产出会被 Stage 2 复用）────────────────
FROM ubuntu:22.04 AS toolchain

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

# 基础构建环境。逐包钉版本以确保可复现（jammy 仓库版本，2026-10 快照）。
RUN apt-get update && apt-get install -y --no-install-recommends \
        # ── 编译器 ──
        gcc-12=12.3.0-1ubuntu1~22.04 \
        g++-12=12.3.0-1ubuntu1~22.04 \
        clang-14=1:14.0.0-1ubuntu1.1 \
        # ── 构建系统 ──
        cmake=3.22.1-1ubuntu1.22.04.2 \
        make=4.3-4.1build1 \
        # ── 静态分析 / 外部对比基线（692-D 公平对比用）──
        cppcheck=2.7-0ubuntu2 \
        clang-tidy-14=1:14.0.0-1ubuntu1.1 \
        # ── 动态分析 ──
        valgrind=1:3.18.1-1ubuntu2 \
        # ── Python ──
        python3.10=3.10.12-1~22.04.3 \
        python3-pip=22.0.2+dfsg-1ubuntu0.4 \
        python3-venv=3.10.6-1~22.04.1 \
        # ── 杂项 ──
        ca-certificates \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# 让 gcc/g++/cc/c++ 指向 12（jammy 默认是 11）
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 100 \
    && update-alternatives --install /usr/bin/cc  cc  /usr/bin/gcc-12 100 \
    && update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-12 100 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 100 \
    && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-14 100 \
    && update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-14 100

# 版本自检：装错版本就在这里失败，而不是在实验里静默给错数
RUN gcc --version   | head -1 | grep -q "12.3.0" \
    && g++ --version | head -1 | grep -q "12.3.0" \
    && clang --version | head -1 | grep -q "14.0" \
    && cppcheck --version | grep -q "2.7" \
    && valgrind --version | grep -q "3.18" \
    && python3 --version | grep -q "3.10"

# AddressSanitizer 运行时：gcc-12 的 libasan 随 gcc-12 一起装；这里显式确认可用
RUN printf 'int main(){return 0;}\n' > /tmp/asan_probe.c \
    && gcc-12 -fsanitize=address -fsanitize=undefined /tmp/asan_probe.c -o /tmp/asan_probe \
    && /tmp/asan_probe && echo "asan/ubsan runtime OK" \
    && printf 'int main(){return 0;}\n' > /tmp/tsan_probe.c \
    && gcc-12 -fsanitize=thread /tmp/tsan_probe.c -o /tmp/tsan_probe \
    && /tmp/tsan_probe && echo "tsan runtime OK" \
    && rm -f /tmp/asan_probe* /tmp/tsan_probe*

# ── Stage 2：runtime（只带运行期需要的东西，镜像更小）─────────────────────────
FROM ubuntu:22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # 复现脚本需要的环境变量（scripts/reproduce_all.sh 会读）
    QUEYI_REPRO_ROOT=/workspace \
    QUEYI_SKIP_WUNSEQUENCED=1

# 从 toolchain 阶段复制**已装好的**工具链（而不是重装一遍 ⇒ 两阶段版本必然一致）
COPY --from=toolchain /usr/bin/gcc-12      /usr/bin/gcc-12
COPY --from=toolchain /usr/bin/g++-12      /usr/bin/g++-12
COPY --from=toolchain /usr/lib/gcc/x86_64-linux-gnu/12 /usr/lib/gcc/x86_64-linux-gnu/12
COPY --from=toolchain /usr/bin/cpp-12      /usr/bin/cpp-12
COPY --from=toolchain /usr/libexec/gcc/x86_64-linux-gnu/12 /usr/libexec/gcc/x86_64-linux-gnu/12
COPY --from=toolchain /usr/bin/clang-14    /usr/bin/clang-14
COPY --from=toolchain /usr/lib/llvm-14     /usr/lib/llvm-14
COPY --from=toolchain /usr/bin/clang-tidy-14 /usr/bin/clang-tidy-14
COPY --from=toolchain /usr/bin/cppcheck    /usr/bin/cppcheck
COPY --from=toolchain /usr/bin/valgrind    /usr/bin/valgrind
COPY --from=toolchain /usr/libexec/valgrind /usr/libexec/valgrind
COPY --from=toolchain /usr/bin/cmake       /usr/bin/cmake
COPY --from=toolchain /usr/bin/make        /usr/bin/make

# 运行期依赖（glibc / libstdc++ / Python / sanitizer 运行时）
RUN apt-get update && apt-get install -y --no-install-recommends \
        libstdc++-12-dev=12.3.0-1ubuntu1~22.04 \
        libasan6=12.3.0-1ubuntu1~22.04 \
        libubsan1=12.3.0-1ubuntu1~22.04 \
        libtsan0=12.3.0-1ubuntu1~22.04 \
        libgcc-12-dev=12.3.0-1ubuntu1~22.04 \
        libllvm14=1:14.0.0-1ubuntu1.1 \
        python3.10=3.10.12-1~22.04.3 \
        python3-pip=22.0.2+dfsg-1ubuntu0.4 \
        binutils=2.38-4ubuntu2.6 \
        libc6-dev=2.35-0ubuntu3.8 \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/gcc-12   /usr/bin/gcc \
    && ln -sf /usr/bin/g++-12   /usr/bin/g++ \
    && ln -sf /usr/bin/clang-14 /usr/bin/clang \
    && ln -sf /usr/bin/clang++-14 /usr/bin/clang++ \
    && ln -sf /usr/bin/clang-tidy-14 /usr/bin/clang-tidy

# Python 依赖（锁定：见 requirements.txt）
COPY requirements.txt /workspace/requirements.txt
# requirements.txt 里钉的是本机 3.13 环境的版本；容器内 3.10 只装"纯 Python 且版本无关"
# 的门禁依赖，其余由 reproduce_all.sh 按需装（避免在 3.10 上装 3.13-only 包而整段失败）
RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir pyyaml==6.0.2

WORKDIR /workspace
COPY --chown=root:root . /workspace

# 以非 root 运行（供应链与最小权限）
RUN useradd --create-home --uid 1000 --shell /bin/bash queyi \
    && chown -R queyi:queyi /workspace
USER queyi

ENV PATH="/home/queyi/.local/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/lib/gcc/x86_64-linux-gnu/12:${LD_LIBRARY_PATH}"

# 入口：一键复现（scripts/reproduce_all.sh）
ENTRYPOINT ["/bin/bash", "-lc"]
CMD ["scripts/reproduce_all.sh"]

LABEL org.opencontainers.image.title="queyi-reproduce" \
      org.opencontainers.image.description="Queyi full-chain reproducibility image (untested build, see header)" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.source="https://github.com/LiaoRanran/CPP-Bible" \
      org.opencontainers.image.version="693-B1"
