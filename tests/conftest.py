#!/usr/bin/env python3
"""
pytest配置文件
确保测试时正确的Python路径设置
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """pytest配置"""
    # 确保项目根目录在Python路径中
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # 添加自定义标记
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
