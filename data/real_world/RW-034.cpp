// RW-034 | CVE-2018-25032 | zlib | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-25032
// project_url: https://zlib.net/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: deflate 压缩特定"未跟踪块"模式时，sym_buf 写入量超过分配（内存破坏，
//   影响面极广：所有内嵌 zlib 的产品）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct DeflateState {
    size_t pending;        // input bytes pending
    size_t sym_buf_size;   // allocated symbol buffer
    char* sym_buf;
};

// BUG: the "unmatched block" path emits 3 symbols per literal but the buffer was
// sized for 1 symbol per byte; a long run of matches overruns sym_buf.
void deflate_unmatched_run(DeflateState& st, size_t run_len) {
    size_t pos = 0;
    for (size_t i = 0; i < run_len; ++i) {
        // literal + length + distance triple written per input byte
        st.sym_buf[pos++] = 'L';
        if (pos < st.sym_buf_size) st.sym_buf[pos++] = 'M';
        if (pos < st.sym_buf_size) st.sym_buf[pos++] = 'D';
        if (pos >= st.sym_buf_size) break;   // guard added... but literals after the
                                             // break still write: simulate real shape
    }
    // crafted input: literals-only block of exactly the wrong size
    for (size_t i = 0; i < 8; ++i) {
        st.sym_buf[st.sym_buf_size + i] = 'X'; // forced overflow (mirrors 1.2.11 bug)
    }
}

int main() {
    DeflateState st{};
    st.sym_buf_size = 64;
    st.sym_buf = static_cast<char*>(std::malloc(st.sym_buf_size));
    deflate_unmatched_run(st, 40);
    std::printf("deflated with unmatched run\n");
    std::free(st.sym_buf);
    return 0;
}
