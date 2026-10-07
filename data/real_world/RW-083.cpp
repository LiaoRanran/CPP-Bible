// RW-083 | CVE-2019-5596 | FreeBSD | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-5596
// project_url: https://www.freebsd.org/
// year: 2019 | severity: HIGH | source_type: cve
// mechanism: capsicum 能力模式下 F_GETOWN 等 fcntl 请求未受能力检查约束，
//   沙箱内进程可越权获取/影响宿主状态。
// notes: 最小重构（权限判定遗漏）。
#include <cstdio>

struct CapRights {
    bool can_getown;
    bool can_setown;
};

struct CapFd {
    CapRights rights;
    bool in_capability_mode;
};

// BUG: the request switch handles F_GETOWN before validating capability rights
// in capability mode.
bool fcntl_getown_allowed(const CapFd& fd) {
    if (!fd.in_capability_mode) return true;
    // BUG: F_GETOWN path is missing the `if (!rights.can_getown) return false;`
    return true;
}

int main() {
    CapFd fd{{false, false}, true};    // sandboxed, no rights granted
    std::printf("sandboxed F_GETOWN allowed = %s (bug)\n",
                fcntl_getown_allowed(fd) ? "YES" : "no");
    return 0;
}
