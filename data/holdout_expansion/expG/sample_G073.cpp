// sample_G073
// defect_type: stack_overflow_write
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-4034 (https://nvd.nist.gov/vuln/detail/CVE-2021-4034) [polkit]
// (authoritative annotation in sample_G073.json)
#include <cstdio>
// CVE-2021-4034: argc==0 时 envp 被当作 argv 使用 → 越界写
static int pkexec_main(int argc, char** envp) {
    char* local_argv[1];      // argc==0: argv 数组实际没有可用槽位
    int n = 0;
    if (argc == 0) {
        /* DEFECT */ // 原始缺陷: 未处理 argc==0, 继续枚举 argv[1..] —— 实际读到 envp 区
        // 简化镜像: 把 envp 字符串写入本地 argv 槽位(模拟对 argv 区的越界写)
        for (n = 0; envp[n]; ++n)
            local_argv[n] = envp[n];          // n>=1 越过 1 槽数组 → 栈越界写
    }
    return n;
}

int main() {
    char* env[] = { "PATH=/usr/bin", "LD_PRELOAD=/tmp/evil.so", "X=1", 0 };
    std::printf("written=%d\n", pkexec_main(0, env));   // 3 个字符串写入 1 槽数组
    return 0;
}
