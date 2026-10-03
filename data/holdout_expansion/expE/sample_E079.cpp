// sample_E079
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E079.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex data_lock, meta_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void cache_flush(){
  wait_go();
  std::lock_guard<std::mutex> d(data_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 刷新路径 data->meta */
  std::lock_guard<std::mutex> m(meta_lock);
  std::printf("E079 flushed\n");
}
static void side_read(){
  wait_go();
  std::lock_guard<std::mutex> m(meta_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 旁路读取路径 meta->data，与刷新路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> d(data_lock);
  std::printf("E079 read side\n");
}
int main(){
  std::thread a(cache_flush), b(side_read);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
