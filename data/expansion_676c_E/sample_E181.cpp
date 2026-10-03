// sample_E181
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E181.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int arrived = 0;
static std::atomic<int> left{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词是「arrived >= 3」，但通知方每来一个就 notify_all 一次；
         醒来后若 arrived 仍不满足（因为通知早于 arrived 更新），等待者继续等，
         而最后一次 notify 已经在它重新 wait 之前发完 ⇒ 永久阻塞 */
  while (arrived < 3) cv.wait(lk);
  left.store(1, std::memory_order_release);
}
static void arrivals(){
  for (int i = 0; i < 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++arrived;
    }
    cv.notify_all();
  }
}
int main(){
  std::thread a(waiter), b(arrivals);
  a.join(); b.join();
  std::printf("E181 left=%d arrived=%d\n", left.load(), arrived);
  return 0;
}
