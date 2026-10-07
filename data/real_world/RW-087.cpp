// RW-087 | CVE-2019-13272 | Linux kernel | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-13272
// project_url: https://www.kernel.org/
// year: 2019 | severity: HIGH | source_type: pwn
// mechanism: ptrace PTRACE_TRACEME + suid 程序的父进程替换检查缺失，
//   可让 suid 进程把提权对象当作调试者（本地提权）。
// notes: 最小重构 —— **用户态复刻**父进程信任判定。
#include <cstdio>
#include <cstring>

struct ProcCreds {
    int uid;
    bool suid;
    char comm[16];
};

struct TraceCtx {
    ProcCreds tracer;
    ProcCreds tracee;
};

// BUG: the "tracer is my parent" check trusts the recorded parent pointer, not
// the current ptraced relationship; a forged parent passes.
bool allow_ptrace_attach(const TraceCtx& ctx, const ProcCreds& claimant) {
    // real bug: `if (task->parent == tracer)` branch lacked a
    // ptrace_may_access() recheck after the parent was replaced
    if (std::strncmp(claimant.comm, ctx.tracee.comm, 8) != 0) {
        return true;   // BUG: mismatched (forged) parent allowed through
    }
    return false;
}

int main() {
    TraceCtx ctx{{1000, false, "attacker"}, {0, true, "suid-binary"}};
    ProcCreds forged{1000, false, "attacker"};
    bool ok = allow_ptrace_attach(ctx, forged);
    std::printf("forged parent can ptrace suid process = %s (bug)\n", ok ? "YES" : "no");
    return 0;
}
