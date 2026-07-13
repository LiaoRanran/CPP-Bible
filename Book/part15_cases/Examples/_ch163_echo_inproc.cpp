// _ch163_echo_inproc.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_echo_inproc.cpp -lws2_32 -o _ch163_echo_inproc.exe
// 行为: 单进程内拉起 server 线程 + client，经 127.0.0.1:54322 回显（确定性证据）。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstring>

static const int PORT = 54322;

void server_thread(std::atomic<bool>* ready) {
    SOCKET lfd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    bind(lfd, (sockaddr*)&a, sizeof(a));
    listen(lfd, 1);
    *ready = true;
    SOCKET c = accept(lfd, nullptr, nullptr);
    char buf[256];
    int n = recv(c, buf, sizeof(buf) - 1, 0);
    buf[n] = '\0';
    std::cout << "[server] got: " << buf << std::flush;
    send(c, buf, n, 0);
    std::cout << "[server] echoed " << n << " bytes\n" << std::flush;
    closesocket(c);
    closesocket(lfd);
}

int main() {
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);

    std::atomic<bool> ready{false};
    std::thread srv(server_thread, &ready);
    while (!ready) std::this_thread::sleep_for(std::chrono::milliseconds(5));

    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    connect(fd, (sockaddr*)&a, sizeof(a));

    const char* m = "ping-pong-163\n";
    send(fd, m, (int)std::strlen(m), 0);
    std::cout << "[client] sent: " << m << std::flush;

    char buf[256];
    int n = recv(fd, buf, sizeof(buf) - 1, 0);
    buf[n] = '\0';
    std::cout << "[client] received: " << buf << std::flush;

    closesocket(fd);
    srv.join();
    WSACleanup();
    return 0;
}
