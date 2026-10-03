// sample_E034
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E034.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Job { int id; int prio; };
static std::atomic<Job*> slot{nullptr};
static std::atomic<bool> armed{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void arm(){
  wait_go();
  Job* j = new Job{1, 5};
  j->prio = 9;
  /*DEFECT: slot 用 relaxed exchange 发布：读侧 acquire 的是 armed，对 slot 的发布链无约束*/
  slot.exchange(j, std::memory_order_relaxed);
  armed.store(true, std::memory_order_release);
}
static Job* take(){
  wait_go();
  while (!armed.load(std::memory_order_acquire)){}
  /*DEFECT: 读侧 relaxed 读 slot：与 relaxed exchange 也不构成 synchronizes-with，Job 字段可见性无保证*/
  Job* j = slot.load(std::memory_order_relaxed);
  std::printf("E034 prio=%d\n", j->prio);
  return j;
}
int main(){
  std::thread a(arm), b(take);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
