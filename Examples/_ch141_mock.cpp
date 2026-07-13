// Examples/_ch141_mock.cpp
// DI 与测试：通过注入“假实现”（mock/fake）隔离被测对象，无需真实数据库/网络。
#include <cassert>
#include <memory>
#include <string>

struct IUserRepo {
    virtual ~IUserRepo() = default;
    virtual std::string name(int id) = 0;
};
struct DbUserRepo : IUserRepo {        // 真实实现（连库）
    std::string name(int id) override { return "db#" + std::to_string(id); }
};
struct FakeUserRepo : IUserRepo {      // 测试替身（test double）
    std::string name(int id) override { return "fake#" + std::to_string(id); }
};

class UserService {
    std::unique_ptr<IUserRepo> repo_;
public:
    explicit UserService(std::unique_ptr<IUserRepo> r) : repo_(std::move(r)) {}
    std::string greeting(int id) { return "Hi " + repo_->name(id); }
};

int main() {
    UserService sut(std::make_unique<FakeUserRepo>());   // ✅ 注入 fake，单测无副作用
    assert(sut.greeting(1) == "Hi fake#1");
}
