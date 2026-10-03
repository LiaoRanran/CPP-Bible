// sample_E198
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E198.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool low_water = false, high_water = false;
static std::atomic<int> woke_low{0}, woke_high{0};
static void waiter_low(){
  std::unique_lock<std::mutex> lk(m);
  while (!low_water) cv.wait(lk);
  woke_low.store(1, std::memory_order_release);
}
static void waiter_high(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 同一个 cv 上挂着两个语义不同的谓词（low_water / high_water），
             通知方无法指定唤醒哪一个，只能 notify_all 或赌 notify_one 恰好唤醒对的 */
  while (!high_water) cv.wait(lk);
  woke_high.store(1, std::memory_order_release);
}
static void notifier(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    low_water = true;                  // 只满足 low_water
  }
  cv.notify_one();                     // DEFECT: 可能唤醒的是 high_water 的等待者
}
int main(){
  std::thread a(waiter_low), b(waiter_high), c(notifier);
  a.join(); b.join(); c.join();
  std::printf("E198 low=%d high=%d\n", woke_low.load(), woke_high.load());
  return 0;
}
