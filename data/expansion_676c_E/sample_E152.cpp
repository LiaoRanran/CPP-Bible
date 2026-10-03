// sample_E152
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E152.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex log_lock;
static char logbuf[256];
static std::atomic<int> stage{0};
static void flush(){
  std::lock_guard<std::mutex> lk(log_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做长时间「落盘」+ 反复重填缓冲，锁被长时间独占 */
  for (int k = 0; k < 3000; ++k){
    for (int i = 0; i < 256; ++i) logbuf[i] = 'a' + ((k + i) % 26);
    if ((k % 512) == 0) std::this_thread::sleep_for(std::chrono::microseconds(80));
  }
  stage.store(2, std::memory_order_release);
}
static void alert(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级告警线程要等这把锁才能写告警 */
  std::lock_guard<std::mutex> lk(log_lock);
  logbuf[0] = 'Z';
  stage.store(3, std::memory_order_release);
}
static void tail(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级「日志采集」线程绕过锁直接读 logbuf，
     与持锁线程的写在同一时间段内并发访问同一缓冲区 ⇒ 真实数据竞争 */
  int sum = 0;
  for (int k = 0; k < 300000; ++k) sum += logbuf[k % 256];
  std::printf("E152 sum=%d\n", sum);
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(flush), b(alert), c(tail);
  a.join(); b.join(); c.join();
  std::printf("E152 logbuf0=%c\n", logbuf[0]);
  return 0;
}
