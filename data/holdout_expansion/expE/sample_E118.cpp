// sample_E118
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E118.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static std::atomic<Cell*> head{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> freed{0};
int main(){
  Cell* c1 = new Cell{1, nullptr};
  Cell* c2 = new Cell{2, c1};
  head.store(c2, std::memory_order_release);
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: h 在 ABA 之后已被释放，读取 h->next 是 use-after-free */
    Cell* nx = h->next;
    std::printf("E118 v=%d\n", h->v);
    head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Cell* taken = head.exchange(nullptr, std::memory_order_acq_rel);
  delete taken;                       // 释放
  head.store(new Cell{9, nullptr});   // 地址可能被复用 ⇒ ABA
  step.store(2, std::memory_order_release);
  a.join();
  delete taken;
  return 0;
}
