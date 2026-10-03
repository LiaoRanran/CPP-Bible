// sample_B012
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B012.json)

#include <thread>
#include <cstdio>
int* gp = nullptr;
void w(){ for (int i = 0; i < 2000000; i++) gp = (int*)&i; /*DEFECT: data race: concurrent pointer assignment */ }
int main(){
  int v = 0;
  std::thread a(w), b([&]{ for (int i=0;i<2000000;i++) (void)gp; }); /* racy read of gp (also unsynchronized) */
  a.join(); b.join();
  std::printf("%d\n", v);
  return 0;
}