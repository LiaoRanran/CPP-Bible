// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
struct Bad : std::enable_shared_from_this<Bad> {
  Bad() {
    auto self = shared_from_this(); // <<PLANTED-DEFECT>> 构造函数中调用 shared_from_this（对象尚未被 shared_ptr 管理,2）
    (void)self;
  }
};
int main() {
  auto p = std::make_shared<Bad>();
  std::printf("ok\n");
  return 0;
}
