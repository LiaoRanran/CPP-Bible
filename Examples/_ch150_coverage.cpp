// ⑦ 分支覆盖率：sign() 的 pos/neg/zero 三条分支均被覆盖
#include <cstdio>
#include <cstring>
#include <cassert>
static const char* sign(int x) { return x > 0 ? "pos" : (x < 0 ? "neg" : "zero"); }
int main() {
    assert(std::strcmp(sign(5), "pos") == 0);
    assert(std::strcmp(sign(-3), "neg") == 0);
    assert(std::strcmp(sign(0), "zero") == 0);
    std::printf("coverage: sign() branches pos/neg/zero all hit\n");
    return 0;
}
