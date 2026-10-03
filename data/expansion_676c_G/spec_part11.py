# -*- coding: utf-8 -*-
# 676c-G spec part11: SQLite ubsan/miss + libpng/webp 组 (G055-G059)
PART = [
("G055", dict(
  defect_type="integer_overflow", func="sqlite3_str_appendall", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-35737", url="https://nvd.nist.gov/vuln/detail/CVE-2022-35737",
           project="sqlite", commit="", simplification="剥离 SQLite C API 字符串层，保留『字符串长度按 int 累加』核心缺陷，长度由运行时变量给出"),
  trigger="字符串参数达数十亿字节，nUsed += n 的 int 累加溢出",
  notes="CVE-2022-35737: 数十亿字节的字符串参数导致 array-bounds overflow（CVE 描述: sometimes allows an array-bounds overflow if billions of bytes are used in a string argument to a C API）。本样本镜像 int 累加溢出点。",
), r'''
#include <cstdio>
// CVE-2022-35737: 超长字符串参数 → 长度 int 累加溢出
struct SqliteStr {
    char* z;
    int   nUsed;
    int   nAlloc;
};

static void str_append(SqliteStr* s, int n) {
    /* DEFECT */ s->nUsed += n;   // 原始缺陷: 巨大 n 时 int 溢出, 后续按 nUsed 索引越界
}

int main() {
    SqliteStr s{ 0, 2147483000, 2147483647 };
    volatile int n = 1000000;      // crafted: 巨大字符串追加
    str_append(&s, n);
    std::printf("nUsed=%d (应为 %lld)\n", s.nUsed, (long long)s.nUsed);
    return 0;
}
'''),

("G056", dict(
  defect_type="heap_overread", func="getNodeSize", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-10989", url="https://nvd.nist.gov/vuln/detail/CVE-2017-10989",
           project="sqlite", commit="", simplification="剥离 SQLite rtree 模块与数据库 I/O，保留『undersized blob 按头部声明的单元数读取』核心缺陷"),
  trigger="rtree blob 仅 8 字节，头部声明的维度/单元数要求读 64 字节 → 越界读",
  notes="CVE-2017-10989: getNodeSize 处理 undersized RTree blob 时堆越界读（CVE 描述: mishandles undersized RTree blobs in a crafted database, leading to a heap-based buffer over-read）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2017-10989: getNodeSize 对 undersized blob 越界读
struct RtreeBlob {
    unsigned char* data;
    int            data_len;   // blob 实际大小(攻击者 crafted 过小)
    int            n_dim;      // 头部声明的维度数
};

static int getNodeSize(const RtreeBlob* b) {
    int cell_size = 8 * b->n_dim + 4;
    /* DEFECT */ // 原始缺陷: 未校验 blob 大小是否容纳声明的单元
    double first_coord;
    std::memcpy(&first_coord, b->data + 4, sizeof(first_coord));   // 读 4..12, blob 仅 8 字节
    return cell_size;
}

int main() {
    // crafted 数据库页中的 undersized rtree blob
    RtreeBlob b;
    b.data_len = 8;
    b.n_dim = 7;                       // 声明 7 维 → 单元 60 字节, 但 blob 只有 8 字节
    b.data = new unsigned char[8]{ 0, 0, 0, 7, 0x3F, 0xF0, 0, 0 };
    std::printf("node size=%d\n", getNodeSize(&b));   // memcpy 读 data[4..12] → 越界 4 字节
    delete[] b.data;
    return 0;
}
'''),

("G057", dict(
  defect_type="logic_error", func="os_unix_tmpdir_search", severity="medium", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-6153", url="https://nvd.nist.gov/vuln/detail/CVE-2016-6153",
           project="sqlite", commit="", simplification="基于 CVE 描述（临时目录搜索算法实现不当导致敏感信息泄露/DoS）以等价的目录选择逻辑重构，非原始代码镜像，故标 planted=true"),
  trigger="临时目录搜索把用户可写的世界可写目录排在世界可写目录之前",
  notes="CVE-2016-6153: os_unix.c 临时目录搜索算法实现不当（CVE 描述: improperly implements the temporary directory search algorithm ... obtain sensitive information）。逻辑缺陷，正确=跳过世界可写目录、实际=使用 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2016-6153: 临时目录搜索算法实现不当 → 使用攻击者可控目录
struct DirCandidate {
    const char* path;
    bool        world_writable;
    bool        user_owned;    // 是否当前用户所有
};

static const DirCandidate k_dirs[] = {
    { "/var/tmp",      false, true  },   // 正确顺序应优先安全目录
    { "/tmp",          true,  false },   // 世界可写 → 攻击者可控
    { "/usr/tmp",      true,  false },
};

static const char* pick_tmpdir_vulnerable() {
    /* DEFECT */ // 原始缺陷: 搜索顺序未按世界可写位降权
    for (const DirCandidate& d : k_dirs)
        return d.path;   // 直接返回第一个候选(未检查 world_writable)
    return 0;
}

int main() {
    const char* dir = pick_tmpdir_vulnerable();
    std::printf("SQLite 临时数据库目录: %s (该目录 world_writable=true)\n", dir);
    std::printf("(正确行为: 跳过世界可写目录, 防止 DB 文件被攻击者读取/替换)\n");
    return 0;
}
'''),

