// sample_B049
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B049.json)

#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(sizeof(int));
  *p = 7; /*DEFECT: resource leak: malloc not freed */
  std::printf("%d\n", *p);
  return 0;
}
