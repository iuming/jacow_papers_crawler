#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JACoW 爬虫实际测试脚本
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from crawler.spider import JACoWSpider
from utils.logger import setup_colored_logger


async def test_jacow_spider():
    """测试JACoW爬虫的实际功能"""
    print("=" * 60)
    print("🧪 JACoW 爬虫实际测试")
    print("=" * 60)
    
    logger = setup_colored_logger("test_spider", verbose=True)
    
    # 创建爬虫实例（只测试IPAC 2023）
    spider = JACoWSpider(
        delay=2.0,  # 较长的延迟以免给服务器造成压力
        year_filter=2023,
        conference_filter='IPAC',
        logger=logger
    )
    
    try:
        logger.info("开始测试爬取 IPAC 2023...")
        
        # 爬取论文链接
        papers = await spider.crawl_papers()
        
        logger.info(f"测试完成！找到 {len(papers)} 篇论文")
        
        if papers:
            logger.info("前5篇论文示例:")
            for i, paper in enumerate(papers[:5], 1):
                logger.info(f"{i}. 标题: {paper['title'][:80]}...")
                logger.info(f"   会议: {paper['conference']} ({paper['year']})")
                logger.info(f"   下载链接: {paper['download_url']}")
                logger.info(f"   作者: {paper.get('authors', 'Unknown')[:50]}...")
                logger.info("")
            
            if len(papers) > 5:
                logger.info(f"... 还有 {len(papers) - 5} 篇论文")
        else:
            logger.warning("没有找到论文，可能需要调整爬虫策略")
        
        return len(papers) > 0
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_single_conference_page():
    """测试单个会议页面的爬取"""
    print("\n" + "=" * 60)
    print("🔍 测试单个会议页面")
    print("=" * 60)
    
    logger = setup_colored_logger("test_single", verbose=True)
    
    spider = JACoWSpider(delay=1.0, logger=logger)
    
    # 测试IPAC 2023的具体URL
    test_conference = {
        'name': 'IPAC 2023',
        'url': 'https://proceedings.jacow.org/ipac2023/',
        'year': 2023
    }
    
    try:
        logger.info(f"测试爬取: {test_conference['name']}")
        
        papers = await spider._crawl_conference_papers(test_conference)
        
        logger.info(f"结果: 找到 {len(papers)} 篇论文")
        
        if papers:
            # 显示找到的论文类型
            pdf_count = len([p for p in papers if p['download_url'].endswith('.pdf')])
            logger.info(f"其中 PDF 文件: {pdf_count} 个")
            
            # 显示示例
            for i, paper in enumerate(papers[:3], 1):
                logger.info(f"{i}. {paper['title'][:60]}...")
                logger.info(f"   URL: {paper['download_url']}")
        
        return len(papers) > 0
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        return False


async def test_network_connectivity():
    """测试网络连接性"""
    print("\n" + "=" * 60)
    print("🌐 测试网络连接")
    print("=" * 60)
    
    logger = setup_colored_logger("test_network", verbose=True)
    
    spider = JACoWSpider(delay=0.5, logger=logger)
    
    test_urls = [
        "https://www.jacow.org/",
        "https://www.jacow.org/Main/Proceedings",
        "https://proceedings.jacow.org/ipac2023/",
        "https://proceedings.jacow.org/ipac2023/session/index.html"
    ]
    
    results = []
    
    async with spider:
        for url in test_urls:
            logger.info(f"测试连接: {url}")
            try:
                html = await spider._fetch_page(url)
                if html and len(html) > 100:
                    logger.info(f"✅ 成功 - 获取到 {len(html)} 字符的内容")
                    results.append(True)
                else:
                    logger.warning(f"⚠️  响应内容过短或为空")
                    results.append(False)
            except Exception as e:
                logger.error(f"❌ 失败: {str(e)}")
                results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    logger.info(f"网络连接测试完成: {success_rate:.1f}% 成功率")
    
    return success_rate > 50


async def main():
    """主测试函数"""
    print("🚀 JACoW 爬虫实际功能测试")
    print("这将测试爬虫是否能正确爬取 JACoW 网站")
    print()
    
    # 测试1: 网络连接
    network_ok = await test_network_connectivity()
    
    if not network_ok:
        print("\n❌ 网络连接测试失败，请检查网络连接或网站可访问性")
        return False
    
    # 测试2: 单个会议页面
    single_ok = await test_single_conference_page()
    
    # 测试3: 完整爬取流程
    full_ok = await test_jacow_spider()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    print(f"网络连接: {'✅ 通过' if network_ok else '❌ 失败'}")
    print(f"单页爬取: {'✅ 通过' if single_ok else '❌ 失败'}")
    print(f"完整流程: {'✅ 通过' if full_ok else '❌ 失败'}")
    
    if network_ok and (single_ok or full_ok):
        print("\n🎉 爬虫基本功能正常！")
        print("\n💡 使用建议:")
        print("• 使用 --dry-run 参数先预览要下载的内容")
        print("• 设置适当的延迟时间（建议1-2秒）")
        print("• 从小范围开始测试（如单个会议或年份）")
        return True
    else:
        print("\n⚠️  爬虫可能需要调整")
        print("\n🔧 可能的问题:")
        print("• 网站结构发生变化")
        print("• 网络连接问题")
        print("• 需要调整爬虫策略")
        return False


if __name__ == "__main__":
    try:
        # 在Windows上设置事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中出现异常: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
