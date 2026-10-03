// sample_E150
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E150.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static int state = 0;
static std::atomic<int> stage{0};
static void io_holder(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁进入阻塞等待（等价于持锁做 socket recv / 磁盘读）：
     阻塞期间锁一直被占用，高优先级线程只能干等 */
  std::this_thread::sleep_for(std::chrono::milliseconds(300));
  state = 1;
  stage.store(2, std::memory_order_release);
}
static void urgent(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等这把锁才能推进状态机 */
  std::lock_guard<std::mutex> lk(m);
  state = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(io_holder), b(urgent);
  a.join(); b.join();
  std::printf("E150 state=%d\n", state);
  return 0;
}
