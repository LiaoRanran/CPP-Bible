// RW-037 | CVE-2019-7317 | libpng | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-7317
// project_url: http://www.libpng.org/pub/png/libpng.html
// year: 2019 | severity: MEDIUM | source_type: cve
// mechanism: png_image_free（简化 API）在错误路径已释放图像结构，调用者继续
//   使用（双重清理顺序导致释放后使用）。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct PngImage {
    char name[32];
    unsigned char* pixels;
};

// BUG: frees the struct but the caller's cleanup then clears its fields.
void png_image_free(PngImage* img) {
    if (img->pixels) {
        std::free(img->pixels);
        img->pixels = nullptr;
    }
    std::free(img);                     // struct freed here
}

int main() {
    PngImage* img = static_cast<PngImage*>(std::malloc(sizeof(PngImage)));
    std::memset(img, 0, sizeof(PngImage));
    std::strcpy(img->name, "bad.png");
    img->pixels = static_cast<unsigned char*>(std::malloc(64));

    png_image_free(img);
    std::strcpy(img->name, "cleanup");  // use-after-free write
    std::printf("name after free: %s\n", img->name);
    return 0;
}
