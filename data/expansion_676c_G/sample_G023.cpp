// sample_G023
// defect_type: null_deref
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-3449 (https://nvd.nist.gov/vuln/detail/CVE-2021-3449) [openssl]
// (authoritative annotation in sample_G023.json)
#include <cstdio>
// CVE-2021-3449: 重协商缺少 signature_algorithms 扩展 → NULL 解引用
struct ClientHello {
    const int* sig_algs;   // signature_algorithms 扩展内容
    int        sig_algs_len;
};

static int tls12_choose_sig_alg(const ClientHello* ch) {
    /* DEFECT */ // 原始缺陷: 重协商路径直接使用上次保存的指针, 未检查扩展是否存在
    return ch->sig_algs[0];
}

int main() {
    ClientHello initial{ new int[2]{ 4, 8 }, 2 };   // 首次握手带扩展
    ClientHello renego { 0, 0 };                    // crafted 重协商: 省略扩展
    tls12_choose_sig_alg(&initial);
    tls12_choose_sig_alg(&renego);                  // NULL[0] → SEGV
    delete[] initial.sig_algs;
    return 0;
}