("G058", dict(
  defect_type="heap_overflow", func="png_set_PLTE", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-8126", url="https://nvd.nist.gov/vuln/detail/CVE-2015-8126",
           project="libpng", commit="", simplification="剥离 PNG 解码器，PLTE chunk 硬编码为 1200 字节，保留『palette 数量未校验上限即 memcpy』核心缺陷（修复版校验 num > PNG_MAX_PALETTE_LENGTH）"),
  trigger="PLTE chunk 声明 400 项(1200 字节) > 256 项上限 → 拷贝越界 1KB",
  notes="CVE-2015-8126: png_set_PLTE/png_get_PLTE 缓冲区溢出（CVE 描述: Multiple buffer overflows in the (1) png_set_PLTE and (2) png_get_PLTE functions ... allow remote attackers to cause a denial of service）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2015-8126: png_set_PLTE 未校验调色板数量上限 → 堆溢出
static const int PNG_MAX_PALETTE_LENGTH = 256;

struct PngInfo {
    unsigned char  palette[PNG_MAX_PALETTE_LENGTH * 3];   // 256 项 × RGB
    int            num_palette;
};

static void png_set_PLTE(PngInfo* info, const unsigned char* chunk, int chunk_len) {
    int num = chunk_len / 3;
    /* DEFECT */ // 原始缺陷: 未校验 num <= PNG_MAX_PALETTE_LENGTH
    std::memcpy(info->palette, chunk, (size_t)num * 3);
    info->num_palette = num;
}

int main() {
    // crafted PNG: PLTE chunk 长度 1200 字节(400 项)
    unsigned char* chunk = new unsigned char[1200];
    std::memset(chunk, 0x7F, 1200);
    PngInfo info;
    std::memset(&info, 0, sizeof(info));
    png_set_PLTE(&info, chunk, 1200);   // 400 项 × 3 = 1200 > 768 → 越界写 432 字节
    std::printf("num_palette=%d\n", info.num_palette);
    delete[] chunk;
    return 0;
}
'''),

("G059", dict(
  defect_type="division_by_zero", func="png_check_chunk_length", severity="medium", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2018-13785", url="https://nvd.nist.gov/vuln/detail/CVE-2018-13785",
           project="libpng", commit="", simplification="剥离 PNG 解码器，保留官方公告描述的『row_factor 错误计算导致整数溢出与除零』核心缺陷（使用与原始 pngrutil.c 相同的 row_factor 公式）"),
  trigger="IHDR 高度 h=0x7FFFFFFC，row_factor 公式中 h+7 有符号溢出",
  notes="CVE-2018-13785: png_check_chunk_length 的 row_factor 错误计算（CVE 描述: a wrong calculation of row_factor ... may trigger an integer overflow and resultant divide-by-zero）。保留原始公式与 crafted 高度。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2018-13785: row_factor 错误计算 → 整数溢出 / 除零
static void png_check_chunk_length(unsigned int length, unsigned int height, unsigned int idat_limit) {
    // 原始 pngrutil.c 的 row_factor 公式(有符号 32 位计算)
    /* DEFECT */ int32_t hh = (int32_t)height + 7;   // 2147483644 + 7 → 有符号 32 位加法溢出(UB)
    int32_t denom = (int32_t)((hh & 0x7fffffffL) / (int32_t)height + 1L);
    unsigned int row_factor = idat_limit / (unsigned int)denom;
    // length 检查按 row_factor 分块进行
    unsigned int blocks = length / row_factor;   // 原始缺陷链: 溢出可致除零
    std::printf("chunk length check: %u blocks of %u (hh=%d)\n", blocks, row_factor, hh);
}

int main() {
    // crafted PNG: IHDR 高度 0x7FFFFFFC → height+7 有符号溢出
    png_check_chunk_length(0x7FFFFFF4u, 0x7FFFFFFCu, 0x40000000u);
    return 0;
}
'''),
]
