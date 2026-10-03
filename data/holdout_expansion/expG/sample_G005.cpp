// sample_G005
// defect_type: double_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2014-3505 (https://nvd.nist.gov/vuln/detail/CVE-2014-3505) [openssl]
// (authoritative annotation in sample_G005.json)
#include <cstdio>
#include <cstring>
// CVE-2014-3505: DTLS 握手分片错误路径 double free
struct HmFragment {
    unsigned char* frag;
    int            frag_len;
};

static void dtls1_hm_fragment_free(HmFragment* f) {
    if (!f) return;
    delete[] f->frag;
    delete f;
}

static int dtls1_process_fragment(bool crafted_error) {
    HmFragment* f = new HmFragment{ new unsigned char[256], 256 };
    std::memset(f->frag, 0, 256);

    if (crafted_error) {
        dtls1_hm_fragment_free(f);     // 错误路径第一次释放
        std::printf("fragment error path: freed once\n");
        /* DEFECT */
    }
    // 公共清理路径不区分错误与否, 再次释放 → double free
    dtls1_hm_fragment_free(f);
    return 0;
}

int main() {
    dtls1_process_fragment(true);   // crafted DTLS 分片 → 错误路径 + 公共清理 = 双重释放
    return 0;
}
