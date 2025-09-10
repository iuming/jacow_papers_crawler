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


class TestPythonCompatibility(unittest.TestCase):
    """测试Python兼容性"""
    
    def test_python_version(self):
        """测试Python版本是否满足要求"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3, "需要Python 3.x")
        self.assertGreaterEqual(version.minor, 8, "需要Python 3.8或更高版本")
        print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    
    def test_asyncio_support(self):
        """测试异步编程支持"""
        async def async_test():
            await asyncio.sleep(0.001)
            return "async_works"
        
        # 在Python 3.8+中，asyncio.run()应该可用
        if hasattr(asyncio, 'run'):
            result = asyncio.run(async_test())
            self.assertEqual(result, "async_works")
            print("✅ asyncio.run() 支持正常")
        else:
            # 对于较老版本的备用方案
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(async_test())
            self.assertEqual(result, "async_works")
            print("✅ asyncio 基本支持正常")
    
    def test_pathlib_support(self):
        """测试现代路径处理支持"""
        test_path = Path("test/path/file.txt")
        self.assertEqual(test_path.name, "file.txt")
        self.assertEqual(test_path.suffix, ".txt")
        self.assertEqual(test_path.parent.name, "path")
        print("✅ pathlib 支持正常")
    
    def test_f_strings(self):
        """测试f-string支持（Python 3.6+）"""
        name = "JACoW"
        version = "1.0"
        formatted = f"{name} v{version}"
        self.assertEqual(formatted, "JACoW v1.0")
        print("✅ f-string 支持正常")
    
    def test_type_hints(self):
        """测试类型提示支持（Python 3.5+）"""
        from typing import List, Dict, Optional
        
        def test_function(items: List[str]) -> Dict[str, int]:
            return {item: len(item) for item in items}
        
        result = test_function(["hello", "world"])
        self.assertEqual(result, {"hello": 5, "world": 5})
        print("✅ 类型提示支持正常")
    
    def test_walrus_operator(self):
        """测试海象操作符支持（Python 3.8+）"""
        try:
            # 尝试使用海象操作符
            test_list = [1, 2, 3, 4, 5]
            filtered = [y for x in test_list if (y := x * 2) > 4]
            self.assertEqual(filtered, [6, 8, 10])
            print("✅ 海象操作符支持正常")
        except SyntaxError:
            self.fail("海象操作符不支持，需要Python 3.8+")
    
    def test_positional_only_parameters(self):
        """测试仅位置参数支持（Python 3.8+）"""
        def test_func(a, b, /, c=None):
            return a + b + (c or 0)
        
        result = test_func(1, 2, c=3)
        self.assertEqual(result, 6)
        
        # 这应该可以工作
        result2 = test_func(1, 2)
        self.assertEqual(result2, 3)
        
        print("✅ 仅位置参数支持正常")


if __name__ == "__main__":
    print("JACoW 爬虫 - Python 兼容性测试")
    print("=" * 50)
    unittest.main(verbosity=2)
