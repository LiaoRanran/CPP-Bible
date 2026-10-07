// RW-063 | CVE-2022-1552 | PostgreSQL | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-1552
// project_url: https://www.postgresql.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: autovacuum 以更高权限执行用户可创建的维护函数（security definer 语义
//   被绕过），普通用户借此提权。
// notes: 最小重构（权限判定逻辑缺陷，不涉及内存安全）。
#include <cstdio>
#include <string>

enum Role { ROLE_ATTACKER = 0, ROLE_TABLE_OWNER = 1, ROLE_SUPERUSER = 2 };

struct MaintenanceJob {
    std::string function_owner;
    Role executor_role;      // role the job runs as
    bool user_supplied_fn;   // attacker-created maintenance function
};

// BUG: job runs as its *recorded* executor role (superuser inherited from
// autovacuum) even when the function body was supplied by a lesser role.
Role effective_role(const MaintenanceJob& job) {
    if (job.user_supplied_fn) {
        return job.executor_role;   // BUG: should downgrade to function owner
    }
    return ROLE_TABLE_OWNER;
}

int main() {
    MaintenanceJob job{"attacker", ROLE_SUPERUSER, true};
    Role r = effective_role(job);
    std::printf("attacker maintenance fn runs as ROLE=%d (2=superuser)\n", (int)r);
    return 0;
}
