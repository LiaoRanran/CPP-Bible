// sample_E092
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E092.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex acct, ledger;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void read_balance(){
  wait_go();
  std::lock_guard<std::mutex> a(acct);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 读路径 acct->ledger */
  std::lock_guard<std::mutex> l(ledger);
  std::printf("E092 balance read\n");
}
static void write_entry(){
  wait_go();
  std::lock_guard<std::mutex> l(ledger);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 写路径 ledger->acct，与读路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> a(acct);
  std::printf("E092 entry written\n");
}
int main(){
  std::thread a(read_balance), b(write_entry);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
