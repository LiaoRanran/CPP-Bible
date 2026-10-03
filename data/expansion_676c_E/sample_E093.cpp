// sample_E093
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E093.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex file_lock, meta_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void upload(){
  wait_go();
  std::lock_guard<std::mutex> f(file_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 上传路径 file->meta */
  std::lock_guard<std::mutex> m(meta_lock);
  std::printf("E093 uploaded\n");
}
static void scan(){
  wait_go();
  std::lock_guard<std::mutex> m(meta_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 扫描路径 meta->file，与上传路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> f(file_lock);
  std::printf("E093 scanned\n");
}
int main(){
  std::thread a(upload), b(scan);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
