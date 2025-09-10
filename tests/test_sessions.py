#!/usr/bin/env python3
"""
直接测试已知的session URLs
基于之前fetch_webpage获取的内容
"""

import asyncio
import aiohttp
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

# 基于之前看到的session列表
KNOWN_SESSIONS = [
    "221-supm",
    "172-moxd",
    "173-moyd",
    "163-mozd",
    "162-mozg",
    "175-mood",
    "174-moog",
    "238-mopa",  # 这个我们之前测试过
    "237-mopl",
    "236-mopm",
]


async def test_known_sessions():
    """测试已知的session URLs"""
    base_url = "https://proceedings.jacow.org/ipac2023"

    async with aiohttp.ClientSession() as session:
        print(f"🔍 测试已知sessions")

        working_sessions = []

        for session_code in KNOWN_SESSIONS[:5]:  # 只测试前5个
            session_path = f"{session_code}/index.html"
            full_url = urljoin(f"{base_url}/session/", session_path)

            print(f"\n📄 测试: {full_url}")

            try:
                async with session.get(full_url) as response:
                    if response.status == 200:
                        content = await response.text()

                        # 查找PDF链接
                        pdf_pattern = r'href="([^"]*\.pdf)"'
                        pdf_matches = re.findall(pdf_pattern, content)

                        individual_papers = []
                        for pdf_url in pdf_matches:
                            # 检查是否为单篇论文
                            if re.search(
                                r"[A-Z]{2,4}\d{3}\.pdf$", pdf_url, re.IGNORECASE
                            ):
                                individual_papers.append(pdf_url)

                        print(f"  ✅ 成功! 找到 {len(individual_papers)} 篇单独论文")
                        if individual_papers:
                            working_sessions.append(full_url)
                            for i, paper in enumerate(individual_papers[:3], 1):
                                print(f"    {i}. {paper}")
                            if len(individual_papers) > 3:
                                print(f"    ... 还有 {len(individual_papers) - 3} 篇")
                    else:
                        print(f"  ❌ HTTP {response.status}")

            except Exception as e:
                print(f"  ❌ 错误: {e}")

        return working_sessions


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    working_sessions = asyncio.run(test_known_sessions())
    print(f"\n🎉 工作的sessions: {len(working_sessions)}个")
    for url in working_sessions:
        print(f"  ✅ {url}")
