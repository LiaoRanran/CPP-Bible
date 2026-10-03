# -*- coding: utf-8 -*-
# 676c-G spec part17: GitHub issue 组 I (nlohmann/json, G093-G095; tinyxml2, G096-G097)
PART = [
("G093", dict(
  defect_type="heap_underflow", func="json_array_at", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="nlohmann/json#5647", url="https://github.com/nlohmann/json/issues/5647",
           project="nlohmann/json", commit="", simplification="剥离 JSON 库类型层，用 vector<int> 数组镜像 issue 中引用的 operator[] 代码路径（resize(idx+1) 回绕 + operator[](SIZE_MAX) 前向越界写）"),
  trigger="operator[](SIZE_MAX)：idx+1 回绕为 0 → resize(0) 清空数组 → v[SIZE_MAX] 写到缓冲区之前 1 元素",
  notes="nlohmann/json#5647（已修复）: operator[](size_type) 传入 SIZE_MAX 时 resize(idx+1) 回绕为 0 清空数组，随后 operator[](SIZE_MAX) 定位到缓冲区之前 1 元素并写入（issue 附带代码路径 include/nlohmann/json.hpp#L2838）。",
), r'''
#include <cstdio>
#include <cstring>
#include <vector>
// nlohmann/json#5647: operator[](SIZE_MAX) → resize 回绕 + 前向越界写
class JsonArray {
    std::vector<int> m_data;   // 镜像 json array 底层存储
public:
    void push_back(int v) { m_data.push_back(v); }
    size_t size() const { return m_data.size(); }

    int& operator[](size_t idx) {
        // 镜像 json.hpp#L2838:
        if (idx >= m_data.size()) {
            /* DEFECT */ m_data.resize(idx + 1);   // idx==SIZE_MAX → idx+1 回绕为 0 → 清空
        }
        /* DEFECT */ return m_data[idx];           // operator[](SIZE_MAX) → begin()+SIZE_MAX = begin()-1
    }
};

int main() {
    JsonArray arr;
    arr.push_back(1);
    arr.push_back(2);
    // issue 中的意外触发方式: j[v.size() - 1] 当 v 为空 → SIZE_MAX
    size_t idx = 0xFFFFFFFFFFFFFFFFull;   // SIZE_MAX
    int& ref = arr[idx];
    ref = 42;                             // 写入缓冲区之前 1 个 int → 堆下溢写
    std::printf("arr.size=%zu\n", arr.size());
    return 0;
}
'''),

