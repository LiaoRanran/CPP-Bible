// sample_E072
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E072.json)

#include <atomic>
#include <thread>
#include <cstdio>
static const std::atomic<int> cfg{5};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void push_side_effect(){
  wait_go();
  /*DEFECT: const_cast 去掉 const 后对「本来就是 const 的原子对象」做 store：
     该对象可能被放在只读段里，写它是 UB（对 const 对象的非 const 访问）*/
  std::atomic<int>* p = const_cast<std::atomic<int>*>(&cfg);
  p->store(9, std::memory_order_relaxed);
}
int main(){
  std::thread a(push_side_effect);
  go.store(true, std::memory_order_release);
  a.join();
  std::printf("E072 cfg=%d\n", cfg.load());
  return 0;
}
