#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Test: Python Compatibility Check
File: test_python_compatibility.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 10, 2025
Description: Tests to ensure the crawler works properly with Python 3.8+
             and validates that all modern Python features are supported.
=============================================================================
"""

import sys
import asyncio
import unittest
from pathlib import Path


def safe_print(text: str, fallback: str = None):
    """安全打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        if fallback:
            print(fallback)
        else:
            # 移除中文字符，只保留ASCII字符
            ascii_text = ''.join(char for char in text if ord(char) < 128)
            print(ascii_text)


class TestPythonCompatibility(unittest.TestCase):
    """测试Python兼容性"""

    def test_python_version(self):
        """测试Python版本是否满足要求"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3, "需要Python 3.x")
        self.assertGreaterEqual(version.minor, 8, "需要Python 3.8或更高版本")
        safe_print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}",
                   f"✓ Python version check passed: {version.major}.{version.minor}.{version.micro}")

    def test_asyncio_support(self):
        """测试异步编程支持"""

        async def async_test():
            await asyncio.sleep(0.001)
            return "async_works"

        # 在Python 3.8+中，asyncio.run()应该可用
        if hasattr(asyncio, "run"):
            result = asyncio.run(async_test())
            self.assertEqual(result, "async_works")
            safe_print("✅ asyncio.run() 支持正常", "✓ asyncio.run() support normal")
        else:
            # 对于较老版本的备用方案
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(async_test())
            self.assertEqual(result, "async_works")
            safe_print("✅ asyncio 基本支持正常", "✓ asyncio basic support normal")

    def test_pathlib_support(self):
        """测试现代路径处理支持"""
        test_path = Path("test/path/file.txt")
        self.assertEqual(test_path.name, "file.txt")
        self.assertEqual(test_path.suffix, ".txt")
        self.assertEqual(test_path.parent.name, "path")
        safe_print("✅ pathlib 支持正常", "✓ pathlib support normal")

    def test_f_strings(self):
        """测试f-string支持（Python 3.6+）"""
        name = "JACoW"
        version = "1.0"
        formatted = f"{name} v{version}"
        self.assertEqual(formatted, "JACoW v1.0")
        safe_print("✅ f-string 支持正常", "✓ f-string support normal")

    def test_type_hints(self):
        """测试类型提示支持（Python 3.5+）"""
        from typing import List, Dict, Optional

        def test_function(items: List[str]) -> Dict[str, int]:
            return {item: len(item) for item in items}

        result = test_function(["hello", "world"])
        self.assertEqual(result, {"hello": 5, "world": 5})
        safe_print("✅ 类型提示支持正常", "✓ type hints support normal")

    def test_walrus_operator(self):
        """测试海象操作符支持（Python 3.8+）"""
        try:
            # 尝试使用海象操作符
            test_list = [1, 2, 3, 4, 5]
            filtered = [y for x in test_list if (y := x * 2) > 4]
            self.assertEqual(filtered, [6, 8, 10])
            safe_print("✅ 海象操作符支持正常", "✓ walrus operator support normal")
        except SyntaxError:
            self.fail("海象操作符不支持，需要Python 3.9+")

    def test_positional_only_parameters(self):
        """测试仅位置参数支持（Python 3.9+）"""

        def test_func(a, b, /, c=None):
            return a + b + (c or 0)

        result = test_func(1, 2, c=3)
        self.assertEqual(result, 6)

        # 这应该可以工作
        result2 = test_func(1, 2)
        self.assertEqual(result2, 3)

        safe_print("✅ 仅位置参数支持正常", "✓ positional-only parameters support normal")


if __name__ == "__main__":
    import sys
    
    # 设置标准输出编码为UTF-8以支持中文字符
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except (AttributeError, OSError):
            pass
    
    safe_print("JACoW 爬虫 - Python 兼容性测试", "JACoW Crawler - Python Compatibility Test")
    safe_print("=" * 50, "=" * 50)
    
    unittest.main(verbosity=2)
