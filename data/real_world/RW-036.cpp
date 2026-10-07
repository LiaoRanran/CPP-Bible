// RW-036 | CVE-2016-10087 | libpng | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-10087
// project_url: http://www.libpng.org/pub/png/libpng.html
// year: 2016 | severity: MEDIUM | source_type: cve
// mechanism: png_set_text_2 对无压缩文本块（ztxt/itxt）处理时，畸形块使内部
//   指针为空仍被解引用。
// notes: 最小重构。ASan/UBSan 命中 NULL 解引用。
#include <cstdio>
#include <cstring>

struct PngText {
    char* key;
    char* text;          // null for malformed (missing data field) chunks
    int compression;
};

// BUG: assumes `text` is present, dereferences without check.
int png_set_text_2(PngText* txt, int n) {
    int total = 0;
    for (int i = 0; i < n; ++i) {
        total += static_cast<int>(std::strlen(txt[i].text)); // NULL deref if text == nullptr
    }
    return total;
}

int main() {
    PngText texts[2];
    texts[0].key = (char*)"Comment";
    texts[0].text = (char*)"a comment";
    texts[0].compression = 0;
    texts[1].key = (char*)"ztxt-malformed";
    texts[1].text = nullptr;      // crafted chunk without the data payload
    texts[1].compression = 1;
    int n = png_set_text_2(texts, 2);
    std::printf("text chars = %d\n", n);
    return 0;
}
