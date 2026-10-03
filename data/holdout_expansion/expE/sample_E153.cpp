// sample_E153
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E153.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex q_lock;
static int queue_len = 0;
static std::atomic<int> stage{0};
static void producer(){
  std::lock_guard<std::mutex> lk(q_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待下游消费（背压），锁在阻塞期间一直被占 */
  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  queue_len += 10;
  stage.store(2, std::memory_order_release);
}
static void urgent_producer(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 紧急生产者等同一把锁 */
  std::lock_guard<std::mutex> lk(q_lock);
  queue_len += 1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(producer), b(urgent_producer);
  a.join(); b.join();
  std::printf("E153 qlen=%d\n", queue_len);
  return 0;
}
