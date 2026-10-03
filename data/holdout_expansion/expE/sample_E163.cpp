// sample_E163
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E163.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex hw_lock;
static int reg = 0;
static std::atomic<int> stage{0};
static void device_wait(){
  std::lock_guard<std::mutex> lk(hw_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待外设（sleep 模拟硬件就绪等待） */
  std::this_thread::sleep_for(std::chrono::milliseconds(240));
  reg = 0x1234;
  stage.store(2, std::memory_order_release);
}
static void poll(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 轮询线程（高优先级）等锁读寄存器 */
  std::lock_guard<std::mutex> lk(hw_lock);
  reg |= 0x1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(device_wait), b(poll);
  a.join(); b.join();
  std::printf("E163 reg=%x\n", reg);
  return 0;
}
