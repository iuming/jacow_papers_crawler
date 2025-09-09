#!/usr/bin/env python3
"""
直接测试MOPA session
我们之前在fetch_webpage中看到了MOPA001.pdf等
"""

import asyncio
import aiohttp
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

async def test_mopa_session():
    """测试MOPA session，我们之前确认有论文"""
    base_url = "https://proceedings.jacow.org/ipac2023"
    session_url = f"{base_url}/session/238-mopa/index.html"
    
    async with aiohttp.ClientSession() as session:
        print(f"🔍 测试MOPA session: {session_url}")
        
        try:
            async with session.get(session_url) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"✅ 页面大小: {len(content)} 字符")
                    
                    # 打印部分内容查看结构
                    print(f"\n📋 内容样本 (前500字符):")
                    print(content[:500])
                    
                    # 查找所有PDF链接
                    pdf_pattern = r'href="([^"]*\.pdf)"'
                    pdf_matches = re.findall(pdf_pattern, content)
                    
                    print(f"\n🔗 找到 {len(pdf_matches)} 个PDF链接:")
                    for i, pdf_url in enumerate(pdf_matches, 1):
                        print(f"  {i}. {pdf_url}")
                    
                    # 查找MOPA模式的论文
                    mopa_pattern = r'MOPA\d+'
                    mopa_matches = re.findall(mopa_pattern, content)
                    
                    print(f"\n📄 找到MOPA论文代码: {len(mopa_matches)}个")
                    for i, code in enumerate(set(mopa_matches), 1):
                        print(f"  {i}. {code}")
                    
                    # 查找完整的PDF URL模式
                    full_pdf_pattern = r'(https?://[^"]*MOPA\d+\.pdf)'
                    full_pdf_matches = re.findall(full_pdf_pattern, content)
                    
                    print(f"\n🎯 完整PDF URLs: {len(full_pdf_matches)}个")
                    for i, url in enumerate(full_pdf_matches, 1):
                        print(f"  {i}. {url}")
                        
                else:
                    print(f"❌ HTTP {response.status}")
                    
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(test_mopa_session())
