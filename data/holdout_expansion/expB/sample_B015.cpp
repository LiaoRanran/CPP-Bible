// sample_B015
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B015.json)

#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race (RMW) */ }
int main(){
  std::thread a(f);
  std::thread b(f);
  a.join(); b.join();
  std::printf("%d\n", g);
  return 0;
}