// sample_B014
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B014.json)

#include <thread>
#include <cstdio>
int arr[4] = {0};
void f(){ for (int i = 0; i < 2000000; i++) arr[2]++; /*DEFECT: data race on arr[2] */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\n", arr[2]);
  return 0;
}