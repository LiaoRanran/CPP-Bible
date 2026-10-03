// sample_G090
// defect_type: heap_underflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: nlohmann/json#5647 (https://github.com/nlohmann/json/issues/5647) [nlohmann/json]
// (authoritative annotation in sample_G090.json)
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
