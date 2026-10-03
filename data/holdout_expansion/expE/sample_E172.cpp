// sample_E172
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E172.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int produced = 0, consumed = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 只在进入前检查一次谓词，之后连续 wait 三次都不重新检查：
     第二/三次 wait 可能在条件已满足的情况下仍被唤醒并继续 */
  if (produced < 3) cv.wait(lk);
  cv.wait(lk);
  cv.wait(lk);
  consumed = 3;                        // 未验证 produced 是否真的到 3
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 1; i <= 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      produced = i;
    }
    cv.notify_all();
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(worker), b(producer);
  a.join(); b.join();
  std::printf("E172 produced=%d consumed=%d\n", produced, consumed);
  return 0;
}
