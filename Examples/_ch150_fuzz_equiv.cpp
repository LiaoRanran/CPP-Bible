// ⑩ 模糊测试等价：以固定对抗语料驱动解析器，捕捉越界/崩溃
#include <cstdio>
#include <cstring>
#include <cassert>
// 被测：解析 "key=value"，要求 key 非空且不含 '='
static bool parse(const char* s, char* key, int kcap) {
    int i = 0;
    while (s[i] && s[i] != '=' && i < kcap - 1) { key[i] = s[i]; ++i; }
    key[i] = '\0';
    return i > 0 && s[i] == '=';
}
int main() {
    const char* corpus[] = { "a=1", "=bad", "noeq", "x=y=z", "longkey=val" };
    int ok = 0;
    for (auto* c : corpus) {
        char k[64];
        bool r = parse(c, k, (int)sizeof k);
        assert(std::strlen(k) < sizeof k);  // 永不越界
        ok += r ? 1 : 0;
    }
    std::printf("fuzz-equiv: corpus=%d parsed_ok=%d (no crash)\n", (int)(sizeof(corpus)/sizeof(corpus[0])), ok);
    return 0;
}
