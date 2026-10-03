// sample_E080
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E080.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex engine_lock, plugin_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void engine(){
  wait_go();
  std::lock_guard<std::mutex> e(engine_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 引擎层 engine->plugin */
  std::lock_guard<std::mutex> p(plugin_lock);
  std::printf("E080 engine\n");
}
static void plugin(){
  wait_go();
  std::lock_guard<std::mutex> p(plugin_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 插件层 plugin->engine，与引擎层相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> e(engine_lock);
  std::printf("E080 plugin\n");
}
int main(){
  std::thread a(engine), b(plugin);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
