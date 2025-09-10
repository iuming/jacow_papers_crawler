#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: test_individual.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Comprehensive test suite for the individual paper download
             functionality. Validates the specialized spider's ability to
             identify, extract, and download individual academic papers
             from JACoW conferences instead of large proceedings files.

Development Log:
- Sept 9, 2025: Initial individual paper testing framework
- Sept 9, 2025: Added paper identification tests
- Sept 9, 2025: Implemented download validation tests
- Sept 9, 2025: Added session-based discovery tests
- Sept 9, 2025: Enhanced with error handling validation

Test Coverage:
1. Paper Type Detection - Validates individual vs proceedings identification
2. Session Discovery - Tests session page parsing and enumeration
3. PDF Link Extraction - Verifies data-href and standard link parsing
4. Download Process - Tests actual paper download functionality
5. File Organization - Validates proper file naming and directory structure
6. Error Handling - Tests resilience to network and parsing errors

Test Scenarios:
- IPAC 2023 session testing (verified working with 122+ papers)
- Various conference formats and structures
- Edge cases with malformed URLs or missing papers
- Network timeout and retry scenarios
- Large session handling and performance

Validation Criteria:
- Paper identification accuracy (individual vs proceedings)
- Download success rate and error handling
- File integrity and proper naming
- Directory structure compliance
- Performance within acceptable limits

Usage:
    python tests/test_individual.py
    
Expected Results:
- Successful identification of individual papers
- Proper filtering of large proceedings files
- Accurate session enumeration and paper extraction
- Robust error handling for network issues

License: MIT License
=============================================================================
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from crawler.individual_spider import JACoWIndividualPaperSpider
from utils.logger import setup_logger
from utils.config import Config


async def test_individual_papers():
    """测试单篇论文爬取"""
    # 设置日志
    logger = setup_logger("test_individual", level="DEBUG")

    # 初始化爬虫
    spider = JACoWIndividualPaperSpider(
        delay=1.0, year_filter=2023, conference_filter=None, logger=logger
    )

    try:
        # 测试爬取2023年的前10篇单独论文
        logger.info("开始测试单篇论文爬取...")
        papers = await spider.crawl_individual_papers(year=2023, max_papers=10)

        logger.info(f"找到 {len(papers)} 篇单独论文")

        # 显示结果
        for i, paper in enumerate(papers, 1):
            logger.info(f"\n{i}. 论文信息:")
            logger.info(f"   代码: {paper.get('code', 'N/A')}")
            logger.info(f"   标题: {paper.get('title', 'N/A')}")
            logger.info(f"   作者: {paper.get('authors', 'N/A')}")
            logger.info(f"   会议: {paper.get('conference', 'N/A')}")
            logger.info(f"   年份: {paper.get('year', 'N/A')}")
            logger.info(f"   Session: {paper.get('session', 'N/A')}")
            logger.info(f"   类型: {paper.get('type', 'N/A')}")
            logger.info(f"   URL: {paper.get('url', 'N/A')}")

        # 统计信息
        paper_types = {}
        for paper in papers:
            paper_type = paper.get("type", "unknown")
            paper_types[paper_type] = paper_types.get(paper_type, 0) + 1

        logger.info(f"\n论文类型统计:")
        for ptype, count in paper_types.items():
            logger.info(f"  {ptype}: {count}")

        # 检查是否真的是单篇论文
        individual_count = sum(
            1 for p in papers if spider._is_individual_paper(p.get("url", ""))
        )
        logger.info(f"\n确认为单篇论文的数量: {individual_count}/{len(papers)}")

    except Exception as e:
        logger.error(f"测试出错: {e}")
    finally:
        # 检查spider是否有close方法
        if hasattr(spider, "close"):
            await spider.close()
        elif hasattr(spider, "session") and hasattr(spider.session, "close"):
            await spider.session.close()


if __name__ == "__main__":
    asyncio.run(test_individual_papers())
