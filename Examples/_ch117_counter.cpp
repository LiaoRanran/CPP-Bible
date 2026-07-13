// ⑱ 计数器类：观测拷贝/移动次数（调试利器）
#include <cstdio>

struct Tracer {
    static int copies;
    static int moves;
    int id;
    Tracer(int i = 0) : id(i) {}
    Tracer(const Tracer& o) : id(o.id) { ++copies; std::printf("copy#%d\n", copies); }
    Tracer(Tracer&& o)      : id(o.id) { ++moves;  std::printf("move#%d\n", moves); }
};

int Tracer::copies = 0;
int Tracer::moves   = 0;

Tracer build() {
    Tracer t(42);
    return t;           // NRVO：copies/moves 都为 0
}

int main() {
    Tracer x = build();
    std::printf("copies=%d moves=%d\n", Tracer::copies, Tracer::moves);
    return x.id;
}
