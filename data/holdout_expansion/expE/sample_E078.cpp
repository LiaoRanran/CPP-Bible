// sample_E078
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E078.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex out_lock, cfg_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void log_path(){
  wait_go();
  std::lock_guard<std::mutex> o(out_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 日志路径 out->cfg */
  std::lock_guard<std::mutex> c(cfg_lock);
  std::printf("E078 logged\n");
}
static void cfg_path(){
  wait_go();
  std::lock_guard<std::mutex> c(cfg_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 配置路径 cfg->out，与日志路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> o(out_lock);
  std::printf("E078 cfg applied\n");
}
int main(){
  std::thread a(log_path), b(cfg_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
