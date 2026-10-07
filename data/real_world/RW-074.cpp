// RW-074 | CVE-2022-0847 | Linux kernel | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-0847
// project_url: https://www.kernel.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: Dirty Pipe —— 管道缓冲 page 的 flags 未初始化（关键：PIPE_BUF_FLAG_CAN_MERGE），
//   后续 splice 写合并把受控数据写入只读页（页面缓存覆写）。
// notes: 最小重构 —— **纯用户态逻辑复刻**（不调用任何内核接口）。展示
//   "未初始化 flags 使写合并判定成立"的缺陷本质。
#include <cstdio>
#include <cstring>

#define PIPE_BUF_FLAG_CAN_MERGE 0x10
#define DEF_FLAGS 0x00

struct PipeBuffer {
    unsigned flags;         // per-page flags: drives merge decision
    char data[64];
    size_t len;
};

struct Pipe {
    PipeBuffer bufs[8];
    size_t n;
};

// BUG: flags of a fresh pipe buffer are *not* initialized to DEF_FLAGS; recycled
// buffers keep CAN_MERGE from the previous (readable) state. If the attacker
// arranges the page to be a file-cache page, their bytes merge into it.
void write_pipe(Pipe& p, const char* src, size_t len, bool init_flags) {
    PipeBuffer& b = p.bufs[p.n % 8];
    if (init_flags) b.flags = DEF_FLAGS;     // correct behavior (after the fix)
    else b.flags = PIPE_BUF_FLAG_CAN_MERGE;  // dirty state left over (vulnerable shape)
    std::memcpy(b.data, src, len);
    b.len = len;
    ++p.n;
}

int main() {
    Pipe p{};
    // attacker first fills the pipe with CAN_MERGE buffers (all flags leak set)
    for (int i = 0; i < 8; ++i) write_pipe(p, "AAAA", 4, /*init_flags=*/false);
    // ... drains them, then splices a read-only file page and writes:
    PipeBuffer& reused = p.bufs[3];
    std::printf("reused buffer flags=0x%02X (CAN_MERGE set => file page writable): %s\n",
                reused.flags,
                (reused.flags & PIPE_BUF_FLAG_CAN_MERGE) ? "YES (bug)" : "no");
    return 0;
}
