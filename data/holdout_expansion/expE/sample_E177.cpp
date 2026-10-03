// sample_E177
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E177.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int items = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词判断写在循环外：第一次检查通过后，后续的 wait 就不再验证条件，
     醒来即认为条件成立 */
  if (items > 0){
    cv.wait(lk);
  }
  std::printf("E177 items=%d\n", items);
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    items = 3;
  }
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(producer);
  a.join(); b.join();
  return 0;
}
