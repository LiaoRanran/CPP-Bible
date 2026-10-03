// sample_B097
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B097.json)

#include <cstdio>
int main() noexcept {
  throw 1; /*DEFECT: throwing out of noexcept (UB); std::terminate, no sanitizer trap */
  return 0;
}