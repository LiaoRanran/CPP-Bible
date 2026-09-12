"""pytest 公共配置：把 tools/ 加入 import 路径。

本仓库 80+ 个工具脚本此前**零单元测试**（工具正确性仅靠 CI 跑通间接验证）。
本目录的测试专门锁定**真实发生过的回归**，详见各文件的 docstring。
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
