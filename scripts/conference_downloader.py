#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按会议下载所有单篇论文的专用工具
"""

import asyncio
import aiohttp
import re
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys


async def download_conference_papers(conference_name, year, max_size_mb=50):
    """
    下载指定会议的所有单篇论文

    Args:
        conference_name: 会议名称 (如 'IPAC', 'LINAC')
        year: 年份 (如 2023)
        max_size_mb: 最大文件大小限制(MB)
    """
    print(f"🎯 准备下载 {conference_name} {year} 会议的所有单篇论文")
    print(f"📏 文件大小限制: {max_size_mb}MB")
    print("=" * 60)

    # 构建会议URL
    conference_url = f"https://proceedings.jacow.org/{conference_name.lower()}{year}/"
    session_index_url = urljoin(conference_url, "session/index.html")

    async with aiohttp.ClientSession() as session:
        print(f"🌐 访问会议主页: {conference_url}")

        # 获取session列表
        try:
            async with session.get(session_index_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # 查找所有session链接
                    session_links = []
                    for link in soup.find_all("a", href=True):
                        href = link["href"]
                        if (
                            "session" in href
                            and "index.html" in href
                            and link.get_text(strip=True)
                        ):
                            full_url = urljoin(session_index_url, href)
                            session_links.append(
                                {"name": link.get_text(strip=True), "url": full_url}
                            )

                    print(f"✅ 找到 {len(session_links)} 个session")

                    # 遍历每个session获取论文
                    all_papers = []
                    for i, session_info in enumerate(session_links, 1):
                        print(
                            f"\n📑 处理Session {i}/{len(session_links)}: {session_info['name']}"
                        )

                        try:
                            async with session.get(
                                session_info["url"]
                            ) as session_response:
                                if session_response.status == 200:
                                    session_html = await session_response.text()
                                    papers = extract_papers_from_session(
                                        session_html, session_info["url"]
                                    )

                                    if papers:
                                        print(f"   📄 找到 {len(papers)} 篇论文")
                                        all_papers.extend(papers)
                                    else:
                                        print(f"   ⚠️ 未找到论文")
                                else:
                                    print(
                                        f"   ❌ 无法访问 (状态码: {session_response.status})"
                                    )
                        except Exception as e:
                            print(f"   ❌ 处理出错: {e}")

                        # 避免请求过快
                        await asyncio.sleep(1)

                    print(f"\n🎉 总共找到 {len(all_papers)} 篇单独论文")

                    # 显示前10篇论文作为示例
                    print(f"\n📋 论文列表预览（前10篇）:")
                    for i, paper in enumerate(all_papers[:10], 1):
                        print(f"{i:2d}. {paper['code']} - {paper['title'][:60]}...")
                        print(f"    URL: {paper['url']}")

                    if len(all_papers) > 10:
                        print(f"    ... 还有 {len(all_papers) - 10} 篇论文")

                    return all_papers
                else:
                    print(f"❌ 无法访问会议页面 (状态码: {response.status})")
                    return []
        except Exception as e:
            print(f"❌ 获取会议信息失败: {e}")
            return []


def extract_papers_from_session(html, base_url):
    """从session页面提取论文信息"""
    soup = BeautifulSoup(html, "html.parser")
    papers = []

    # 查找所有PDF链接
    pdf_links = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))

    for link in pdf_links:
        href = link.get("href")
        if href and is_individual_paper(href):
            # 构建完整URL
            if href.startswith("http"):
                paper_url = href
            else:
                paper_url = urljoin(base_url, href)

            # 提取论文代码
            paper_code = href.split("/")[-1].replace(".pdf", "")

            # 提取标题（简化版）
            title = extract_title_from_context(link, paper_code)

            papers.append(
                {
                    "code": paper_code,
                    "title": title,
                    "url": paper_url,
                    "session": extract_session_from_url(base_url),
                }
            )

    return papers


def is_individual_paper(url):
    """判断是否是单篇论文"""
    filename = url.split("/")[-1].lower()

    # 排除论文集
    exclude_patterns = ["proceedings", "complete", "full", "volume", "brief"]
    if any(pattern in filename for pattern in exclude_patterns):
        return False

    # 单篇论文模式
    import re

    individual_patterns = [
        r"^[A-Z]{2,4}[A-Z0-9]{2,6}\.pdf$",
        r"^[A-Z]{2,6}\d{2,4}\.pdf$",
    ]

    for pattern in individual_patterns:
        if re.match(pattern, filename, re.IGNORECASE):
            return True

    return len(filename) < 20 and bool(re.search(r"\d", filename))


def extract_title_from_context(link, paper_code):
    """从上下文提取论文标题"""
    # 简化的标题提取
    parent = link.parent
    if parent:
        parent_text = parent.get_text(strip=True)
        # 查找论文代码后的文本作为标题
        code_index = parent_text.find(paper_code)
        if code_index >= 0:
            title_start = code_index + len(paper_code)
            title = parent_text[title_start:].strip()
            # 清理标题
            title = re.sub(r"^[^\w]*", "", title)  # 去掉开头的标点
            title = title.split("■")[0]  # 去掉作者信息
            title = title.split("DOI:")[0]  # 去掉DOI信息
            if len(title) > 10:
                return title[:100]  # 限制长度

    return paper_code


def extract_session_from_url(url):
    """从URL提取session信息"""
    if "/session/" in url:
        session_part = url.split("/session/")[-1]
        session_code = session_part.split("/")[0]
        session_match = re.search(r"(\d+-)?(.+)", session_code)
        if session_match:
            return session_match.group(2).upper()
    return "unknown"


async def main():
    """主函数"""
    print("🎯 JACoW会议单篇论文批量下载工具")
    print("=" * 60)

    if len(sys.argv) < 3:
        print("使用方法:")
        print("python conference_downloader.py <会议名> <年份> [最大文件大小MB]")
        print()
        print("示例:")
        print("python conference_downloader.py IPAC 2023")
        print("python conference_downloader.py IPAC 2023 30")
        print("python conference_downloader.py LINAC 2022 50")
        return

    conference = sys.argv[1].upper()
    year = int(sys.argv[2])
    max_size = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    papers = await download_conference_papers(conference, year, max_size)

    if papers:
        print(f"\n✅ 成功获取 {len(papers)} 篇论文信息")
        print(f"\n💡 你现在可以用这些URL来下载论文：")
        print(f"   - 使用现有的下载器")
        print(f"   - 或者添加实际下载功能")
        print(f"\n🎊 {conference} {year} 会议单篇论文获取完成！")
    else:
        print(f"\n❌ 未能获取到论文信息")


if __name__ == "__main__":
    asyncio.run(main())
