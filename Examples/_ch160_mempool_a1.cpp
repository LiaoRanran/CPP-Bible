#include <iostream>
#include <iomanip>
#include <cstdint>
#include <chrono>
#include <vector>
#include <new>

int main() {
    constexpr int N = 100'000;
    std::vector<void*> p(N, nullptr);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) p[i] = ::operator new(32);
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) ::operator delete(p[i]);
    auto t2 = std::chrono::steady_clock::now();
    double ms_new = std::chrono::duration<double, std::milli>(t1 - t0).count()
                  + std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::cout << "default new/delete: " << std::fixed << std::setprecision(3) << ms_new << " ms" << std::endl;

    struct Node { Node* next; };
    std::vector<Node> nodes(N);
    for (int i = 0; i < N; ++i) nodes[i].next = (i + 1 < N) ? &nodes[i + 1] : nullptr;
    Node* fl = &nodes[0];
    auto t3 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { Node* n = fl; fl = n->next; p[i] = n; }
    auto t4 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { Node* n = static_cast<Node*>(p[i]); n->next = fl; fl = n; }
    auto t5 = std::chrono::steady_clock::now();
    double ms_pool = std::chrono::duration<double, std::milli>(t4 - t3).count()
                   + std::chrono::duration<double, std::milli>(t5 - t4).count();
    std::cout << "fixed-size pool:    " << ms_pool << " ms" << std::endl;
    return 0;
}