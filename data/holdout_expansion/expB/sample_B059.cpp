// sample_B059
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B059.json)

#include <cstdlib>
#include <cstdio>
int main(){
  void* p = std::malloc(1024);
  std::printf("%p\n", p);
  /*DEFECT: resource leak: large malloc not freed */
  return 0;
}