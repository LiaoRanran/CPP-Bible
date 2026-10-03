// sample_E104
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E104.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b, c;
static std::atomic<int> held{0}, ready{0};
static void gate(){ while (held.load(std::memory_order_acquire) < 2){} }
static void holder(){
  std::lock_guard<std::mutex> la(a);
  held.fetch_add(1, std::memory_order_release);
  ready.store(1, std::memory_order_release);
  gate();
  /*DEFECT: 路径甲：先单独 lock(a)，再 std::lock(b,c)。
     std::lock 只会为自己参数里的两把键做死锁避免，它看不见「a 已被本线程持有」 */
  std::lock(b, c);
  std::printf("E104 holder done\n");
}
static void packer(){
  while (ready.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 路径乙：先 std::lock(b,c) 一次拿走两把，再单独 lock(a) ⇒ 与甲构成循环等待 */
  std::lock(b, c);
  held.fetch_add(1, std::memory_order_release);
  std::lock_guard<std::mutex> la(a);
  std::printf("E104 packer done\n");
}
int main(){
  std::thread x(holder), y(packer);
  x.join(); y.join();
  return 0;
}
