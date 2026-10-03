# -*- coding: utf-8 -*-
# 676c-G spec part12: libwebp/zlib/libxml2/nginx 组 (G060-G065)
PART = [
("G060", dict(
  defect_type="heap_overflow", func="BuildHuffmanTable", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2023-4863", url="https://nvd.nist.gov/vuln/detail/CVE-2023-4863",
           project="libwebp", commit="", simplification="剥离 WebP VP8L 解码器，保留 Huffman 表构建『码长分布合法性未校验 → 表项写入越过分配大小』核心缺陷（与原始 BuildHuffmanTable 填表逻辑同构）"),
  trigger="crafted 码长分布: 5 个长度为 2 的码 → 需写 20 项 > 分配的 16 项表",
  notes="CVE-2023-4863: libwebp BuildHuffmanTable 堆溢出（CVE 描述: Heap buffer overflow in libwebp ... allowed a remote attacker to perform an out of bounds memory write, Chromium Critical）。修复版增加码长分布合法性校验。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2023-4863: BuildHuffmanTable 未校验码长分布 → 表项越界写
static const int ROOT_BITS = 4;                 // 根表 16 项
static const int MAX_CODE_BITS = 4;

static int BuildHuffmanTable(const int* code_lengths, int n_symbols, unsigned int* table, int table_cap) {
    // 统计各码长数量
    int count[MAX_CODE_BITS + 1] = { 0 };
    for (int s = 0; s < n_symbols; ++s)
        if (code_lengths[s]) ++count[code_lengths[s]];
    // 原始缺陷: 缺少合法性校验 sum(count[i] << (MAX-i)) <= (1 << ROOT_BITS)
    // (修复版: if (total > (1 << ROOT_BITS)) return 0;)
    int key = 0;
    int written = 0;
    for (int len = 1; len <= MAX_CODE_BITS; ++len) {
        for (int s = 0; s < n_symbols; ++s) {
            if (code_lengths[s] != len) continue;
            int step = 1 << (MAX_CODE_BITS - len);       // 该码占用的表项数
            /* DEFECT */ for (int i = 0; i < step; ++i) {
                table[key + i] = (unsigned int)s;        // 无任何边界检查: 越过 table_cap 继续写
                ++written;
            }
            key += step;
        }
    }
    return written;
}

int main() {
    unsigned int* table = new unsigned int[1 << ROOT_BITS];   // 分配 16 项
    std::memset(table, 0xEE, (1 << ROOT_BITS) * sizeof(unsigned int));
    // crafted 码长: 5 个长度为 2 的码 → 每个 4 项 → 需要 20 项 > 16
    int code_lengths[5] = { 2, 2, 2, 2, 2 };
    int n = BuildHuffmanTable(code_lengths, 5, table, 1 << ROOT_BITS);
    std::printf("huffman entries written=%d (表容量 16)\n", n);
    delete[] table;
    return 0;
}
'''),

("G061", dict(
  defect_type="pointer_overflow", func="inflate_table_build", severity="medium", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-9840", url="https://nvd.nist.gov/vuln/detail/CVE-2016-9840",
           project="zlib", commit="", simplification="基于 CVE 描述（inftrees.c 不当指针算术）以等价的码表填充循环重构（指针推进越过表尾），非原始代码镜像，故标 planted=true"),
  trigger="crafted 码长分布使码表填充指针越过分配的表尾",
  notes="CVE-2016-9840: inftrees.c 不当指针算术（CVE 描述: inftrees.c in zlib 1.2.8 might allow ... improper pointer arithmetic）。用户态等价重构（planted=true）。UBSan pointer-overflow 捕获。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2016-9840: inftrees.c 码表填充指针算术不当 → 指针越界回绕
struct Code {
    unsigned short op;    // 操作/长度位
    unsigned short val;   // 值
};

static unsigned inflate_table_build(const unsigned char* lengths, int n, Code* table, int table_cap) {
    Code* here = table;
    Code* end = table + table_cap;
    for (int i = 0; i < n; ++i) {
        if (!lengths[i]) continue;
        /* DEFECT */ // 原始缺陷: 码长非法分布时 here 推进越过表尾而不停止
        here += (1 << (15 - lengths[i]));
        if (here > end) {
            // crafted 分布: 持续推进直到指针算术回绕(未定义行为)
            here += (1 << 15);
        }
        *here = Code{ (unsigned short)lengths[i], (unsigned short)i };
    }
    return (unsigned)(here - table);
}

int main() {
    Code table[16];
    // crafted 码长: 全部为 15 位码 → 每码推进 1, 随后非法再推进 2^15 → 回绕
    unsigned char lengths[32];
    for (int i = 0; i < 32; ++i) lengths[i] = 15;
    std::printf("table used=%u\n", inflate_table_build(lengths, 32, table, 16));
    return 0;
}
'''),

("G062", dict(
  defect_type="pointer_overflow", func="inflate_fast_out", severity="medium", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-9841", url="https://nvd.nist.gov/vuln/detail/CVE-2016-9841",
           project="zlib", commit="", simplification="基于 CVE 描述（inffast.c 不当指针算术）以等价的输出指针推进循环重构（距离/长度 unchecked 使 out 指针越过窗口末尾），非原始代码镜像，故标 planted=true"),
  trigger="crafted 解压流的 copy 距离把输出指针推进越过窗口末尾直至回绕",
  notes="CVE-2016-9841: inffast.c 不当指针算术（CVE 描述: inffast.c in zlib 1.2.8 might allow ... improper pointer arithmetic）。用户态等价重构（planted=true）。UBSan pointer-overflow 捕获。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2016-9841: inffast.c 输出指针 unchecked 推进 → 指针回绕
static unsigned inflate_fast_out(const unsigned char* in, int in_len, unsigned char* out, int out_cap) {
    unsigned char* o = out;
    unsigned char* out_end = out + out_cap;
    int i = 0;
    while (i + 1 < in_len) {
        unsigned dist = in[i + 1];            // crafted: 距离字段
        /* DEFECT */ o += dist;               // 原始缺陷: 推进量未按 out_end 校验
        if (o >= out_end)
            *o = 'X';                         // 越过窗口末尾仍写入 → 堆越界写
        i += 2;
    }
    return (unsigned)(o - out);
}

int main() {
    unsigned char* out = new unsigned char[64];
    // crafted 解压流: 距离字段 0x46(70) → 首次写入落在 out+70, 越过 64 字节缓冲 6 字节
    unsigned char in[4] = { 0x00, 0x46, 0x00, 0x30 };
    std::printf("produced=%u\n", inflate_fast_out(in, 4, out, 64));
    delete[] out;
    return 0;
}
'''),

("G063", dict(
  defect_type="use_after_free", func="xptr_range_eval", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-4658", url="https://nvd.nist.gov/vuln/detail/CVE-2016-4658",
           project="libxml2", commit="", simplification="剥离 libxml2 XPointer 解析器，保留『namespace 节点进入 range 后被释放又复用』核心缺陷"),
  trigger="XPointer range 含 namespace 节点，节点被释放后仍保留在结果集并被访问",
  notes="CVE-2016-4658: libxml2 xpointer.c 不禁止 namespace 节点进入 XPointer range（CVE 描述: does not forbid namespace nodes in XPointer ranges ... execute arbitrary code or cause a denial of service）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2016-4658: XPointer range 含 namespace 节点 → 节点释放后复用
struct XmlNode {
    char* name;
    bool  is_namespace;
};

static void xml_free_node(XmlNode* n) {
    delete[] n->name;
    delete n;
}

static XmlNode* g_result_set[8];
static int g_result_n = 0;

static void xptr_add_to_range(XmlNode* node) {
    /* DEFECT */ // 原始缺陷: 未禁止 namespace 节点进入 range
    g_result_set[g_result_n++] = node;
}

int main() {
    XmlNode* ns = new XmlNode{ new char[8], true };
    std::memcpy(ns->name, "xmlns:a", 8);
    xptr_add_to_range(ns);        // namespace 节点进入 range 结果集
    // 解析器清理阶段释放 namespace 节点(但结果集仍持有指针)
    xml_free_node(ns);
    // range 遍历阶段复用已释放节点
    for (int i = 0; i < g_result_n; ++i)
        std::printf("range node: %s\n", g_result_set[i]->name);   // UAF 读
    return 0;
}
'''),

("G064", dict(
  defect_type="stack_overflow_write", func="xmlSnprintfElementContent", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-9047", url="https://nvd.nist.gov/vuln/detail/CVE-2017-9047",
           project="libxml2", commit="", simplification="剥离 libxml2 校验器，保留『len=strlen(buf) 后第二次追加分支未按剩余空间收缩 size』核心缺陷（与 issue 中引用的 valid.c 逻辑同构）"),
  trigger="元素内容名 60 字节 + 子内容再追加 → 第二次写入越过 64 字节缓冲",
  notes="CVE-2017-9047: xmlSnprintfElementContent 缓冲溢出（CVE 描述: The function xmlSnprintfElementContent ... is supposed to recursively dump the element content definition into a char buffer 'buf' of size 'size'; len assigned strlen(buf) ... overflow）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2017-9047: xmlSnprintfElementContent 第二次追加未收缩可用空间
struct ElementContent {
    const char*     name;
    ElementContent* child;
};

static void xmlSnprintfElementContent(char* buf, size_t size, const ElementContent* content, int depth) {
    if (!content) return;
    size_t len = std::strlen(buf);
    if (depth > 0) {
        std::snprintf(buf + len, size, ", ");
        len = std::strlen(buf);
    }
    std::snprintf(buf + len, size - len, "%s", content->name);
    if (content->child) {
        len = std::strlen(buf);
        /* DEFECT */ // 原始缺陷: 递归子内容时 size 未按 len 收缩, 直接用原 size
        std::snprintf(buf + len, size, " includes %s", content->child->name);
    }
}

int main() {
    char buf[64];                       // 原始代码的 buf/size
    buf[0] = '\0';
    ElementContent child{ "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 0 };   // 60 字节
    ElementContent parent{ "elem", &child };
    xmlSnprintfElementContent(buf, sizeof(buf), &parent, 0);
    std::printf("content=%s\n", buf);
    return 0;
}
'''),

("G065", dict(
  defect_type="heap_overflow", func="ngx_resolver_copy_name", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-23017", url="https://nvd.nist.gov/vuln/detail/CVE-2021-23017",
           project="nginx", commit="", simplification="剥离 nginx DNS 解析器与网络层，保留『名字解压时 '.' 偏移差一 → 1 字节越界写』核心缺陷（与官方描述 CWE-193 off-by-one 一致）"),
  trigger="crafted DNS 名总长恰等于目的缓冲大小 → 终止符写到 dst[cap]",
  notes="CVE-2021-23017: nginx resolver 差一错误（CVE 描述: an attacker who is able to forge UDP packets from the DNS server to cause 1-byte memory overwrite, CWE-193）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2021-23017: DNS 名解压 '.'/终止符偏移差一 → 1 字节越界写
static int ngx_resolver_copy_name(const unsigned char* src, size_t src_len,
                                  char* dst, size_t dst_cap) {
    size_t n = 0;
    size_t i = 0;
    while (i < src_len) {
        unsigned char label_len = src[i++];
        if (label_len == 0) break;
        if (i + label_len > src_len) return -1;
        if (n + label_len > dst_cap) return -1;       // 仅检查标签本体(边界条件差一)
        std::memcpy(dst + n, src + i, label_len);
        n += label_len;
        i += label_len;
        if (i < src_len && src[i]) dst[n++] = '.';    // 后续还有标签 → 追加分隔符
    }
    /* DEFECT */ // 原始缺陷: 未检查 n 是否已达 dst_cap
    dst[n] = '\0';                                    // n == dst_cap 时写 dst[dst_cap] → 越界 1 字节
    return (int)n;
}

int main() {
    // forged DNS 响应: 名字 "www.example-x.com" 恰 17 字符 → dst 恰好 17 字节
    unsigned char src[32] = { 3, 'w', 'w', 'w', 9, 'e', 'x', 'a', 'm', 'p', 'l', 'e', '-', 'x',
                              3, 'c', 'o', 'm', 0 };
    char* dst = new char[17];
    ngx_resolver_copy_name(src, 19, dst, 17);
    std::printf("resolved=%s\n", dst);
    delete[] dst;
    return 0;
}
'''),
]
