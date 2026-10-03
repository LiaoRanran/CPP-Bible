// sample_E187
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E187.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool a_done = false, b_done = false;
static std::atomic<int> woke{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (!a_done) cv.wait(lk);
  /*DEFECT: 在 a_done 满足后继续等待 b_done，但通知方对 b_done 的更新与 notify 的顺序
     在某条路径上是「先 notify 后更新」⇒ 这次唤醒看不到 b_done，只能再等，
     而下一次 notify 不保证到来 */
  while (!b_done) cv.wait(lk);
  woke.store(1, std::memory_order_release);
}
static void updater(){
  {
    std::lock_guard<std::mutex> lk(m);
    a_done = true;
  }
  cv.notify_all();                     // 第一次通知（a_done 已更新）
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    b_done = true;
  }
  /*DEFECT: 若 worker 恰好在这次 notify 之后才进入第二次 wait，这次通知就丢了 */
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(updater);
  a.join(); b.join();
  std::printf("E187 woke=%d\n", woke.load());
  return 0;
}
