// sample_E180
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E180.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool shutdown_req = false;
static std::atomic<int> exited{0};
static void worker(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!shutdown_req) cv.wait(lk);
  exited.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void controller(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    shutdown_req = true;
  }
  /*DEFECT: 有两个等待者却只 notify_one：只有一个能被唤醒，另一个永久阻塞 */
  cv.notify_one();
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  cv.notify_one();
}
int main(){
  std::thread a(worker, 1), b(worker, 2), c(controller);
  a.join(); b.join(); c.join();
  std::printf("E180 exited=%d\n", exited.load());
  return 0;
}
