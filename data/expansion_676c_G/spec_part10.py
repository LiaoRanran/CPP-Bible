# -*- coding: utf-8 -*-
# 676c-G spec part10: curl miss 组 II + SQLite asan 组 (G049-G054)
PART = [
("G049", dict(
  defect_type="logic_error", func="url_parse_host_percent", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-27780", url="https://nvd.nist.gov/vuln/detail/CVE-2022-27780",
           project="curl", commit="", simplification="剥离 URL 解析器全流程，保留『主机名部分百分号编码分隔符被错误解码』核心缺陷"),
  trigger="主机名含 %2F，解码后 URL 与解析时被视为不同主机",
  notes="CVE-2022-27780: 百分号编码分隔符使主机名解析不一致（CVE 描述: wrongly accepts percent-encoded URL separators like '/' when decoding the host name part ... making it a *different* URL using the wrong host name, CWE-177）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2022-27780: 主机名百分号解码产生与解析时不同的 URL
static std::string percent_decode_host(const std::string& host) {
    std::string out;
    for (size_t i = 0; i < host.size(); ++i) {
        /* DEFECT */ // 原始缺陷: 主机名部分的 %2F 被解码为 '/', 生成另一个 URL
        if (host[i] == '%' && i + 2 < host.size() &&
            host[i + 1] == '2' && (host[i + 2] == 'F' || host[i + 2] == 'f')) {
            out += '/';
            i += 2;
        } else {
            out += host[i];
        }
    }
    return out;
}

int main() {
    std::string parsed_host = "example.com%2F127.0.0.1";   // 解析时视作单一主机
    std::string used_host = percent_decode_host(parsed_host);
    std::printf("解析时主机: %s\n实际连接主机: %s\n(正确行为: 两者必须一致)\n",
                parsed_host.c_str(), used_host.c_str());
    return 0;
}
'''),

("G050", dict(
  defect_type="logic_error", func="cert_reuse_credential_check", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-7141", url="https://nvd.nist.gov/vuln/detail/CVE-2016-7141",
           project="curl", commit="", simplification="剥离 NSS/PEM 后端，保留『连接复用未校验客户端证书状态 → 认证被劫持』核心缺陷"),
  trigger="新连接未配置客户端证书，复用了此前从文件加载证书的连接",
  notes="CVE-2016-7141: 连接复用劫持客户端证书认证（CVE 描述: allow remote attackers to hijack the authentication of a TLS connection by leveraging reuse of a previously loaded client certificate from file for a connection）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2016-7141: 连接复用不校验客户端证书状态
struct TlsConn {
    std::string client_cert_file;   // 该连接使用的客户端证书
    bool        in_pool;
};

static TlsConn* reuse_or_create(TlsConn* pool, int n, const std::string& wanted_cert) {
    /* DEFECT */ // 原始缺陷: 复用判定不比较 client_cert_file
    for (int i = 0; i < n; ++i)
        if (pool[i].in_pool) return &pool[i];
    TlsConn* c = new TlsConn{ wanted_cert, true };
    return c;
}

int main() {
    TlsConn pool[1] = { { "/home/alice/client.pem", true } };   // alice 证书的连接
    // 攻击者(无证书)发起新连接 → 错误复用 alice 的已认证连接
    TlsConn* c = reuse_or_create(pool, 1, "");
    std::printf("新连接使用的客户端证书: '%s' (正确行为: 无证书应新建连接)\n",
                c->client_cert_file.c_str());
    return 0;
}
'''),

("G051", dict(
  defect_type="stack_overflow_write", func="sqlite3VXPrintf_float", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-3416", url="https://nvd.nist.gov/vuln/detail/CVE-2015-3416",
           project="sqlite", commit="", simplification="剥离 SQLite SQL 引擎，保留『浮点转换的 width/precision 未按缓冲容量截断』核心缺陷"),
  trigger="SQL 中 %.200000f 的巨量宽度 → 输出循环越过 100 字节缓冲",
  notes="CVE-2015-3416: sqlite3VXPrintf 未正确处理浮点转换的 precision/width（CVE 描述: does not properly handle precision and width values during floating-point conversions ... integer overflow and stack-based buffer overflow）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2015-3416: VXPrintf 浮点转换 width 未截断 → 栈缓冲溢出
static void vxprintf_float(char* buf, double v, int width) {
    char digits[64];
    int n = std::snprintf(digits, sizeof(digits), "%.3f", v);
    int i = 0;
    /* DEFECT */ // 原始缺陷: width 未按 buf 容量截断
    for (; i < width; ++i)
        buf[i] = (i < n) ? digits[i] : ' ';
    buf[i] = '\0';
}

int main() {
    // crafted SQL: SELECT printf('%.200f', 3.14159) — width=200 远超输出缓冲 100
    char buf[100];
    vxprintf_float(buf, 3.14159, 200);
    std::printf("printf result=%.20s...\n", buf);
    return 0;
}
'''),

("G052", dict(
  defect_type="heap_overread", func="rtreenode", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2019-8457", url="https://nvd.nist.gov/vuln/detail/CVE-2019-8457",
           project="sqlite", commit="", simplification="剥离 SQLite rtree 模块，保留『单元数与节点缓冲大小不一致时循环读越界』核心缺陷"),
  trigger="rtree 节点缓冲仅含 2 个单元，头部声明的单元数为 9 → 循环读越界",
  notes="CVE-2019-8457: rtreenode() 处理无效 rtree 表时堆越界读（CVE 描述: heap out-of-bound read in the rtreenode() function when handling invalid rtree tables, CWE-125）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-8457: rtreenode 处理 invalid rtree 表 → 堆越界读
struct RtreeNode {
    unsigned char* data;
    int            data_len;   // 实际缓冲大小
    int            n_cell;     // 头部声明的单元数(攻击者可控)
};

static double rtreenode_read_coord(const RtreeNode* n, int cell, int dim) {
    // 每单元 8 字节坐标 × 4 维
    size_t off = sizeof(int) + (size_t)cell * 32 + (size_t)dim * 8;
    double v;
    /* DEFECT */ // 原始缺陷: 未校验 cell 数与 data_len 的一致性
    std::memcpy(&v, n->data + off, sizeof(v));
    return v;
}

int main() {
    // crafted rtree 节点: 缓冲只有 2 个单元(8+64 字节), 头部声明 n_cell=9
    RtreeNode n;
    n.data_len = 8 + 2 * 32;
    n.n_cell = 9;
    n.data = new unsigned char[n.data_len];
    std::memset(n.data, 0x3F, n.data_len);
    std::memcpy(n.data, &n.n_cell, sizeof(int));
    for (int c = 0; c < n.n_cell; ++c)
        std::printf("cell %d coord0=%f\n", c, rtreenode_read_coord(&n, c, 0));   // c>=2 越界
    delete[] n.data;
    return 0;
}
'''),

("G053", dict(
  defect_type="null_deref", func="window_query_agginfo", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2020-11655", url="https://nvd.nist.gov/vuln/detail/CVE-2020-11655",
           project="sqlite", commit="", simplification="剥离 SQLite 窗口函数引擎，保留『畸形窗口函数查询时 AggInfo 初始化被跳过但调用方继续使用』核心缺陷"),
  trigger="畸形窗口函数查询 → AggInfo 初始化失败(列为 NULL)但后续遍历仍解引用",
  notes="CVE-2020-11655: 畸形窗口函数查询因 AggInfo 初始化被错误处理而段错误（CVE 描述: denial of service (segmentation fault) via a malformed window-function query because the AggInfo object's initialization is mishandled）。",
), r'''
#include <cstdio>
// CVE-2020-11655: AggInfo 初始化被错误处理 → NULL 解引用
struct AggInfo {
    int    n_column;
    char** columns;   // 初始化失败时应保持 NULL 且调用方必须停止
};

static int parse_window_query(bool malformed, AggInfo* agg) {
    agg->n_column = 1;
    if (malformed) {
        agg->columns = 0;   // 初始化失败(畸形查询)
        return -1;
    }
    agg->columns = new char*[1];
    agg->columns[0] = new char[8];
    return 0;
}

static void walk_agg_columns(const AggInfo* agg) {
    /* DEFECT */ // 原始缺陷: 初始化失败的 AggInfo 仍被遍历
    for (int i = 0; i < agg->n_column; ++i) {
        std::printf("col %d: %s\n", i, agg->columns[i]);   // columns 为 NULL → SEGV
    }
}

int main() {
    AggInfo agg;
    parse_window_query(true, &agg);   // 畸形窗口函数查询
    walk_agg_columns(&agg);           // 调用方未检查解析结果 → 崩溃
    return 0;
}
'''),

