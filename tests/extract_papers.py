#!/usr/bin/env python3
"""
正确解析JACoW session中的PDF链接
使用data-href属性
"""

import asyncio
import aiohttp
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys


async def extract_papers_from_mopa():
    """从MOPA session正确提取PDF链接"""
    base_url = "https://proceedings.jacow.org/ipac2023"
    session_url = f"{base_url}/session/238-mopa/index.html"

    async with aiohttp.ClientSession() as session:
        print(f"🔍 正确解析MOPA session: {session_url}")

        try:
            async with session.get(session_url) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"✅ 页面大小: {len(content)} 字符")

                    soup = BeautifulSoup(content, "html.parser")

                    # 查找具有data-href属性的链接
                    data_href_links = soup.find_all("a", attrs={"data-href": True})
                    print(f"\n🔗 找到 {len(data_href_links)} 个data-href链接")

                    individual_papers = []
                    for link in data_href_links:
                        data_href = link.get("data-href", "")

                        # 检查是否为单篇PDF论文
                        if data_href.endswith(".pdf") and "MOPA" in data_href:
                            # 构建完整URL
                            full_url = urljoin(session_url, data_href)

                            # 提取论文ID
                            paper_id = data_href.split("/")[-1].replace(".pdf", "")

                            # 获取论文标题
                            title = link.get_text(strip=True) or paper_id

                            individual_papers.append(
                                {
                                    "id": paper_id,
                                    "url": full_url,
                                    "title": title,
                                    "relative_path": data_href,
                                }
                            )

                    print(f"\n📄 找到 {len(individual_papers)} 篇单独论文:")
                    for i, paper in enumerate(individual_papers[:10], 1):
                        print(f"  {i}. {paper['id']}: {paper['title'][:40]}...")
                        print(f"      URL: {paper['url']}")

                    if len(individual_papers) > 10:
                        print(f"  ... 还有 {len(individual_papers) - 10} 篇论文")

                    return individual_papers

                else:
                    print(f"❌ HTTP {response.status}")
                    return []

        except Exception as e:
            print(f"❌ 错误: {e}")
            return []


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    papers = asyncio.run(extract_papers_from_mopa())
    print(f"\n🎉 成功提取 {len(papers)} 篇论文")
