// sample_G081
// defect_type: double_free
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-2384 (https://nvd.nist.gov/vuln/detail/CVE-2016-2384) [linux-kernel]
// (authoritative annotation in sample_G081.json)
#include <cstdio>
// CVE-2016-2384 (用户态等价): 错误路径与调用方双重释放 USB 接口对象
struct UsbInterface {
    int refs;
};

static void usb_if_put(UsbInterface* iface) {
    delete iface;
}

static int snd_usbmidi_create(UsbInterface* iface, bool invalid_descriptor) {
    if (invalid_descriptor) {
        /* DEFECT */ usb_if_put(iface);   // 错误路径释放(第一次)
        std::printf("usbmidi: error path freed interface\n");
        return -1;
    }
    return 0;
}

int main() {
    UsbInterface* iface = new UsbInterface{ 1 };
    // crafted USB 设备: MIDI 端点描述符无效
    if (snd_usbmidi_create(iface, true) < 0) {
        usb_if_put(iface);   /* DEFECT */ // 调用方错误处理再次释放 → double free
    }
    return 0;
}
