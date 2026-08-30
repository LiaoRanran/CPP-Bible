# CPP-Bible 工具链固定镜像
#
# 钉 GCC 15.3.0 —— 与书内汇编证据(Examples/*.asm)的生成基线(本地 mingw1530 15.3.0)
# 以及 CI compile(GCC-15) 矩阵的主编译器主版本保持一致，保证本地开发与 CI 编译行为一致。
#
# 重要边界：Examples/*.asm 由 **Windows MinGW GCC 15.3.0** 生成（Intel 语法 / Win64 ABI）；
# 本镜像的 Linux GCC 15.3.0 产物为 AT&T 语法 / Linux ABI，不能直接替代 asm 证据重生成。
# 本镜像定位 = 本地编译门禁复现 + 开发环境，不用于重生成 Examples/*.asm
#（asm 重生成仍需本地 mingw1530 15.3.0）。
# 钉 digest 而非仅 tag：tag 可被强制重推指向别的镜像，digest 不可（可复现性
# 与供应链安全）。digest 取自 Docker Hub 官方 API（2026-08-25 快照，多架构
# manifest list，含 12 个平台镜像）：
#   https://hub.docker.com/v2/repositories/library/gcc/tags/15.3.0
# 升级时：重查该 API 取新 digest，并同步改 .github/workflows/ci.yml 的
# compile job container（那里用 `gcc@sha256:` 形式，digest 替代 tag）。
FROM gcc:15.3.0@sha256:8f59ba4bd41dced92b4ab1c0290ae4a6719d286c936f4d25ff75cb689c7c63fe

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        binutils \
        git \
    && rm -rf /var/lib/apt/lists/*

# 工具链自检：确认 gcc/g++ 即 15.3.0
RUN g++ --version | head -1

WORKDIR /workspace

# 与 CI 一致地以非 root 用户运行
RUN useradd -m -s /bin/bash builder && chown -R builder:builder /workspace
USER builder

CMD ["/bin/bash"]
