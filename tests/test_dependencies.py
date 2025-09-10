#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Test: Dependency Compatibility Check
File: test_dependencies.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 10, 2025
Description: Tests to ensure all required packages are properly installed
             and compatible with the current Python version.
=============================================================================
"""

import sys
import unittest
from packaging import version


class TestDependencies(unittest.TestCase):
    """测试依赖包兼容性"""

    def test_core_dependencies(self):
        """测试核心依赖包"""
        try:
            import requests
            import aiohttp
            import aiofiles

            print("✅ 核心HTTP库导入成功")
        except ImportError as e:
            self.fail(f"核心依赖包导入失败: {e}")

    def test_parsing_dependencies(self):
        """测试解析相关依赖包"""
        try:
            import bs4
            import lxml

            print("✅ 解析库导入成功")
        except ImportError as e:
            self.fail(f"解析依赖包导入失败: {e}")

    def test_data_dependencies(self):
        """测试数据处理依赖包"""
        try:
            import pandas as pd
            import openpyxl

            # 检查pandas版本兼容性
            pandas_version = version.parse(pd.__version__)
            python_version = sys.version_info

            if python_version >= (3, 9):
                # Python 3.9+ 可以使用更新的pandas
                self.assertGreaterEqual(pandas_version, version.parse("2.0.0"))
            else:
                # 不应该到达这里，因为我们现在要求 Python 3.9+
                self.fail("需要 Python 3.9 或更高版本")

            print(f"✅ 数据处理库导入成功 (pandas {pd.__version__})")
        except ImportError as e:
            self.fail(f"数据处理依赖包导入失败: {e}")

    def test_ui_dependencies(self):
        """测试用户界面依赖包"""
        try:
            import tqdm
            import rich

            print("✅ UI库导入成功")
        except ImportError as e:
            self.fail(f"UI依赖包导入失败: {e}")

    def test_network_dependencies(self):
        """测试网络相关依赖包"""
        try:
            import urllib3
            import fake_useragent

            print("✅ 网络库导入成功")
        except ImportError as e:
            self.fail(f"网络依赖包导入失败: {e}")

    def test_optional_dependencies(self):
        """测试可选依赖包"""
        optional_imports = []

        try:
            import selenium

            optional_imports.append("selenium")
        except ImportError:
            print("⚠️  Selenium 未安装 (可选)")

        try:
            import webdriver_manager

            optional_imports.append("webdriver_manager")
        except ImportError:
            print("⚠️  WebDriver Manager 未安装 (可选)")

        if optional_imports:
            print(f"✅ 可选依赖包: {', '.join(optional_imports)}")

    def test_version_compatibility(self):
        """测试版本兼容性"""
        python_version = sys.version_info

        # 测试Python版本特定的功能
        if python_version >= (3, 8):
            # 测试海象操作符
            test_list = [1, 2, 3]
            result = [y for x in test_list if (y := x * 2) > 2]
            self.assertEqual(result, [4, 6])
            print("✅ Python 3.8+ 特性支持正常")

        if python_version >= (3, 9):
            # 测试字典合并操作符
            dict1 = {"a": 1}
            dict2 = {"b": 2}
            merged = dict1 | dict2
            self.assertEqual(merged, {"a": 1, "b": 2})
            print("✅ Python 3.9+ 特性支持正常")


if __name__ == "__main__":
    print("JACoW 爬虫 - 依赖包兼容性测试")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print("=" * 50)
    unittest.main(verbosity=2)
