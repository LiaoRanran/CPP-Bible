// _ch163_echo_server.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_echo_server.cpp -lws2_32 -o _ch163_echo_server.exe
// 行为: 绑定 127.0.0.1:54321，accept 一个连接，逐行回显，客户端关闭后退出。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>

int main() {
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "[server] WSAStartup 失败\n";
        return 1;
    }
    SOCKET listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(54321);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    if (bind(listen_fd, (sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "[server] bind 失败, code=" << WSAGetLastError() << "\n";
        return 1;
    }
    listen(listen_fd, 1);
    std::cout << "[server] listening on 127.0.0.1:54321\n" << std::flush;

    SOCKET conn = accept(listen_fd, nullptr, nullptr);
    std::cout << "[server] accepted a client\n" << std::flush;

    char buf[256];
    int n;
    while ((n = recv(conn, buf, sizeof(buf) - 1, 0)) > 0) {
        buf[n] = '\0';
        std::cout << "[server] recv: " << buf << std::flush;
        send(conn, buf, n, 0);
        std::cout << "[server] echo " << n << " bytes\n" << std::flush;
    }
    std::cout << "[server] client closed, bye\n" << std::flush;
    closesocket(conn);
    closesocket(listen_fd);
    WSACleanup();
    return 0;
}
