// sample_E184
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E184.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool done = false;
static int result = 0;
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait_for 的返回值被丢弃：超时返回后不检查谓词，直接把「还没完成」当成完成 */
  cv.wait_for(lk, std::chrono::milliseconds(20));
  result = done ? 1 : -1;
  std::printf("E184 result=%d done=%d\n", result, (int)done);
}
static void slow(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(200));  // 远超超时时间
  {
    std::lock_guard<std::mutex> lk(m);
    done = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(slow);
  a.join(); b.join();
  return 0;
}
