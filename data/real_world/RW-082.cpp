// RW-082 | CVE-2024-2961 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2024-2961
// project_url: https://www.gnu.org/software/libc/
// year: 2024 | severity: HIGH | source_type: cve
// mechanism: iconv ISO-2022-CN-EXT 转换器对转义序列的目标数估计错误，
//   输出缓冲越界写（PHP 文件读取链一环）。
// notes: 最小重构 —— **用户态复刻**多字节转义序列的写出逻辑。
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: writes the 4-byte escape sequence into a buffer sized with the *input*
// byte count assumption (1 output byte per input byte).
std::vector<char> iconv_iso2022_convert(const std::vector<unsigned char>& in) {
    std::vector<char> out(in.size());              // 1:1 size assumption
    size_t w = 0;
    for (size_t i = 0; i < in.size(); ++i) {
        if (in[i] == 0x1B && i + 3 < in.size()) {  // ESC $ ) X style sequence
            out[w++] = '\x1B';                      // 4 output bytes for 4 input...
            out[w++] = '$';
            out[w++] = ')';
            out[w++] = 'X';                         // state switch; later chars expand
            i += 3;
        } else {
            out[w++] = static_cast<char>(in[i]);
        }
    }
    return out;
}

int main() {
    // crafted: repeated escape sequences that each expand past the 1:1 sizing
    std::vector<unsigned char> in;
    for (int k = 0; k < 8; ++k) {
        in.push_back(0x1B); in.push_back('$'); in.push_back(')'); in.push_back('X');
        in.push_back(0x0E); in.push_back(0x5B);   // SO + shift-in payload
    }
    std::vector<char> out = iconv_iso2022_convert(in);
    std::printf("converted %zu -> %zu (capacity %zu) \n", in.size(), out.size(), in.size());
    return 0;
}
