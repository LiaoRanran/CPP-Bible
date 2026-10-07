// sample_G069
// [redacted]
// severity: high
// [redacted]
// expected_verdict: catch
// [redacted]
// [redacted]
// (authoritative annotation in sample_G069.json)
#include <cstdio>
#include <cstring>
// [redacted]
static const size_t HOST_BUF_SIZE = 1024;

static bool digits_dots(const char* name, char* buffer, size_t buffer_size) {
    /* [redacted]*/ size_t size_needed = std::strlen(name);   // [redacted]
    if (size_needed > buffer_size) return false;
    std::memcpy(buffer, name, size_needed);
    buffer[size_needed] = '\0';   // [redacted]
    return true;
}

int main() {
    char* hostbuf = new char[HOST_BUF_SIZE];
    // crafted 主机名: 恰好 1024 个 'a'
    char* name = new char[HOST_BUF_SIZE + 1];
    std::memset(name, 'a', HOST_BUF_SIZE);
    name[HOST_BUF_SIZE] = '\0';
    if (digits_dots(name, hostbuf, HOST_BUF_SIZE))
        std::printf("hostname accepted: %.8s...\n", hostbuf);
    delete[] name;
    delete[] hostbuf;
    return 0;
}
