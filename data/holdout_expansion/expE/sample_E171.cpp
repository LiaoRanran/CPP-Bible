// sample_E171
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E171.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static int work_done = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：虚假唤醒（或过早的 notify）会让线程在 ready 仍为 false 时继续执行 */
  cv.wait(lk);
  work_done = 1;                       // 资源其实还没准备好
}
static void waker(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  /*DEFECT: 此刻 ready 仍是 false（数据还没就绪），却发了通知 */
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(waker);
  a.join(); b.join();
  std::printf("E171 work_done=%d ready=%d\n", work_done, (int)ready);
  return 0;
}
