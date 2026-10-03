// sample_B054
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B054.json)

#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(8);
  int* q = (int*)std::realloc(p, 16); /*DEFECT: if realloc moves, old p lost; here discard p */
  std::printf("%d\n", q ? 1 : 0);
  std::free(q);
  return 0;
}