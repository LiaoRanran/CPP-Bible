// sample_B098
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B098.json)

#include <cstdio>
struct D { ~D() noexcept(false) { throw 2; } };
int main(){
  try { D d; } catch (...) { } /*DEFECT: destructor throws (UB when unwinding); terminate, no trap */
  std::printf("done\n");
  return 0;
}