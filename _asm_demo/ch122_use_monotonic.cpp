#include <memory_resource>
void use_monotonic() {
    char buf[1024];
    std::pmr::monotonic_buffer_resource res{buf, sizeof(buf)};
    void* p = res.allocate(64);
    (void)p;
}
