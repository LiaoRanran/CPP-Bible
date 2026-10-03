// sample_B093
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B093.json)

#include <cstdio>
int main(){
  int* p = nullptr;
  *p = 5; /*DEFECT: null pointer dereference (UB) -> ASan */
  return 0;
}