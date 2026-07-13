// 文件：Examples/_ch160_overhead.cpp
// 行号：1
// malloc 元数据开销取证：_msize 显示实际分配字节数 >= 请求字节数
#include <cstdio>
#include <cstdlib>
#include <initializer_list>
#include <malloc.h>

int main() {
    // MinGW 下 _msize 返回堆块"可用"大小（含对齐/元数据后的实际占用）
    for (std::size_t req : {1u, 8u, 16u, 33u, 100u}) {
        void* p = std::malloc(req);
        std::size_t usable = _msize(p);
        std::printf("request=%-4zu  _msize(usable)=%-4zu  overhead=%zu bytes\n",
                    req, usable, usable - req);
        std::free(p);
    }
    return 0;
}
