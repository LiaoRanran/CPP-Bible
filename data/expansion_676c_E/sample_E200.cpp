// sample_E200
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E200.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool shutting_down = false;
static bool workers_stopped = false;
static std::atomic<int> finished{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (!shutting_down) cv.wait(lk);
  /*DEFECT: 被唤醒时 shutting_down 仍可能是 false（通知早于置位）：
             循环会重新 wait，而关停方已经退出 ⇒ 永久阻塞 */
  while (!workers_stopped) cv.wait(lk);
  finished.fetch_add(1, std::memory_order_release);
}
static void shutdown(){
  cv.notify_all();                     // DEFECT: 先唤醒
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    shutting_down = true;              // 后置位
    workers_stopped = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(worker), c(shutdown);
  a.join(); b.join(); c.join();
  std::printf("E200 finished=%d\n", finished.load());
  return 0;
}
