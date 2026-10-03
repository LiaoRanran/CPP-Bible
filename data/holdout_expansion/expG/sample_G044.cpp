// sample_G044
// defect_type: state_machine
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2022-32221 (https://nvd.nist.gov/vuln/detail/CVE-2022-32221) [curl]
// (authoritative annotation in sample_G044.json)
#include <cstdio>
#include <string>
// CVE-2022-32221: PUT 后复用 handle 发 POST → 错误使用读回调
enum HttpMethod { HTTP_NONE, HTTP_PUT, HTTP_POST };

struct EasyHandle {
    HttpMethod last_method;
    std::string postfields;       // POST 正文(直接发送)
    bool        read_callback_set;
};

static std::string http_perform(EasyHandle* h, HttpMethod method) {
    h->last_method = method;
    if (method == HTTP_POST && !h->postfields.empty()) {
        // 应直接发送 POSTFIELDS
        if (h->read_callback_set && h->last_method == HTTP_PUT) {
            /* DEFECT */ // 原始缺陷: 之前 PUT 设置的读回调状态残留, 错误走读回调路径
            return "READ-CALLBACK-DATA[stale]";
        }
        return h->postfields;
    }
    return "PUT-BODY";
}

int main() {
    EasyHandle h{ HTTP_NONE, "POST-REQUEST-BODY", true };
    http_perform(&h, HTTP_PUT);                     // 第一个请求: PUT 用读回调
    std::string sent = http_perform(&h, HTTP_POST); // 第二个请求: POST 用 POSTFIELDS
    std::printf("POST 实际发送: %s\n", sent.c_str());
    std::printf("(正确行为: 发送 POST-REQUEST-BODY, 不应调用已废弃的读回调)\n");
    return 0;
}
