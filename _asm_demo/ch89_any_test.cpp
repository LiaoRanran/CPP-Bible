#include <any>
#include <string>

// 批 L8：any SBO 小对象(int)内联存 16B 本体 + any_cast 类型校验；大对象(string)走堆
int main() {
    std::any a = 42;                          // 小对象：SBO 内联，无 operator new
    volatile int v = std::any_cast<int>(a);   // 内联类型校验
    (void)v;
    std::any b = std::string("this string is longer than 16 bytes SBO");  // 大对象：堆分配
    volatile bool ok = b.has_value();
    (void)ok;
    return 0;
}
