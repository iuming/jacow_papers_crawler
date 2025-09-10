#!/usr/bin/env python3
"""
Unit tests for crawler modules
"""

import pytest
import sys
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_crawler_imports():
    """测试crawler模块导入"""
    try:
        import crawler
        assert crawler is not None
    except ImportError as e:
        pytest.fail(f"Failed to import crawler: {e}")


def test_spider_import():
    """测试spider模块导入"""
    try:
        from crawler.spider import JACoWSpider
        assert JACoWSpider is not None
    except ImportError as e:
        pytest.fail(f"Failed to import JACoWSpider: {e}")


def test_individual_spider_import():
    """测试individual_spider模块导入"""
    try:
        from crawler.individual_spider import JACoWIndividualPaperSpider
        assert JACoWIndividualPaperSpider is not None
    except ImportError as e:
        pytest.fail(f"Failed to import JACoWIndividualPaperSpider: {e}")


def test_utils_imports():
    """测试utils模块导入"""
    try:
        from utils.config import Config
        from utils.logger import setup_logger
        from utils.helpers import sanitize_filename
        
        assert Config is not None
        assert setup_logger is not None
        assert sanitize_filename is not None
    except ImportError as e:
        pytest.fail(f"Failed to import utils: {e}")


def test_config_creation():
    """测试配置对象创建"""
    from utils.config import Config
    
    config = Config()
    assert hasattr(config, 'BASE_URL')
    assert config.BASE_URL == 'https://www.jacow.org'


def test_logger_creation():
    """测试日志器创建"""
    from utils.logger import setup_logger
    
    logger = setup_logger("test_logger")
    assert logger is not None
    assert logger.name == "test_logger"


def test_filename_sanitization():
    """测试文件名清理功能"""
    from utils.helpers import sanitize_filename
    
    # 测试基本清理 - 空格不会被替换
    assert sanitize_filename("test file.pdf") == "test file.pdf"
    assert sanitize_filename("test/file\\name.pdf") == "test_file_name.pdf"
    assert sanitize_filename("test:file<name>.pdf") == "test_file_name_.pdf"
    
    # 测试空字符串
    assert sanitize_filename("") == "untitled"
    
    # 测试只有扩展名 - 点号会被移除
    assert sanitize_filename(".pdf") == "pdf"
    
    # 测试前后空格移除
    assert sanitize_filename("  test.pdf  ") == "test.pdf"


@pytest.mark.unit
def test_spider_class_attributes():
    """测试Spider类属性"""
    from crawler.spider import JACoWSpider
    
    # 检查类是否有必要的属性
    assert hasattr(JACoWSpider, '__init__')
    
    # 创建实例测试
    spider = JACoWSpider()
    assert spider is not None