("G094", dict(
  defect_type="heap_overread", func="bjdata_parse_string", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="nlohmann/json#3492", url="https://github.com/nlohmann/json/issues/3492",
           project="nlohmann/json", commit="", simplification="issue 报告 OSS-Fuzz 47391 的 parse_bjdata 堆越界读（READ 1）但未公开具体代码行；按报告的崩溃类别以『解析器按头部声明长度读而未校验剩余输入』等价重构，故标 planted=true"),
  trigger="BJData string 头部声明长度 32，输入缓冲仅 8 字节 → 解析循环读越界",
  notes="nlohmann/json#3492（已修复）: OSS-Fuzz 报告 parse_bjdata Heap-buffer-overflow READ 1。等价重构：BJData 解析器按声明长度消费输入而不校验剩余空间。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// nlohmann/json#3492 (等价重构): BJData 解析按声明长度读 → 堆越界读
// BJData string 编码: 'S' 'i' <int8 len> <bytes...>
static int bjdata_parse(const unsigned char* in, size_t in_size) {
    size_t pos = 0;
    if (pos >= in_size || in[pos] != 'S') return -1;
    ++pos;
    if (pos >= in_size || in[pos] != 'i') return -1;
    ++pos;
    if (pos >= in_size) return -1;
    unsigned char declared = in[pos++];       // 头部声明的字符串长度
    char out[64];
    /* DEFECT */ for (unsigned char i = 0; i < declared; ++i) {   // 未校验 declared <= in_size - pos
        out[i] = (char)in[pos + i];           // declared=32, 剩余 5 字节 → 越界读
    }
    out[declared < 64 ? declared : 63] = '\0';
    std::printf("bjdata string=%s\n", out);
    return 0;
}

int main() {
    // crafted BJData(对应 OSS-Fuzz 最小化用例的结构): 'S','i',32,5 字节数据
    unsigned char in[8] = { 'S', 'i', 32, 'a', 'b', 'c', 'd', 'e' };
    bjdata_parse(in, 8);
    return 0;
}
'''),

("G095", dict(
  defect_type="heap_overread", func="json_parse_string", severity="medium", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="nlohmann/json#575", url="https://github.com/nlohmann/json/issues/575",
           project="nlohmann/json", commit="", simplification="issue 为 OSS-Fuzz 1400 自动报告（Heap-buffer-overflow READ 2, 位于 parse 期间的 string 构造），未附最小代码；按崩溃类别以『字符串解析越过输入缓冲末尾』等价重构，故标 planted=true"),
  trigger="字符串解析扫描闭合引号时越过 4 字节堆输入缓冲（READ 2）",
  notes="nlohmann/json#575（已修复）: OSS-Fuzz 1400 Heap-buffer-overflow READ 2（parse 期间 std::string 构造）。等价重构：字符串扫描缺少 end 边界检查。",
), r'''
#include <cstdio>
#include <cstring>
// nlohmann/json#575 (等价重构): 字符串解析越过输入末尾 → 堆越界读
static void json_parse_string(const char* cur, const char* end) {
    if (*cur != '\"') return;
    ++cur;
    /* DEFECT */ while (*cur && *cur != '\"') ++cur;   // 原始缺陷: 未检查 cur < end
    ++cur;                                             // READ 2: 再读闭合引号之后 1 字节
    std::printf("string parsed len=%ld\n", (long)(cur - end));
}

int main() {
    // crafted JSON 输入(OSS-Fuzz 用例结构): 4 字节堆缓冲, 引号未闭合
    char* in = new char[4]{ '\"', 'a', 'b', 'c' };
    json_parse_string(in, in + 4);
    delete[] in;
    return 0;
}
'''),

("G096", dict(
  defect_type="heap_overflow", func="DynArray_EnsureCapacity", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="leethomason/tinyxml2#1065", url="https://github.com/leethomason/tinyxml2/issues/1065",
           project="tinyxml2", commit="", simplification="按 issue 中引用的原始代码（DynArray<T,INITIAL_SIZE>::EnsureCapacity: cap*2 无运行时保护 + memcpy）直接镜像，只剥离 XML 解析层"),
  trigger="EnsureCapacity(cap=2^63/T)：cap*2 溢出 → 分配极小 → memcpy 大尺寸 → 堆越界写",
  notes="tinyxml2#1065（未修复）: EnsureCapacity 的 newAllocated = cap*2 仅由 release 版被移除的 TIXMLASSERT 保护，溢出后小分配 + 大 memcpy → 堆越界写。issue 附原始代码位置 tinyxml2.h:450-470。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// tinyxml2#1065: DynArray::EnsureCapacity 整数溢出 → 小分配大拷贝
template <typename T, int INITIAL_SIZE = 16>
class DynArray {
    T*     _mem;
    int    _size;
    int    _allocated;

public:
    DynArray() : _mem(new T[INITIAL_SIZE]), _size(0), _allocated(INITIAL_SIZE) {}
    ~DynArray() { delete[] _mem; }

    /* DEFECT */ // 镜像 issue 引用的 EnsureCapacity: cap*2 无运行时保护(release 无 TIXMLASSERT)
    void EnsureCapacity(size_t cap) {
        if (cap <= (size_t)_allocated) return;
        const size_t newAllocated = cap * 2;                 // 溢出 → 极小值
        T* newMem = new T[newAllocated > 0 ? newAllocated : 1];
        std::memcpy(newMem, _mem, sizeof(T) * (size_t)_size);   // 大 memcpy → 堆越界写
        delete[] _mem;
        _mem = newMem;
        _allocated = (int)newAllocated;
    }

    void Push(const T& v) {
        EnsureCapacity((size_t)_size + 1);   // 常规增长
        _mem[_size++] = v;
    }
};

int main() {
    DynArray<int> arr;
    for (int i = 0; i < 16; ++i) arr.Push(i);      // 填满 16 个元素(_size=16)
    // crafted XML 触发的巨大 cap: 2^63 → cap*2 回绕为 0 → 分配 1 元素
    arr.EnsureCapacity(0x8000000000000000ull);
    std::printf("capacity grown\n");
    return 0;
}
'''),

