// sample_E186
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E186.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<int> waiting{0};
static void waiter(){
  /*DEFECT: 截止时间点在「还没拿到锁」时就已算好，等真正进 wait 时可能早已过期：
     wait_until 立即返回 no_timeout 之外的状态，而谓词根本没检查 ⇒ 无谓的超时返回被当成「可以继续」 */
  auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds(1);
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  std::cv_status st = cv.wait_until(lk, deadline);
  bool ok = (st == std::cv_status::no_timeout);
  std::printf("E186 ok=%d ready=%d\n", (int)ok, (int)ready);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    ready = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
