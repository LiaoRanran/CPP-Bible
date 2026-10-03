// sample_E174
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E174.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int slot = -1;
static int taken = -1;
static std::atomic<int> waiting{0};
static void consumer(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：即使 slot 还没被填，醒来也会直接取走 slot */
  cv.wait(lk);
  taken = slot;                        // slot 可能仍是 -1
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    slot = 42;
  }
  cv.notify_all();                     // DEFECT: 通知与数据准备之间没有内存序约束的配对
}
int main(){
  std::thread a(consumer), b(producer);
  a.join(); b.join();
  std::printf("E174 taken=%d\n", taken);
  return 0;
}
