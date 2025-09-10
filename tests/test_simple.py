#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试单篇论文下载功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

async def test_simple():
    """简单测试"""
    print("🎯 测试单篇论文爬虫功能")
    
    try:
        # 导入模块
        from crawler.individual_spider import JACoWIndividualPaperSpider
        from utils.logger import setup_logger
        
        # 设置日志
        logger = setup_logger("test", level="INFO")
        
        # 初始化爬虫
        spider = JACoWIndividualPaperSpider(
            delay=1.0,
            logger=logger
        )
        
        print("✅ 成功导入和初始化爬虫")
        
        # 测试URL判断功能
        test_urls = [
            "https://proceedings.jacow.org/ipac2023/pdf/MOPA001.pdf",  # 应该是单篇论文
            "https://proceedings.jacow.org/ipac2023/pdf/ipac-23_proceedings_volume.pdf",  # 应该是论文集
            "https://proceedings.jacow.org/ipac2023/pdf/TUPB123.pdf",  # 应该是单篇论文
        ]
        
        print("\n📋 测试论文类型判断:")
        for url in test_urls:
            is_individual = spider._is_individual_paper(url)
            filename = url.split('/')[-1]
            result = "✅ 单篇论文" if is_individual else "❌ 论文集"
            print(f"  {filename}: {result}")
        
        print("\n🌐 测试实际爬取（获取一个session的论文）...")
        
        # 直接测试一个已知的session页面
        session_url = "https://proceedings.jacow.org/ipac2023/session/238-mopa/index.html"
        papers = await spider._crawl_individual_papers_from_session(session_url)
        
        print(f"✅ 成功获取 {len(papers)} 篇论文")
        
        # 显示前5篇论文
        for i, paper in enumerate(papers[:5], 1):
            print(f"\n{i}. {paper.get('code', 'N/A')}")
            print(f"   标题: {paper.get('title', 'N/A')[:80]}...")
            print(f"   类型: {paper.get('type', 'N/A')}")
            print(f"   URL: {paper.get('url', 'N/A')}")
        
        if len(papers) > 5:
            print(f"\n... 还有 {len(papers)-5} 篇论文")
        
        print(f"\n🎉 测试完成！单篇论文爬虫功能正常工作")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple())
