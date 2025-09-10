#!/usr/bin/env python3
"""
从网页内容中解析session链接
基于之前获取的实际网页内容
"""

import re
import asyncio
import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys


async def extract_sessions_from_content():
    """从HTML内容中提取session信息"""
    base_url = "https://proceedings.jacow.org/ipac2023"
    session_url = f"{base_url}/session/index.html"

    async with aiohttp.ClientSession() as session:
        print(f"🔍 正在分析: {session_url}")

        try:
            async with session.get(session_url) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"✅ 页面大小: {len(content)} 字符")

                    # 查找session文本内容，它们包含在HTML中
                    # 基于之前看到的模式：[MOPA - Monday Poster Session: MOPA]
                    session_pattern = r"\[([A-Z]{2,6})\s*-\s*([^]]+)\]\(([^)]+)\)"
                    matches = re.findall(session_pattern, content)

                    print(f"\n🎯 找到session模式匹配: {len(matches)}个")
                    for i, (code, description, url) in enumerate(matches[:10], 1):
                        print(f"  {i}. {code}: {description[:30]}... -> {url}")

                    # 另一种方法：查找特定的href模式
                    # 基于看到的URL：proceedings.jacow.org/ipac2023/session/238-mopa/index.html
                    href_pattern = r'href="([^"]*session/[^"]*index\.html)"'
                    href_matches = re.findall(href_pattern, content)

                    print(f"\n🔗 找到href模式匹配: {len(href_matches)}个")
                    for i, url in enumerate(href_matches[:10], 1):
                        print(f"  {i}. {url}")

                    # 直接搜索session数字-字母模式
                    session_code_pattern = r"(\d+)-([a-z]+)/index\.html"
                    code_matches = re.findall(session_code_pattern, content)

                    print(f"\n📊 找到session代码: {len(code_matches)}个")
                    sessions = []
                    for i, (number, code) in enumerate(code_matches[:15], 1):
                        session_path = f"{number}-{code}/index.html"
                        full_url = urljoin(f"{base_url}/session/", session_path)
                        sessions.append(full_url)
                        print(f"  {i}. {session_path} -> {full_url}")

                    return sessions

                else:
                    print(f"❌ HTTP {response.status}")
                    return []

        except Exception as e:
            print(f"❌ 错误: {e}")
            return []


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    sessions = asyncio.run(extract_sessions_from_content())
    print(f"\n🎉 总共找到 {len(sessions)} 个sessions")
