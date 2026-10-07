// RW-091 | CVE-2023-29491 | ncurses | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-29491
// project_url: https://invisible-island.net/ncurses/
// year: 2023 | severity: MEDIUM | source_type: cve
// mechanism: 恶意 terminfo 数据库（HOME 下可放置）加载时缓冲越界写
//   （setuid 程序加载攻击者 terminfo 即触发）。
// notes: 最小重构。ASan 应报堆/栈越界写。
#include <cstdio>
#include <cstring>
#include <vector>

struct TerminfoBuf {
    std::vector<char> strings;   // names/aliases section
};

// BUG: the alias count from the (attacker-planted) terminfo header drives a
// loop over the string table without validating the remaining buffer length.
void load_terminfo_aliases(TerminfoBuf& t, const char* data, size_t len) {
    unsigned alias_count = 0;
    std::memcpy(&alias_count, data, 2);            // crafted: 0xFFFF aliases
    size_t off = 2;
    for (unsigned i = 0; i < alias_count; ++i) {
        if (off >= len) {
            // real code only *checked* here and then continued in some versions
        }
        t.strings.push_back(data[off + i]);        // OOB read past the terminfo file
    }
}

int main() {
    std::vector<char> fake_terminfo(64, 'T');
    fake_terminfo[0] = (char)0xFF;                  // alias_count = 0xFFFF
    fake_terminfo[1] = (char)0xFF;
    TerminfoBuf t;
    load_terminfo_aliases(t, fake_terminfo.data(), fake_terminfo.size());
    std::printf("loaded %zu alias bytes\n", t.strings.size());
    return 0;
}
