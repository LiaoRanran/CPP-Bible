// sample_E141
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E141.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static long acc = 0;
static std::atomic<int> stage{0};
static void low_prio(){
  std::lock_guard<std::mutex> lk(m);
  /*DEFECT: 低优先级线程持锁做百万次累加（等价于持锁执行耗时操作）：
     高优先级线程在下面被阻塞，而中优先级线程会抢占本线程 ⇒ 优先级反转三要素齐备 */
  stage.store(1, std::memory_order_release);
  for (long i = 0; i < 3000000; ++i) acc += i % 7;
  stage.store(2, std::memory_order_release);
}
static void high_prio(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程必须等低优先级线程释放锁才能推进 */
  std::lock_guard<std::mutex> lk(m);
  acc += 1;
  stage.store(3, std::memory_order_release);
}
static void mid_prio(){
  while (stage.load(std::memory_order_acquire) < 1){}
  while (stage.load(std::memory_order_acquire) < 2){
    /*DEFECT: 中优先级线程抢占低优先级线程的时间片，进一步推迟锁的释放 */
    std::this_thread::yield();
  }
}
int main(){
  std::thread a(low_prio), b(high_prio), c(mid_prio);
  a.join(); b.join(); c.join();
  std::printf("E141 acc=%ld stage=%d\n", acc, stage.load());
  return 0;
}
