#include <string>
const std::string& bad() {
    const std::string& r = std::string("tmp"); // 绑定到临时对象
    return r;                                 // 悬垂引用
}
int main(){ (void)bad(); }
