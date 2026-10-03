// sample_B010
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B010.json)

#include <thread>
#include <cstdio>
int g = 0;
void f(int n){ for (int i = 0; i < n; i++) g++; /*DEFECT: data race on g (passed-by-value count) */ }
int main(){
  std::thread a(f, 2000000), b(f, 2000000);
  a.join(); b.join();
  std::printf("%d\n", g);
  return 0;
}