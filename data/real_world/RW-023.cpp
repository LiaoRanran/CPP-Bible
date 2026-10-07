// RW-023 | CVE-2021-23017 | nginx | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-23017
// project_url: https://nginx.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: resolver 解析 CNAME 时，DNS 应答中的压缩指针指向自身/越界，
//   名称解压导致 1 字节堆越界写（off-by-one）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write（1 byte）。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct DnsNameCtx {
    const uint8_t* msg;      // full DNS message
    size_t msg_len;
    size_t cursor;           // points into msg
};

// BUG: when a compression pointer chains back one byte before the name start,
// the off-by-one calculation writes one byte past the allocated name buffer.
std::vector<char> decompress_name(DnsNameCtx& ctx, size_t name_start) {
    size_t out_cap = 64;
    std::vector<char> name(out_cap);
    size_t out_len = 0;

    // crafted pointer: 0xC0 prefix with offset == name_start - 1
    uint16_t ptr_off = static_cast<uint16_t>(name_start - 1);
    uint8_t lo = static_cast<uint8_t>(ptr_off & 0xFF);

    // copy the raw label bytes the pointer "resolves" to (one byte before start)
    size_t src = ptr_off;
    while (src < ctx.msg_len && ctx.msg[src] != 0 && out_len < out_cap) {
        name[out_len++] = static_cast<char>(ctx.msg[src++]);
    }
    name[out_len] = '\0';                    // off-by-one: index out_len == out_cap
    (void)lo;
    return name;
}

int main() {
    uint8_t msg[80];
    std::memset(msg, 'a', sizeof(msg));
    msg[79] = 0;
    DnsNameCtx ctx{msg, sizeof(msg), 0};
    // name starts at 64; pointer resolves at 63 -> 64 bytes of label + terminator
    std::vector<char> n = decompress_name(ctx, 64);
    std::printf("name len=%zu\n", n.size());
    return 0;
}
