// ⑯-1 ❌ 误以为 monotonic_buffer_resource 会逐个析构元素
#include <memory_resource>
#include <vector>
#include <iostream>
struct File { ~File() { std::cout << "close\n"; } };  // 非平凡析构
int main() {
    char buf[1024];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    {
        std::pmr::vector<File> v(&mr);
        v.emplace_back();   // 分配在 arena
    }                       // 析构 v：vector 仍会逐个析构成员（元素析构照常）
    mr.release();           // 仅归还底层缓冲，不影响"已发生的元素析构"
    return 0;               // ✅ 元素析构在 vector 析构时已发生；release 只是免逐个 free 缓冲
}