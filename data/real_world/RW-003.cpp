// RW-003 | CVE-2021-3711 | OpenSSL | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-3711
// project_url: https://www.openssl.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: SM2 解密流程中密文字节长度被转换为 int 后参与缓冲区长度计算，
//   长度不匹配时可写入超出分配大小的缓冲区（堆溢出）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct SM2Ciphertext {
    std::vector<uint8_t> c1; // 65 bytes point
    std::vector<uint8_t> c3; // digest
    std::vector<uint8_t> c2; // encrypted data
};

// BUG: output buffer sized for `declared_len` (attacker-controlled) but copy uses c2.size()
int sm2_decrypt(const SM2Ciphertext& ct, std::vector<uint8_t>& out, int declared_len) {
    out.resize(static_cast<size_t>(declared_len)); // small, e.g. 16
    std::memcpy(out.data(), ct.c2.data(), ct.c2.size()); // copies 48 bytes -> overflow
    return 0;
}

int main() {
    SM2Ciphertext ct{};
    ct.c2.assign(48, 0xAB);      // actual ciphertext payload: 48 bytes
    std::vector<uint8_t> plain;
    int declared_len = 16;       // derived from malformed ASN.1 length fields
    sm2_decrypt(ct, plain, declared_len);
    std::printf("plaintext size = %zu\n", plain.size());
    return 0;
}
