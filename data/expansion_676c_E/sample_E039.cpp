// sample_E039
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E039.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int wave[8] = {0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<int> seq{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i) wave[i] = i + 700;             // 非原子写
  /*DEFECT: seq 用 acq_rel 做读-改-写，但读侧只 relaxed 读 seq：写侧再强也建立不了与读者的边*/
  seq.fetch_add(1, std::memory_order_acq_rel);
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 读 seq 后读非原子 wave → 数据竞争*/
  while (seq.load(std::memory_order_relaxed) < 1){}
  std::printf("E039 w7=%d\n", wave[7]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
