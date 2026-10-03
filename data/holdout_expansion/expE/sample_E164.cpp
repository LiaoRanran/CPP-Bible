// sample_E164
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E164.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <functional>
#include <cstdio>
static std::mutex m;
static int state = 0;
static std::atomic<int> stage{0};
static std::function<void()> on_commit;
static void commit(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁调用外部回调，回调内部会发起「阻塞式」请求 */
  on_commit();
  stage.store(2, std::memory_order_release);
}
static void urgent(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁 */
  std::lock_guard<std::mutex> lk(m);
  state = 5;
  stage.store(3, std::memory_order_release);
}
int main(){
  on_commit = []{ std::this_thread::sleep_for(std::chrono::milliseconds(160)); };
  std::thread a(commit), b(urgent);
  a.join(); b.join();
  std::printf("E164 state=%d\n", state);
  return 0;
}
