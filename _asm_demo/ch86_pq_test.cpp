#include <queue>

// 批 L6：priority_queue 零开销 = vector + 比较器；push=c.push_back+push_heap 上浮
int main() {
    std::priority_queue<int> pq;
    for (int i = 0; i < 100; ++i) pq.push(i);
    volatile int top = pq.top();
    (void)top;
    return 0;
}
