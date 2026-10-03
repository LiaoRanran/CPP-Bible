// sample_B046
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B046.json)

#include <cstdio>
int main(){
  for (int i = 0; i < 5; i++){
    int* p = new int(i); /*DEFECT: resource leak: per-iteration alloc never freed */
    std::printf("%d\n", *p);
  }
  return 0;
}