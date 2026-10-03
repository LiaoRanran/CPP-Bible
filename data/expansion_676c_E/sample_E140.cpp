// sample_E140
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E140.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<unsigned> global_epoch{0};
static std::atomic<int> step{0}, frees{0};
int main(){
  Node arena[2];
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  std::thread t([&]{
    unsigned e = global_epoch.load(std::memory_order_acquire);
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用「epoch 号相等」当回收安全判据，但 epoch 是有限位宽计数器：
       长时间运行后 epoch 绕回同值，读侧据此认为「没有新 epoch 推进」而错误地允许回收 */
    if (global_epoch.load(std::memory_order_acquire) == e){
      frees.fetch_add(1, std::memory_order_relaxed);
      p->v = 0;                            // 回收：写回槽位
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  global_epoch.store(1, std::memory_order_release);
  global_epoch.store(0, std::memory_order_release);   // epoch 绕回同值
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E140 frees=%d head_v=%d\n", frees.load(), head.load()->v);
  return 0;
}
