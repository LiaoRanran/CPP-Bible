// ⑧ 集成测试：仓储层 + 服务层协作（自包含，无外部 DB）
#include <cstdio>
#include <map>
#include <string>
#include <cassert>
struct Repo {
    std::map<int, std::string> m;
    void put(int k, const std::string& v) { m[k] = v; }
    std::string get(int k) const { auto it = m.find(k); return it == m.end() ? "" : it->second; }
};
struct UserService { Repo& r; explicit UserService(Repo& r_) : r(r_) {} std::string name(int id) { return r.get(id); } };
int main() {
    Repo repo;
    UserService svc(repo);
    repo.put(1, "alice");
    assert(svc.name(1) == "alice");
    assert(svc.name(2) == "");  // 未注册用户返回空
    std::printf("integration: UserService<->Repo OK (alice, empty)\n");
    return 0;
}
