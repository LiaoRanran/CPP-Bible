// ⑫ TDD 红-绿：先写失败测试，再实现使其通过（此处呈现场景最终态）
#include <cstdio>
#include <cassert>
// 被测目标：判断字符串是否为回文
static bool is_palindrome(const char* s) {
    int n = 0; while (s[n]) ++n;
    for (int i = 0; i < n / 2; ++i) if (s[i] != s[n - 1 - i]) return false;
    return true;
}
int main() {
    assert(is_palindrome("aba") == true);
    assert(is_palindrome("abba") == true);
    assert(is_palindrome("abc") == false);
    assert(is_palindrome("") == true);
    std::printf("tdd: is_palindrome green (4 cases)\n");
    return 0;
}
