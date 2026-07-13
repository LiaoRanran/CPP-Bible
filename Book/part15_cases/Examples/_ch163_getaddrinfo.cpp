// _ch163_getaddrinfo.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_getaddrinfo.cpp -lws2_32 -o _ch163_getaddrinfo.exe
// 作用: 用 getaddrinfo 解析 "localhost"——跨平台可移植的地址解析入口（③）。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>

int main() {
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);

    addrinfo hints{};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    addrinfo* res = nullptr;
    int rc = getaddrinfo("localhost", "54321", &hints, &res);
    if (rc != 0) {
        std::cerr << "[ga] getaddrinfo 失败: " << gai_strerrorA(rc) << "\n";
        return 1;
    }
    int count = 0;
    for (addrinfo* p = res; p; p = p->ai_next) {
        char ip[INET6_ADDRSTRLEN] = {0};
        if (p->ai_family == AF_INET) {
            sockaddr_in* s = (sockaddr_in*)p->ai_addr;
            inet_ntop(AF_INET, &s->sin_addr, ip, sizeof(ip));
        } else {
            sockaddr_in6* s = (sockaddr_in6*)p->ai_addr;
            inet_ntop(AF_INET6, &s->sin6_addr, ip, sizeof(ip));
        }
        std::cout << "[ga] 候选 " << ++count << ": " << ip << "\n";
    }
    freeaddrinfo(res);
    WSACleanup();
    return 0;
}