("G054", dict(
  defect_type="use_after_free", func="alter_table_rename", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2020-11656", url="https://nvd.nist.gov/vuln/detail/CVE-2020-11656",
           project="sqlite", commit="", simplification="剥离 SQLite ALTER TABLE 引擎，保留『token 内容释放后错误路径仍引用』核心缺陷"),
  trigger="ALTER TABLE RENAME 失败路径先释放 token.z，错误消息构造仍引用 t->z",
  notes="CVE-2020-11656: ALTER TABLE 实现中的 use-after-free（CVE 描述: the ALTER TABLE implementation has a use-after-free, as demonstrated by an ORDER BY clause that belongs to a compound SELECT statement）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2020-11656: ALTER TABLE token 释放后仍被引用 → UAF
struct Token {
    char* z;   // 词法单元内容
    int   n;
};

static void token_free(Token* t) {
    delete[] t->z;
    /* DEFECT */ // 原始缺陷: 释放后 t->z 未置空, 错误路径仍引用
}

static char* alter_rename_error_message(const Token* t) {
    char* msg = new char[64];
    /* DEFECT */ std::snprintf(msg, 64, "rename failed near: %.*s", t->n, t->z);   // 读已释放内存
    return msg;
}

int main() {
    Token t;
    t.n = 11;
    t.z = new char[12];
    std::memcpy(t.z, "ORDER BY x", 12);
    token_free(&t);                                  // compound SELECT 的 ORDER BY token 被释放
    char* msg = alter_rename_error_message(&t);      // 错误消息仍引用 → UAF
    std::printf("%s\n", msg);
    delete[] msg;
    return 0;
}
'''),
]
