// sample_E051
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E051.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int table[4] = {10, 20, 30, 40};
static std::atomic<int*> cur{table};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void shifter(){
  wait_go();
  int* p = cur.load(std::memory_order_relaxed);
  /*DEFECT: 对原子指针做无边界检查的算术并写回：越出 table 的 4 个元素之外*/
  cur.store(p + 9, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  while (cur.load(std::memory_order_relaxed) == table){}
  /*DEFECT: 读侧直接解引用越界指针 → 越界访问*/
  std::printf("E051 v=%d\n", *cur.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(shifter), b(reader);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
