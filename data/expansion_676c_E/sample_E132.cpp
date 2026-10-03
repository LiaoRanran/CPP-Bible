// sample_E132
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E132.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; int gen; Node* next; };
static Node arena[2];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, read_gen{0};
int main(){
  arena[0].v = 1; arena[0].gen = 100; arena[0].next = nullptr;
  top.store(&arena[0], std::memory_order_release);
  std::thread a([&]{
    Node* p = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 只凭地址判断「还是同一个节点」：其实 gen 字段已经从 100 变成 200，
       消费者以为在读原来的对象，读到的是被复用后的新对象（ABA 的内容维度） */
    read_gen.store(p->gen, std::memory_order_relaxed);
    std::printf("E132 v=%d gen=%d\n", p->v, p->gen);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(nullptr, std::memory_order_release);
  arena[0].v = 2; arena[0].gen = 200;          // 同址复用，内容全变
  top.store(&arena[0], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E132 read_gen=%d\n", read_gen.load());
  return 0;
}
