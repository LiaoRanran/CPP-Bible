// RW-018 | CVE-2022-32221 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-32221
// project_url: https://curl.se/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: 307/308 重定向后，当请求体已被消费（如 PUT）时方法被错误改写成 POST，
//   可能把敏感数据以错误方法发送（请求语义混淆）。
// notes: 最小重构。逻辑缺陷类。
#include <cstdio>
#include <cstring>
#include <string>

struct RequestState {
    std::string method;      // current method, e.g. "PUT"
    bool body_sent;          // whether the body was already consumed
    bool follow_307;         // redirect tells "keep method and body"
};

// BUG: after following a 307 with an already-consumed body, the code resets the
// method to POST (data leak / semantic confusion) instead of aborting.
void handle_redirect(RequestState& st) {
    if (st.follow_307) {
        if (st.body_sent) {
            st.method = "POST";   // WRONG: should keep PUT (or rewind/abort)
        }
        // method otherwise preserved
    } else {
        st.method = "GET";
    }
}

int main() {
    RequestState st{"PUT", true, true};
    handle_redirect(st);
    std::printf("method after 307 redirect = %s (expected PUT)\n", st.method.c_str());
    return 0;
}
