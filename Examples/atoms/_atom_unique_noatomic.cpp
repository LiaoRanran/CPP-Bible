// Examples/_atom_unique_noatomic.cpp
// 服务 ATOM-MEM-SHARED-002（第二卡）：unique_ptr 的移动与析构**不含原子操作**——工件里不出现
// 任何 `lock` 前缀指令（与 EV-MEM-034 的引用计数原子操作形成镜像对照）。
// 其"零共享开销"的另一面由类型系统给出：unique_ptr 不可拷贝（拷贝构造被删除），要共享必须显式
// 改用 shared_ptr —— 于是"要不要付原子代价"成了**编译期选择**，而不是运行期祈祷。
// 文件名的历史：原名 _atom_unique_nolock.cpp 含 "nolock" 子串，会被工件的 .file 指令带进工件，
// 使 `absent: "lock"` 这类断言被**文件名**误伤（红队 M4 拦截）；改名为 noatomic 后一条 absent 即可覆盖全形态。
#include <cstdio>
#include <memory>
#include <type_traits>
#include <utility>

static volatile int g_dtor = 0;
static volatile int g_moves = 0;          // volatile：-O2 不可折叠（M2 §5；红队 H1 拦截后的修正）

struct Tracked {
    int v = 0;
    ~Tracked() { g_dtor = g_dtor + 1; }
};

static std::unique_ptr<Tracked> make_one(int v) {
    auto p = std::make_unique<Tracked>();
    p->v = v;
    return p;                                     // 隐式移动（无原子操作、无控制块）
}

int main() {
    std::printf("sizeof unique_ptr=%d\n", (int)sizeof(std::unique_ptr<Tracked>));
    std::printf("copyable=%d\n", (int)std::is_copy_constructible<std::unique_ptr<Tracked>>::value);
    std::printf("movable=%d\n", (int)std::is_move_constructible<std::unique_ptr<Tracked>>::value);

    {
        auto a = make_one(7);
        auto b = std::move(a);                    // 纯指针搬运
        g_moves = g_moves + 1;
        auto c = std::move(b);
        g_moves = g_moves + 1;
        std::printf("value=%d dtor during lifetime=%d\n", c->v, (int)g_dtor);
    }
    std::printf("moves=%d dtor after scope=%d\n", (int)g_moves, (int)g_dtor);
    return 0;
}
