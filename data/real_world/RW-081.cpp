// RW-081 | CVE-2021-4034 | polkit | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-4034
// project_url: https://gitlab.freedesktop.org/polkit/polkit
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: PwnKit —— pkexec 处理 argc==0 时把 argv[0] 当路径读取，
//   重写 argv[0]/argv[1] 造成越界写（本地提权）。
// notes: 最小重构 —— **用户态复刻** argc==0 参数处理。
#include <cstdio>
#include <cstring>

// BUG: when argc == 0 the loop rewrites argv[1] (== NULL terminator slot),
// turning it into a controlled path string ("GCONV_PATH=."-style injection).
int pkexec_parse(char** argv, int argc) {
    int rewritten = 0;
    // real code: for (n = 1; n < argc; n++) path = argv[n];
    // with argc = 0: n starts at 1, first argc-check is bypassed by the loop shape
    int n = 1;
    while (n < argc || n == 1) {
        argv[n] = (char*)"ATTACKER-ENV=controlled";   // argv[1] == NULL slot rewritten
        ++rewritten;
        if (n >= argc + 1) break;                     // late/incomplete guard
        ++n;
    }
    return rewritten;
}

int main() {
    char a0[] = "pkexec";
    char* argv[3] = {a0, nullptr, nullptr};           // argc == 0 scenario
    int r = pkexec_parse(argv, 0);
    std::printf("rewrote %d arg slot(s); argv[1] now: %s\n", r, argv[1]);
    return 0;
}
