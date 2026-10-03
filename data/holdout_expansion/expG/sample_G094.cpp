// sample_G094
// defect_type: global_overflow
// severity: medium
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: leethomason/tinyxml2#923 (https://github.com/leethomason/tinyxml2/issues/923) [tinyxml2]
// (authoritative annotation in sample_G094.json)
#include <cstdio>
// tinyxml2#923: ErrorIDToName 对 XML_ERROR_COUNT 越界读全局数组
enum XMLError {
    XML_SUCCESS = 0,
    XML_NO_ATTRIBUTE, XML_WRONG_ATTRIBUTE_TYPE, XML_ERROR_FILE_NOT_FOUND,
    XML_ERROR_FILE_COULD_NOT_BE_OPENED, XML_ERROR_FILE_READ_ERROR,
    XML_ERROR_PARSING_ELEMENT, XML_ERROR_PARSING_ATTRIBUTE,
    XML_ERROR_PARSING_TEXT, XML_ERROR_PARSING_CDATA, XML_ERROR_PARSING_COMMENT,
    XML_ERROR_PARSING_DECLARATION, XML_ERROR_PARSING_UNKNOWN,
    XML_ERROR_EMPTY_DOCUMENT, XML_ERROR_PARSING, XML_ERROR_PARSING_X,
    XML_ERROR_ELEMENT_MISMATCH, XML_ERROR_PARSING_ROOT_ELEMENT,
    XML_ERROR_PARSING_DOCUMENT, XML_ERROR_COUNT
    // _errorNames 数组只有 19 项(下标 0..18), XML_ERROR_COUNT = 19 → 越界下标
};

static const char* _errorNames[19] = {
    "XML_SUCCESS", "XML_NO_ATTRIBUTE", "XML_WRONG_ATTRIBUTE_TYPE",
    "XML_ERROR_FILE_NOT_FOUND", "XML_ERROR_FILE_COULD_NOT_BE_OPENED",
    "XML_ERROR_FILE_READ_ERROR", "XML_ERROR_PARSING_ELEMENT",
    "XML_ERROR_PARSING_ATTRIBUTE", "XML_ERROR_PARSING_TEXT",
    "XML_ERROR_PARSING_CDATA", "XML_ERROR_PARSING_COMMENT",
    "XML_ERROR_PARSING_DECLARATION", "XML_ERROR_PARSING_UNKNOWN",
    "XML_ERROR_EMPTY_DOCUMENT", "XML_ERROR_PARSING", "XML_ERROR_PARSING_X",
    "XML_ERROR_ELEMENT_MISMATCH", "XML_ERROR_PARSING_ROOT_ELEMENT",
    "XML_ERROR_PARSING_DOCUMENT"
};

static const char* ErrorIDToName(XMLError errorID) {
    /* DEFECT */ return _errorNames[errorID];   // errorID 可达 XML_ERROR_COUNT(19)? 数组下标 19 越界
}

int main() {
    // crafted 路径: 内部把 errorID 置为 XML_ERROR_COUNT(与 issue 一致)
    XMLError err = XML_ERROR_COUNT;
    std::printf("error name=%s\n", ErrorIDToName(err));   // 读 _errorNames[19] → 全局越界
    return 0;
}