("G097", dict(
  defect_type="global_overflow", func="XMLDocument_ErrorIDToName", severity="medium", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="leethomason/tinyxml2#923", url="https://github.com/leethomason/tinyxml2/issues/923",
           project="tinyxml2", commit="", simplification="按 issue 引用的原始代码路径直接镜像（_errorNames 数组 19 项, errorID 可达 XML_ERROR_COUNT=19 → _errorNames[errorID] 越界读）"),
  trigger="errorID == XML_ERROR_COUNT(19)：_errorNames[19] 越过 19 元素全局数组",
  notes="tinyxml2#923（未修复）: ErrorIDToName 对 errorID==XML_ERROR_COUNT 读 _errorNames[19] → AddressSanitizer global-buffer-overflow（issue 附 tinyxml2.cpp:2501-2507 与数组定义 tinyxml2.cpp:2136-2156）。",
), r'''
#include <cstdio>
// tinyxml2#923: ErrorIDToName 对 XML_ERROR_COUNT 越界读全局数组
enum XMLError {
    XML_SUCCESS = 0,
    XML_NO_ATTRIBUTE, XML_WRONG_ATTRIBUTE_TYPE, XML_ERROR_FILE_NOT_FOUND,
    XML_ERROR_FILE_COULD_NOT_BE_OPENED, XML_ERROR_FILE_READ_ERROR,
    XML_ERROR_PARSING_ELEMENT, XML_ERROR_PARSING_ATTRIBUTE,
    XML_ERROR_PARSING_TEXT, XML_ERROR_PARSING_CDATA, XML_ERROR_PARSING_COMMENT,
    XML_ERROR_PARSING_DECLARATION, XML_ERROR_PARSING_UNKNOWN,
    XML_ERROR_EMPTY_DOCUMENT, XML_ERROR_PARSING, XML_ERROR_PARSING_X,
    XML_ERROR_ELEMENT_MISMATCH, XML_ERROR_PARSING_ROOT_ELEMENT,
    XML_ERROR_PARSING_DOCUMENT, XML_ERROR_COUNT
    // _errorNames 数组只有 19 项(下标 0..18), XML_ERROR_COUNT = 19 → 越界下标
};

static const char* _errorNames[19] = {
    "XML_SUCCESS", "XML_NO_ATTRIBUTE", "XML_WRONG_ATTRIBUTE_TYPE",
    "XML_ERROR_FILE_NOT_FOUND", "XML_ERROR_FILE_COULD_NOT_BE_OPENED",
    "XML_ERROR_FILE_READ_ERROR", "XML_ERROR_PARSING_ELEMENT",
    "XML_ERROR_PARSING_ATTRIBUTE", "XML_ERROR_PARSING_TEXT",
    "XML_ERROR_PARSING_CDATA", "XML_ERROR_PARSING_COMMENT",
    "XML_ERROR_PARSING_DECLARATION", "XML_ERROR_PARSING_UNKNOWN",
    "XML_ERROR_EMPTY_DOCUMENT", "XML_ERROR_PARSING", "XML_ERROR_PARSING_X",
    "XML_ERROR_ELEMENT_MISMATCH", "XML_ERROR_PARSING_ROOT_ELEMENT",
    "XML_ERROR_PARSING_DOCUMENT"
};

static const char* ErrorIDToName(XMLError errorID) {
    /* DEFECT */ return _errorNames[errorID];   // errorID 可达 XML_ERROR_COUNT(19)? 数组下标 19 越界
}

int main() {
    // crafted 路径: 内部把 errorID 置为 XML_ERROR_COUNT(与 issue 一致)
    XMLError err = XML_ERROR_COUNT;
    std::printf("error name=%s\n", ErrorIDToName(err));   // 读 _errorNames[19] → 全局越界
    return 0;
}
'''),
]
