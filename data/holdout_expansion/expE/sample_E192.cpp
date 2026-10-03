// sample_E192
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E192.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool one_shot = false;
static std::atomic<int> served{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!one_shot) cv.wait(lk);
  /*DEFECT: 谓词是「一次性信号」，被第一个等待者读走后不复位：
             第二个等待者进入 wait 时谓词已为 true，会立刻通过（虚假通过），
             语义上等于同一份资源被消费两次 */
  served.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void trigger(){
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    one_shot = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter, 1), b(waiter, 2), c(trigger);
  a.join(); b.join(); c.join();
  std::printf("E192 served=%d\n", served.load());
  return 0;
}
