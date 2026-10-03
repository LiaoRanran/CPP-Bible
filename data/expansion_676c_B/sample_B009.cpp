// sample_B009
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B009.json)

#include <thread>
#include <cstdio>
int* heap = nullptr;
void f(){ for (int i = 0; i < 2000000; i++) *heap = i; /*DEFECT: data race on heap int */ }
int main(){
  int v = 0; heap = &v;
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\n", v);
  return 0;
}