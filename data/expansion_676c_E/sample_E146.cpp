// sample_E146
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E146.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;                       // std::mutex 不提供优先级继承
static int resource = 0;
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 关键区被低优先级线程拉长，而锁本身不提供优先级继承（PI）：
     持锁者被抢占时，锁的优先级不会跟随高优先级等待者提升 */
  for (long i = 0; i < 2000000; ++i) resource += (int)(i & 1);
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程在此阻塞；没有 PI 的话，它的等待无法帮助持锁者尽快退出 */
  std::lock_guard<std::mutex> lk(m);
  resource = -1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  std::printf("E146 resource=%d\n", resource);
  return 0;
}
