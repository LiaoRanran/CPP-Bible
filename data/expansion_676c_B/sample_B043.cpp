// sample_B043
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B043.json)

#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(4 * sizeof(int));
  p[0] = 1;
  std::printf("%d\n", p[0]);
  /*DEFECT: resource leak: malloc not freed */
  return 0;
}