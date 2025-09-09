#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本
"""

import unittest
import sys
from pathlib import Path
import tempfile
import shutil

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.config import Config
from utils.helpers import (
    sanitize_filename, get_file_extension_from_url,
    extract_year_from_text, format_file_size
)
from crawler.classifier import PaperClassifier


class TestHelpers(unittest.TestCase):
    """测试辅助函数"""
    
    def test_sanitize_filename(self):
        """测试文件名清理"""
        # 测试非法字符
        self.assertEqual(
            sanitize_filename('test<>:"/\\|?*.pdf'),
            'test_________.pdf'
        )
        
        # 测试长度限制
        long_name = 'a' * 300 + '.pdf'
        result = sanitize_filename(long_name, max_length=50)
        self.assertLessEqual(len(result), 50)
        self.assertTrue(result.endswith('.pdf'))
        
        # 测试空文件名
        self.assertEqual(sanitize_filename(''), 'untitled')
    
    def test_get_file_extension_from_url(self):
        """测试从URL获取扩展名"""
        # 直接URL
        self.assertEqual(
            get_file_extension_from_url('https://example.com/paper.pdf'),
            '.pdf'
        )
        
        # 带查询参数的URL
        self.assertEqual(
            get_file_extension_from_url('https://example.com/download?file=paper.pdf'),
            ''
        )
        
        # 带filename参数的URL
        self.assertEqual(
            get_file_extension_from_url('https://example.com/download?filename=paper.pdf'),
            '.pdf'
        )
    
    def test_extract_year_from_text(self):
        """测试从文本提取年份"""
        self.assertEqual(extract_year_from_text('IPAC 2023 Conference'), 2023)
        self.assertEqual(extract_year_from_text('Conference in 1999'), 1999)
        self.assertIsNone(extract_year_from_text('No year here'))
        self.assertIsNone(extract_year_from_text('Year 1900 too old'))
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        self.assertEqual(format_file_size(1024), '1.0 KB')
        self.assertEqual(format_file_size(1024 * 1024), '1.0 MB')
        self.assertEqual(format_file_size(1024 * 1024 * 1024), '1.0 GB')


class TestConfig(unittest.TestCase):
    """测试配置类"""
    
    def setUp(self):
        self.config = Config()
    
    def test_classification_keywords(self):
        """测试分类关键词"""
        # 测试RF技术分类
        result = self.config.classify_by_keywords('RF cavity design for accelerators')
        self.assertIn(result, ['RF_Technology', 'Accelerator_Technology'])  # 两个都可能匹配
        
        # 测试束流动力学分类  
        self.assertEqual(
            self.config.classify_by_keywords('Beam dynamics simulation and optics'),
            'Beam_Dynamics'
        )
        
        # 测试默认分类
        self.assertEqual(
            self.config.classify_by_keywords('Random topic with no keywords'),
            'Other'
        )
    
    def test_is_supported_file(self):
        """测试支持的文件类型"""
        self.assertTrue(self.config.is_supported_file('paper.pdf'))
        self.assertTrue(self.config.is_supported_file('document.doc'))
        self.assertTrue(self.config.is_supported_file('presentation.ppt'))
        self.assertFalse(self.config.is_supported_file('image.jpg'))
        self.assertFalse(self.config.is_supported_file('archive.zip'))
    
    def test_get_conference_from_url(self):
        """测试从URL提取会议名"""
        self.assertEqual(
            self.config.get_conference_from_url('https://jacow.org/ipac2023/'),
            'IPAC'
        )
        self.assertEqual(
            self.config.get_conference_from_url('https://jacow.org/linac2022/'),
            'LINAC'
        )
        self.assertIsNone(
            self.config.get_conference_from_url('https://jacow.org/unknown/')
        )


class TestClassifier(unittest.TestCase):
    """测试分类器"""
    
    def setUp(self):
        # 创建临时目录
        self.temp_dir = Path(tempfile.mkdtemp())
        self.classifier = PaperClassifier(self.temp_dir)
    
    def tearDown(self):
        # 清理临时目录
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_classification_stats(self):
        """测试分类统计"""
        # 创建测试数据
        test_results = [
            {
                'title': 'RF Technology Paper',
                'conference': 'IPAC',
                'year': 2023,
                'success': True,
                'file_path': str(self.temp_dir / 'test1.pdf'),
                'abstract': 'RF cavity development'
            },
            {
                'title': 'Beam Dynamics Paper',
                'conference': 'IPAC',
                'year': 2023,
                'success': True,
                'file_path': str(self.temp_dir / 'test2.pdf'),
                'abstract': 'Beam optics simulation'
            }
        ]
        
        # 创建测试文件
        for result in test_results:
            Path(result['file_path']).touch()
        
        # 执行分类
        stats = self.classifier.classify_papers(test_results)
        
        # 检查结果
        self.assertIn('IPAC/2023', stats)
        self.assertEqual(stats['IPAC/2023'], 2)


def run_tests():
    """运行所有测试"""
    print("运行JACoW爬虫测试...")
    print("=" * 50)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTest(unittest.makeSuite(TestHelpers))
    test_suite.addTest(unittest.makeSuite(TestConfig))
    test_suite.addTest(unittest.makeSuite(TestClassifier))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出结果
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
        print(f"失败: {len(result.failures)} 个")
        print(f"错误: {len(result.errors)} 个")
    
    print(f"总计运行: {result.testsRun} 个测试")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
