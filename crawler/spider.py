#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: spider.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Core web spider module for crawling JACoW conference websites.
             Implements intelligent paper discovery, conference proceedings
             detection, and robust error handling for various JACoW site
             structures across different years and conferences.

Development Log:
- Sept 9, 2025: Initial spider implementation with basic crawling
- Sept 9, 2025: Added conference and year filtering capabilities
- Sept 9, 2025: Implemented robust URL pattern recognition
- Sept 9, 2025: Added retry mechanism and error handling
- Sept 9, 2025: Enhanced with proceedings vs individual paper detection

Features:
- Multi-year JACoW website structure support
- Automatic conference detection and filtering
- Rate-limited requests with configurable delays
- Comprehensive error handling and retry logic
- Paper metadata extraction (title, authors, conference)
- Progress tracking and detailed logging

Supported Conferences:
- IPAC (International Particle Accelerator Conference)
- LINAC (Linear Accelerator Conference)
- PAC (Particle Accelerator Conference)
- FEL (Free Electron Laser Conference)
- And other JACoW member conferences

Technical Details:
- Uses aiohttp for async HTTP requests
- BeautifulSoup4 for HTML parsing
- Implements exponential backoff for failed requests
- Handles various JACoW URL patterns and structures

License: MIT License
=============================================================================
"""

import asyncio
import re
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup, Tag
from utils.config import Config
from utils.helpers import extract_year_from_text, normalize_url, is_valid_url


class JACoWSpider:
    """JACoW 网站爬虫"""

    def __init__(
        self,
        delay: float = 1.0,
        year_filter: Optional[int] = None,
        conference_filter: Optional[str] = None,
        logger=None,
    ):
        self.config = Config()
        self.delay = delay
        self.year_filter = year_filter
        self.conference_filter = conference_filter
        self.logger = logger
        self.session: Optional[aiohttp.ClientSession] = None
        self.visited_urls: Set[str] = set()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.TIMEOUT),
            headers=self.config.get_headers(),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()

    async def crawl_papers(self) -> List[Dict[str, str]]:
        """
        爬取所有论文链接

        Returns:
            论文信息列表
        """
        papers = []

        async with self:
            # 获取主页面
            if self.logger:
                self.logger.info("开始爬取 JACoW 主页...")

            # 先爬取 proceedings 页面获取会议列表
            proceedings_url = f"{self.config.BASE_URL}/Main/Proceedings"
            proceedings_html = await self._fetch_page(proceedings_url)
            if not proceedings_html:
                if self.logger:
                    self.logger.error("无法获取 proceedings 页面")
                return papers

            # 解析会议链接
            conference_links = self._extract_conference_links_from_proceedings(
                proceedings_html
            )
            if self.logger:
                self.logger.info(f"找到 {len(conference_links)} 个会议")

            # 过滤会议
            if self.conference_filter:
                conference_links = [
                    link
                    for link in conference_links
                    if self.conference_filter.upper() in link["name"].upper()
                ]
                if self.logger:
                    self.logger.info(f"过滤后剩余 {len(conference_links)} 个会议")

            # 爬取每个会议的论文
            for conf_link in conference_links:
                if self.logger:
                    self.logger.info(f"正在爬取会议: {conf_link['name']}")

                conf_papers = await self._crawl_conference_papers(conf_link)
                papers.extend(conf_papers)

                if self.logger:
                    self.logger.info(
                        f"会议 {conf_link['name']} 找到 {len(conf_papers)} 篇论文"
                    )

                # 延迟请求
                await asyncio.sleep(self.delay)

        # 过滤年份
        if self.year_filter:
            papers = [p for p in papers if p.get("year") == self.year_filter]
            if self.logger:
                self.logger.info(f"年份过滤后剩余 {len(papers)} 篇论文")

        return papers

    async def _fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        """
        获取网页内容

        Args:
            url: 网页URL
            retries: 重试次数

        Returns:
            网页HTML内容
        """
        if not self.session:
            return None

        for attempt in range(retries):
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        if self.logger:
                            self.logger.warning(f"HTTP {response.status} for {url}")
            except Exception as e:
                if self.logger:
                    self.logger.warning(
                        f"请求失败 (尝试 {attempt + 1}/{retries}): {url} - {str(e)}"
                    )

                if attempt < retries - 1:
                    await asyncio.sleep(self.config.RETRY_DELAY * (attempt + 1))

        return None

    def _extract_conference_links_from_proceedings(
        self, html: str
    ) -> List[Dict[str, str]]:
        """
        从 proceedings 页面提取会议链接

        Args:
            html: proceedings 页面HTML内容

        Returns:
            会议链接列表
        """
        soup = BeautifulSoup(html, "html.parser")
        conference_links = []

        # JACoW 网站的实际结构：查找会议链接
        # 根据实际观察，会议链接通常在特定的格式中

        # 查找所有可能的会议链接
        # 格式1：直接链接到会议主页，如 jacow.org/ipac2023/
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            text = link.get_text(strip=True)

            # 检查是否是会议链接
            if href and any(
                conf.lower() in href.lower() for conf in self.config.KNOWN_CONFERENCES
            ):
                # 提取年份
                year = extract_year_from_text(href + " " + text)
                if year and year >= 2000:  # 只考虑2000年以后的会议
                    full_url = normalize_url(href, self.config.BASE_URL)
                    if full_url not in self.visited_urls:
                        conference_links.append(
                            {
                                "name": f"{self._extract_conference_name_from_url(href)} {year}",
                                "url": full_url,
                                "year": year,
                            }
                        )
                        self.visited_urls.add(full_url)

        # 格式2：查找 proceedings.jacow.org 域名的链接
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href and "proceedings.jacow.org" in href:
                text = link.get_text(strip=True)
                year = extract_year_from_text(href + " " + text)
                conf_name = self._extract_conference_name_from_url(href)

                if year and conf_name and href not in self.visited_urls:
                    conference_links.append(
                        {"name": f"{conf_name} {year}", "url": href, "year": year}
                    )
                    self.visited_urls.add(href)

        # 如果还是没找到，构建常见的会议URL
        if not conference_links:
            conference_links = self._generate_common_conference_urls()

        # 去重并排序
        unique_links = []
        seen_urls = set()
        for link in conference_links:
            if link["url"] not in seen_urls:
                unique_links.append(link)
                seen_urls.add(link["url"])

        # 按年份和会议名排序
        unique_links.sort(key=lambda x: (x.get("year", 0), x["name"]), reverse=True)

        return unique_links

    def _generate_common_conference_urls(self) -> List[Dict[str, str]]:
        """
        生成常见的会议URL（当自动发现失败时使用）

        Returns:
            会议链接列表
        """
        conference_links = []
        current_year = 2024

        # 生成最近几年的主要会议URL
        for year in range(current_year, current_year - 10, -1):  # 最近10年
            for conf in ["IPAC", "LINAC", "PAC"]:
                # JACoW的URL格式通常是 proceedings.jacow.org/confYEAR/
                conf_lower = conf.lower()
                url = f"https://proceedings.jacow.org/{conf_lower}{year}/"

                conference_links.append(
                    {"name": f"{conf} {year}", "url": url, "year": year}
                )

        return conference_links

    def _extract_conference_name_from_url(self, url: str) -> str:
        """
        从URL中提取会议名称

        Args:
            url: 会议URL

        Returns:
            会议名称
        """
        url_upper = url.upper()
        for conf in self.config.KNOWN_CONFERENCES:
            if conf in url_upper:
                return conf

        # 尝试从URL路径中提取
        # 例如：proceedings.jacow.org/ipac2023/ -> IPAC
        import re

        match = re.search(r"/([a-z]+)\d{4}/", url, re.I)
        if match:
            return match.group(1).upper()

        return "UNKNOWN"

    async def _crawl_conference_papers(
        self, conference_link: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        爬取单个会议的论文

        Args:
            conference_link: 会议链接信息

        Returns:
            论文列表
        """
        papers = []

        # 获取会议主页面
        html = await self._fetch_page(conference_link["url"])
        if not html:
            return papers

        soup = BeautifulSoup(html, "html.parser")

        # 提取会议信息
        conference_name = conference_link.get("name", "Unknown").split()[
            0
        ]  # 取第一个词作为会议名
        year = conference_link.get("year") or extract_year_from_text(
            conference_link["name"]
        )

        # JACoW 的实际结构：查找 session 链接
        session_links = []

        # 方法1：查找 session/index.html 链接
        session_index_url = conference_link["url"].rstrip("/") + "/session/index.html"
        session_html = await self._fetch_page(session_index_url)

        if session_html:
            session_soup = BeautifulSoup(session_html, "html.parser")
            # 查找所有session链接
            for link in session_soup.find_all("a", href=True):
                href = link.get("href")
                if href and "/session/" in href and href.endswith("/index.html"):
                    full_session_url = normalize_url(href, session_index_url)
                    session_links.append(full_session_url)

        # 方法2：如果没找到session链接，尝试直接在主页查找PDF链接
        if not session_links:
            paper_links = self._extract_direct_paper_links(soup, conference_link["url"])
            for paper_link in paper_links:
                paper_info = {
                    "title": paper_link.get("title", "Unknown Title"),
                    "download_url": paper_link["url"],
                    "conference": conference_name,
                    "year": year,
                    "source_page": conference_link["url"],
                    "authors": paper_link.get("authors", ""),
                    "abstract": paper_link.get("abstract", ""),
                    "keywords": paper_link.get("keywords", ""),
                    "file_extension": self._get_file_extension(paper_link["url"]),
                }
                papers.append(paper_info)
        else:
            # 爬取每个session的论文
            for session_url in session_links[:5]:  # 限制session数量以避免过多请求
                session_papers = await self._crawl_session_papers(
                    session_url, conference_name, year
                )
                papers.extend(session_papers)

                # 延迟请求
                await asyncio.sleep(self.delay)

        return papers

    async def _crawl_session_papers(
        self, session_url: str, conference_name: str, year: int
    ) -> List[Dict[str, str]]:
        """
        爬取单个session的论文

        Args:
            session_url: session页面URL
            conference_name: 会议名称
            year: 年份

        Returns:
            论文列表
        """
        papers = []

        html = await self._fetch_page(session_url)
        if not html:
            return papers

        soup = BeautifulSoup(html, "html.parser")

        # 查找论文链接 - JACoW的实际格式
        paper_links = self._extract_paper_links_from_session(soup, session_url)

        for paper_link in paper_links:
            paper_info = {
                "title": paper_link.get("title", "Unknown Title"),
                "download_url": paper_link["url"],
                "conference": conference_name,
                "year": year,
                "source_page": session_url,
                "authors": paper_link.get("authors", ""),
                "abstract": paper_link.get("abstract", ""),
                "keywords": paper_link.get("keywords", ""),
                "file_extension": self._get_file_extension(paper_link["url"]),
                "paper_id": paper_link.get("paper_id", ""),
            }
            papers.append(paper_info)

        return papers

    def _extract_paper_links_from_session(
        self, soup: BeautifulSoup, base_url: str
    ) -> List[Dict[str, str]]:
        """
        从session页面提取论文链接 - 基于JACoW的实际结构

        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL

        Returns:
            论文链接列表
        """
        paper_links = []

        # JACoW的实际格式：查找Paper链接
        # 格式通常是：Paper: [MOXD1](url.pdf)
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            text = link.get_text(strip=True)

            if href and href.endswith(".pdf"):
                full_url = normalize_url(href, base_url)

                # 提取论文ID（通常是链接文本）
                paper_id = text if text and len(text) < 20 else ""

                # 查找标题（通常在附近的文本中）
                title = self._extract_title_from_context(link)

                # 查找作者（通常在标题附近）
                authors = self._extract_authors_from_context(link)

                paper_links.append(
                    {
                        "url": full_url,
                        "title": title or paper_id or "Unknown Title",
                        "authors": authors,
                        "paper_id": paper_id,
                    }
                )

        return paper_links

    def _extract_direct_paper_links(
        self, soup: BeautifulSoup, base_url: str
    ) -> List[Dict[str, str]]:
        """
        直接从页面提取PDF链接

        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL

        Returns:
            论文链接列表
        """
        paper_links = []

        # 查找所有PDF链接
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href and href.endswith(".pdf") and "proceedings" in href:
                full_url = normalize_url(href, base_url)

                title = self._extract_title_from_context(link)
                authors = self._extract_authors_from_context(link)

                paper_links.append(
                    {
                        "url": full_url,
                        "title": title or "Unknown Title",
                        "authors": authors,
                    }
                )

        return paper_links

    def _extract_title_from_context(self, link: Tag) -> str:
        """
        从链接上下文中提取标题

        Args:
            link: 链接标签

        Returns:
            提取的标题
        """
        # 查找包含标题的父元素或兄弟元素
        parent = link.parent

        # 方法1：查找同一段落中的文本
        if parent:
            # 获取父元素的文本，排除链接本身
            parent_text = parent.get_text()
            link_text = link.get_text()
            title_text = parent_text.replace(link_text, "").strip()

            # 清理标题
            if title_text and len(title_text) > 10 and len(title_text) < 200:
                # 移除常见的前缀
                title_text = re.sub(r"^(Paper:|Slides:|DOI:)", "", title_text).strip()
                if title_text:
                    return title_text

        # 方法2：查找前面的文本节点
        for prev in link.previous_siblings:
            if hasattr(prev, "strip"):
                text = prev.strip()
                if text and len(text) > 10 and len(text) < 200:
                    return text

        return ""

    def _extract_authors_from_context(self, link: Tag) -> str:
        """
        从链接上下文中提取作者信息

        Args:
            link: 链接标签

        Returns:
            作者信息
        """
        # 查找包含作者的元素（通常有特定的样式或位置）
        parent = link.parent
        if parent:
            # 查找后续的文本节点，通常包含作者信息
            for next_elem in parent.next_siblings:
                if hasattr(next_elem, "get_text"):
                    text = next_elem.get_text(strip=True)
                    # 简单判断是否为作者信息
                    if text and "," in text and len(text) < 150:
                        # 排除一些明显不是作者的文本
                        if not any(
                            word in text.lower()
                            for word in [
                                "doi:",
                                "paper:",
                                "slides:",
                                "received:",
                                "about:",
                            ]
                        ):
                            return text

        return ""

    def _extract_paper_links(
        self, soup: BeautifulSoup, base_url: str
    ) -> List[Dict[str, str]]:
        """
        从会议页面提取论文链接

        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL

        Returns:
            论文链接列表
        """
        paper_links = []

        # PDF链接选择器
        pdf_selectors = [
            'a[href$=".pdf"]',
            'a[href*=".pdf"]',
            'a[href*="download"]',
            ".paper-link",
            ".download-link",
            ".pdf-link",
        ]

        for selector in pdf_selectors:
            links = soup.select(selector)
            for link in links:
                if isinstance(link, Tag):
                    href = link.get("href")
                    if href:
                        full_url = normalize_url(href, base_url)
                        if is_valid_url(full_url):
                            title = self._extract_paper_title(link)
                            authors = self._extract_authors(link)

                            paper_links.append(
                                {"url": full_url, "title": title, "authors": authors}
                            )

        # 如果没有找到PDF链接，查找其他文档类型
        if not paper_links:
            doc_patterns = [r"\.pdf$", r"\.doc$", r"\.docx$", r"\.ppt$", r"\.pptx$"]
            all_links = soup.find_all("a", href=True)

            for link in all_links:
                href = link.get("href")
                if href and any(
                    re.search(pattern, href, re.I) for pattern in doc_patterns
                ):
                    full_url = normalize_url(href, base_url)
                    if is_valid_url(full_url):
                        title = self._extract_paper_title(link)
                        authors = self._extract_authors(link)

                        paper_links.append(
                            {"url": full_url, "title": title, "authors": authors}
                        )

        return paper_links

    def _extract_paper_title(self, link: Tag) -> str:
        """从链接元素提取论文标题"""
        # 尝试从链接文本提取
        title = link.get_text(strip=True)

        # 如果链接文本是"PDF"或"Download"等，尝试从周围元素获取标题
        if title.lower() in ["pdf", "download", "paper", "full text"]:
            # 查找父元素或兄弟元素中的标题
            parent = link.parent
            if parent:
                # 查找标题标签
                title_elem = parent.find(["h1", "h2", "h3", "h4", "h5", "h6"])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                else:
                    # 使用父元素的文本，但排除链接本身
                    parent_text = parent.get_text(strip=True)
                    link_text = link.get_text(strip=True)
                    title = parent_text.replace(link_text, "").strip()

        # 清理标题
        title = re.sub(r"\s+", " ", title)
        title = title.strip(".,;:")

        return title if title else "Unknown Title"

    def _extract_authors(self, link: Tag) -> str:
        """从链接元素提取作者信息"""
        authors = ""

        # 查找作者信息的常见位置
        parent = link.parent
        if parent:
            # 查找class包含author的元素
            author_elem = parent.find(class_=re.compile(r"author", re.I))
            if author_elem:
                authors = author_elem.get_text(strip=True)
            else:
                # 查找紧跟在标题后的作者信息
                for sibling in parent.find_all(["p", "span", "div"]):
                    text = sibling.get_text(strip=True)
                    # 简单的作者检测逻辑
                    if (
                        ", " in text
                        and len(text) < 200
                        and not any(
                            word in text.lower()
                            for word in ["abstract", "download", "pdf"]
                        )
                    ):
                        authors = text
                        break

        return authors

    def _extract_conference_name(self, name: str) -> str:
        """从会议名称中提取标准化的会议名"""
        # 检查已知会议列表
        name_upper = name.upper()
        for conf in self.config.KNOWN_CONFERENCES:
            if conf in name_upper:
                return conf

        # 尝试从名称中提取
        # 查找常见的会议名称模式
        patterns = [
            r"\b(IPAC|LINAC|PAC|EPAC|DIPAC|BIW|SRF|IBIC|COOL|HB)\b",
            r"\b([A-Z]{3,6})\s*\d{2,4}\b",
            r"\b([A-Z][a-zA-Z]{2,10})\s*\d{2,4}\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, name, re.I)
            if match:
                return match.group(1).upper()

        # 如果都没有找到，使用第一个单词
        words = name.split()
        if words:
            return words[0].upper()

        return "UNKNOWN"

    def _get_file_extension(self, url: str) -> str:
        """从URL获取文件扩展名"""
        parsed = urlparse(url)
        path = parsed.path.lower()

        for ext in self.config.SUPPORTED_EXTENSIONS:
            if path.endswith(ext):
                return ext

        return ".pdf"  # 默认为PDF
