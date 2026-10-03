// sample_B003
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B003.json)

#include <thread>
#include <cstdio>
struct Counter { int x = 0; };
Counter c;
void f(){ for (int i = 0; i < 2000000; i++) c.x++; /*DEFECT: data race on member c.x */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\n", c.x);
  return 0;
}