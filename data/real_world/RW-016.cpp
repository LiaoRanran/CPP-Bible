// RW-016 | CVE-2023-38545 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-38545
// project_url: https://curl.se/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: SOCKS5 握手：目标主机名超长（>255）时本应回退本地解析，
//   但回退路径下已分配缓冲尺寸不足，堆越界写（"让 curl 用恶意 SOCKS5 代理即可触发"）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: buffer sized for a "short" hostname (255) but the slow-path fallback
// copies the full attacker-controlled hostname into it.
std::vector<char> socks5_send_hostname(const char* hostname, bool resolve_locally) {
    std::vector<char> pkt(256);           // 255 + length byte, per SOCKS5 spec
    size_t len = std::strlen(hostname);
    if (len > 255 && resolve_locally) {
        // intended: fall back to local resolution (send address, not name)
        // actual: copies the name anyway -> overflow
        std::memcpy(pkt.data() + 1, hostname, len);
    } else {
        pkt[0] = static_cast<char>(len);
        std::memcpy(pkt.data() + 1, hostname, len);
    }
    return pkt;
}

int main() {
    // curl truncation happens at 65535; a 600-byte host overflows the 256-byte packet
    std::vector<char> big(600, 'h');
    big.push_back('\0');
    std::vector<char> pkt = socks5_send_hostname(big.data(), /*resolve_locally=*/true);
    std::printf("packet size = %zu\n", pkt.size());
    return 0;
}
