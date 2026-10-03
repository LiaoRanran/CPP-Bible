// sample_B019
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B019.json)

#include <thread>
#include <cstdio>
int arr[4] = {0};
void f(){ for (int i = 0; i < 2000000; i++) arr[1]++; /*DEFECT: data race on arr[1] */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\n", arr[1]);
  return 0;
}