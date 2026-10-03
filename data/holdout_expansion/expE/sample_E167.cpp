// sample_E167
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E167.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex tx_lock;
static char txbuf[512];
static std::atomic<int> stage{0};
static void bulk_tx(){
  std::lock_guard<std::mutex> lk(tx_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做大批量「发送」填充，锁占用时间长 */
  for (int k = 0; k < 20000; ++k)
    for (int i = 0; i < 512; ++i) txbuf[i] = (char)('a' + ((k + i) % 26));
  stage.store(2, std::memory_order_release);
}
static void fast_ack(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 快路径（高优先级）直接写同一发送缓冲区，不取锁 ⇒ 与持锁线程真实数据竞争 */
  for (int k = 0; k < 20000; ++k) txbuf[k % 512] = 'Z';
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(bulk_tx), b(fast_ack);
  a.join(); b.join();
  std::printf("E167 tx0=%c\n", txbuf[0]);
  return 0;
}
