#!/usr/bin/env python3
"""
调试JACoW session链接提取
"""

import asyncio
import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

async def debug_session_links():
    """调试session链接提取"""
    base_url = "https://proceedings.jacow.org/ipac2023"
    session_url = f"{base_url}/session/index.html"
    
    async with aiohttp.ClientSession() as session:
        print(f"🔍 正在调试: {session_url}")
        
        try:
            async with session.get(session_url) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"✅ 页面大小: {len(content)} 字符")
                    
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # 查找所有链接
                    all_links = []
                    for link in soup.find_all('a', href=True):
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        all_links.append((href, text))
                    
                    print(f"\n📄 所有链接:")
                    for i, (href, text) in enumerate(all_links, 1):
                        print(f"  {i}. '{href}' -> '{text[:30]}...'")
                    
                    # 分析可能的session链接
                    potential_sessions = []
                    for href, text in all_links:
                        # 寻找符合session模式的链接 - 更宽松的匹配
                        if href.endswith('.html') and href != 'index.html':
                            potential_sessions.append((href, text))
                    
                    print(f"\n🎯 可能的session链接 ({len(potential_sessions)}个):")
                    for i, (href, text) in enumerate(potential_sessions, 1):
                        print(f"  {i}. '{href}' -> '{text[:50]}...'")
                    
                    # 特别查找数字-字母模式的链接
                    numeric_sessions = []
                    for href, text in all_links:
                        # 寻找类似 "221-supm/index.html" 的模式
                        if '/' in href and href.endswith('/index.html'):
                            numeric_sessions.append((href, text))
                    
                    print(f"\n🔢 数字模式session链接 ({len(numeric_sessions)}个):")
                    for i, (href, text) in enumerate(numeric_sessions, 1):
                        print(f"  {i}. '{href}' -> '{text[:50]}...'")
                        if i >= 10:
                            print(f"  ... 还有 {len(numeric_sessions) - 10} 个")
                            break
                    
                    # 生成完整URL
                    if potential_sessions:
                        print(f"\n🌐 生成的完整session URLs:")
                        for i, (href, text) in enumerate(potential_sessions[:5], 1):
                            full_url = urljoin(f"{base_url}/session/", href)
                            print(f"  {i}. {full_url}")
                    
                else:
                    print(f"❌ HTTP {response.status}")
                    
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(debug_session_links())
