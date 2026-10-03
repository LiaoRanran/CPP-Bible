// sample_E155
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E155.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex dev_lock;
static int dev_regs[8] = {0};
static std::atomic<int> in_isr{0}, stage{0};
static void driver_thread(){
  std::lock_guard<std::mutex> lk(dev_lock);
  in_isr.store(1, std::memory_order_release);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 驱动持锁做一长串寄存器访问，锁被长时间占用 */
  for (int k = 0; k < 200000; ++k)
    for (int i = 0; i < 8; ++i) dev_regs[i] += k;
  stage.store(2, std::memory_order_release);
}
static void isr_like(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 「中断服务程序」在用户态用线程模拟，却直接获取驱动正在持有的用户态锁：
     真实系统里中断上下文获取可能被中断的锁 ⇒ 锁顺序反转 / 系统级卡死 */
  std::lock_guard<std::mutex> lk(dev_lock);
  dev_regs[0] = 0xFF;
}
static void deferred(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 延后处理线程无锁写同一寄存器组，与驱动线程并发 ⇒ 真实数据竞争 */
  for (int k = 0; k < 200000; ++k) dev_regs[7] ^= k;
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(driver_thread), b(isr_like), c(deferred);
  a.join(); b.join(); c.join();
  std::printf("E155 r0=%d in_isr=%d\n", dev_regs[0], in_isr.load());
  return 0;
}
