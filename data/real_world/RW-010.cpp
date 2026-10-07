// RW-010 | CVE-2016-2107 | OpenSSL | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-2107
// project_url: https://www.openssl.org/
// year: 2016 | severity: HIGH | source_type: cve
// mechanism: AES-NI CBC 路径下填充校验与 MAC 校验的顺序/短路使 padding oracle 成立
//   （密文长度检查发生在 MAC 计算之前的错误位置）。
// notes: 最小重构。信息泄露类逻辑缺陷：内存/UB 检测器全盲。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

// CBC decrypt stub (identity "decrypt" for demonstration purposes only).
std::vector<uint8_t> cbc_decrypt_stub(const std::vector<uint8_t>& ct, uint8_t key) {
    std::vector<uint8_t> pt(ct.size());
    for (size_t i = 0; i < ct.size(); ++i) pt[i] = ct[i] ^ key;
    return pt;
}

// BUG: returns early on padding error BEFORE MAC check, and the timing/error
// distinction is observable by the attacker (padding oracle).
bool decrypt_and_check(const std::vector<uint8_t>& ct, uint8_t key, const std::vector<uint8_t>& mac) {
    std::vector<uint8_t> pt = cbc_decrypt_stub(ct, key);
    uint8_t pad = pt.back();
    if (pad == 0 || pad > 16) {
        return false;               // observable padding failure (oracle!)
    }
    // MAC verification happens only after padding passed
    std::vector<uint8_t> computed(mac.size(), 0);
    for (size_t i = 0; i < mac.size(); ++i) computed[i] = pt[i] ^ 0x5A;
    return std::memcmp(computed.data(), mac.data(), mac.size()) == 0;
}

int main() {
    std::vector<uint8_t> ct(32, 0x00);
    ct.back() = 0x10 ^ 0xA5;                 // craft pad byte to be "valid"
    std::vector<uint8_t> mac(16, 0x11);
    // Attacker iterates ciphertexts and distinguishes "padding ok, mac fail"
    // from "padding fail" -> byte-at-a-time plaintext recovery.
    bool r = decrypt_and_check(ct, 0xA5, mac);
    std::printf("oracle result = %d\n", (int)r);
    return 0;
}
