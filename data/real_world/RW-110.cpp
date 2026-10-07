// RW-110 | CVE-2016-0778 | OpenSSH | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-0778
// project_url: https://www.openssh.com/
// year: 2016 | severity: HIGH | source_type: cve
// mechanism: roaming 客户端（已废弃功能）对服务器位置变更通知处理时
//   堆缓冲区溢出（影响所有默认启用 roaming 的构建）。
// notes: 最小重构。ASan 应报堆越界。
#include <cstdio>
#include <cstring>
#include <vector>

struct RoamingState {
    std::vector<char> host_info;    // updated from server messages
    size_t alloc_size;
};

// BUG: the new host info is copied into the existing buffer without resizing
// when the server sends a longer value than the original.
void update_roaming(RoamingState& rs, const char* new_host) {
    std::memcpy(rs.host_info.data(), new_host, std::strlen(new_host));  // overflow
    (void)rs.alloc_size;
}

int main() {
    RoamingState rs;
    rs.host_info.resize(16);
    rs.alloc_size = 16;
    rs.host_info.assign(16, 'a');
    // crafted server message: 200-byte host field
    char long_host[201];
    std::memset(long_host, 'H', 200);
    long_host[200] = '\0';
    update_roaming(rs, long_host);       // writes 200 bytes into 16
    std::printf("roaming host updated\n");
    return 0;
}
