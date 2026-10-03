// sample_E179
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E179.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool batch_done = false;
static std::atomic<int> done_count{0}, wake_count{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!batch_done) cv.wait(lk);
  done_count.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void notifier(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    batch_done = true;
  }
  /*DEFECT: 三个等待者共用一个谓词，却只在「相信一次 notify_one 能唤醒全部」的前提下
     发了三次通知——一旦某次通知在等待者尚未进入 wait 时发出，就永久丢失 */
  for (int i = 0; i < 3; ++i){
    cv.notify_one();
    wake_count.fetch_add(1, std::memory_order_relaxed);
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(waiter, 0), b(waiter, 1), c(waiter, 2), d(notifier);
  a.join(); b.join(); c.join(); d.join();
  std::printf("E179 done=%d wakes=%d\n", done_count.load(), wake_count.load());
  return 0;
}
