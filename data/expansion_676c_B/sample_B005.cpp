// sample_B005
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B005.json)

#include <thread>
#include <cstdio>
int* p = nullptr;
void w(){ for (int i = 0; i < 2000000; i++) *p = i; /*DEFECT: data race: concurrent write through p */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)*p; /* racy read through p (also unsynchronized) */ }
int main(){
  int v = 0; p = &v;
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\n", v);
  return 0;
}