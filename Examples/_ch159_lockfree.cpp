// 文件：Examples/_ch159_lockfree.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_lockfree.cpp -o Examples/_ch159_lockfree.exe
// 说明：Vyukov 有界 MPMC 无锁环形队列（教学正确实现，非阻塞）。
#include <atomic>
#include <cstdio>
#include <thread>
#include <vector>

template <typename T>
class MPMCRing {
    struct Cell {
        std::atomic<size_t> seq;
        T data;
    };
    std::vector<Cell> buf_;
    size_t cap_;
    std::atomic<size_t> enq_{0};
    std::atomic<size_t> deq_{0};

public:
    explicit MPMCRing(size_t cap) : cap_(cap), buf_(cap) {
        for (size_t i = 0; i < cap; ++i)
            buf_[i].seq.store(i, std::memory_order_relaxed);
    }
    bool enqueue(const T& v) {
        Cell* c;
        size_t pos = enq_.load(std::memory_order_relaxed);
        for (;;) {
            c = &buf_[pos % cap_];
            size_t s = c->seq.load(std::memory_order_acquire);
            long long diff = (long long)s - (long long)pos;
            if (diff == 0) {
                if (enq_.compare_exchange_weak(pos, pos + 1,
                                               std::memory_order_relaxed))
                    break;
            } else if (diff < 0) {
                return false;  // 满
            } else {
                pos = enq_.load(std::memory_order_relaxed);
            }
        }
        c->data = v;
        c->seq.store(pos + 1, std::memory_order_release);
        return true;
    }
    bool dequeue(T& v) {
        Cell* c;
        size_t pos = deq_.load(std::memory_order_relaxed);
        for (;;) {
            c = &buf_[pos % cap_];
            size_t s = c->seq.load(std::memory_order_acquire);
            long long diff = (long long)s - (long long)(pos + 1);
            if (diff == 0) {
                if (deq_.compare_exchange_weak(pos, pos + 1,
                                               std::memory_order_relaxed))
                    break;
            } else if (diff < 0) {
                return false;  // 空
            } else {
                pos = deq_.load(std::memory_order_relaxed);
            }
        }
        v = c->data;
        c->seq.store(pos + cap_, std::memory_order_release);
        return true;
    }
};

int main() {
    MPMCRing<int> q(8);
    std::thread prod([&] {
        for (int i = 0; i < 1000; ++i) {
            while (!q.enqueue(i)) {
            }  // 自旋直到有空位（演示用）
        }
    });
    int sum = 0, cnt = 0;
    std::thread cons([&] {
        int v;
        while (cnt < 1000) {
            if (q.dequeue(v)) {
                sum += v;
                ++cnt;
            }
        }
    });
    prod.join();
    cons.join();
    std::printf("lockfree sum=%d cnt=%d (expect 499500)\n", sum, cnt);
}
