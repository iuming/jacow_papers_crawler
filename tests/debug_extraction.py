#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试单篇论文提取功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

async def debug_paper_extraction():
    """调试论文提取过程"""
    print("🔍 调试单篇论文提取过程")
    
    try:
        from crawler.individual_spider import JACoWIndividualPaperSpider
        from utils.logger import setup_logger
        from bs4 import BeautifulSoup
        
        # 设置日志
        logger = setup_logger("debug", level="DEBUG")
        
        # 初始化爬虫
        spider = JACoWIndividualPaperSpider(delay=1.0, logger=logger)
        
        # 测试页面
        session_url = "https://proceedings.jacow.org/ipac2023/session/238-mopa/index.html"
        print(f"\n📄 获取页面内容: {session_url}")
        
        html = await spider._fetch_page(session_url)
        if html:
            print(f"✅ 成功获取页面 ({len(html)} 字符)")
            
            # 解析HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找所有PDF链接
            pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
            print(f"\n🔗 找到 {len(pdf_links)} 个PDF链接:")
            
            for i, link in enumerate(pdf_links[:10], 1):  # 只显示前10个
                href = link.get('href')
                text = link.get_text(strip=True)
                is_individual = spider._is_individual_paper(href) if href else False
                
                print(f"  {i}. {href}")
                print(f"     文本: {text}")
                print(f"     单篇论文: {'✅' if is_individual else '❌'}")
                print()
            
            # 查找"Paper:"文本
            paper_texts = soup.find_all(text=lambda text: text and 'paper:' in text.lower())
            print(f"\n📝 找到 {len(paper_texts)} 个'Paper:'文本")
            
            # 测试论文信息提取
            print(f"\n🔍 测试论文信息提取:")
            extracted_papers = []
            
            for link in pdf_links:
                paper = spider._extract_paper_info_from_link(link, session_url)
                if paper:
                    extracted_papers.append(paper)
            
            print(f"✅ 成功提取 {len(extracted_papers)} 篇论文信息")
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_paper_extraction())
