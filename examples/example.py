#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: example.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Comprehensive example script demonstrating the usage of various
             components in the JACoW paper crawler system. Provides hands-on
             examples for crawling, downloading, and classifying academic
             papers from JACoW conferences.

Development Log:
- Sept 9, 2025: Initial example suite creation
- Sept 9, 2025: Added crawling-only demonstration
- Sept 9, 2025: Implemented download sample examples
- Sept 9, 2025: Added paper classification demonstrations
- Sept 9, 2025: Enhanced with interactive menu system

Examples Included:
1. Paper Link Crawling - Demonstrates basic spider functionality
2. Sample Downloads - Shows download manager capabilities
3. Paper Classification - Illustrates automatic categorization
4. Complete Workflow - End-to-end process demonstration

Features Demonstrated:
- Spider configuration and paper discovery
- Download manager with concurrent downloads
- Paper classification and organization
- Error handling and logging
- Progress monitoring and reporting

Educational Value:
- Clear code structure for learning
- Extensive comments explaining each step
- Safe test examples that won't overload servers
- Interactive prompts for user engagement

Usage:
    python examples/example.py
    
Then follow the interactive menu to explore different features.

Dependencies:
- All crawler modules (spider, downloader, classifier)
- Logging utilities
- asyncio for async operations

License: MIT License
=============================================================================
"""

import asyncio
import sys
from pathlib import Path

# Add project root directory to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from crawler.spider import JACoWSpider
from crawler.downloader import PaperDownloader
from crawler.classifier import PaperClassifier
from utils.logger import setup_colored_logger


async def example_crawl_only():
    """Example: Only crawl paper links (no download)"""
    print("=" * 60)
    print("Example 1: Only crawl paper links")
    print("=" * 60)
    
    logger = setup_colored_logger("example", verbose=True)
    
    # Create spider instance
    spider = JACoWSpider(
        delay=0.5,  # Faster request interval (for testing only)
        year_filter=2023,  # Only crawl papers from 2023
        logger=logger
    )
    
    # Crawl paper links
    papers = await spider.crawl_papers()
    
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers[:5], 1):  # Only show first 5
        print(f"{i}. {paper['title']}")
        print(f"   Conference: {paper['conference']} ({paper['year']})")
        print(f"   Link: {paper['download_url']}")
        print()
    
    if len(papers) > 5:
        print(f"... {len(papers) - 5} more papers")


async def example_download_sample():
    """Example: Download a few paper samples"""
    print("=" * 60)
    print("Example 2: Download paper samples")
    print("=" * 60)
    
    logger = setup_colored_logger("example", verbose=True)
    
    # Create test paper list
    sample_papers = [
        {
            'title': 'Test Paper 1',
            'download_url': 'https://www.jacow.org/sample1.pdf',
            'conference': 'IPAC',
            'year': 2023,
            'authors': 'Author A, Author B',
            'file_extension': '.pdf'
        },
        {
            'title': 'Test Paper 2',
            'download_url': 'https://www.jacow.org/sample2.pdf',
            'conference': 'LINAC',
            'year': 2023,
            'authors': 'Author C, Author D',
            'file_extension': '.pdf'
        }
    ]
    
    # Create downloader instance
    output_dir = Path("./data/example_downloads")
    downloader = PaperDownloader(
        output_dir=output_dir,
        max_size_mb=10,  # Limit to smaller file size
        concurrent_downloads=2,
        logger=logger
    )
    
    # Download papers (this may fail as URLs are examples)
    results = await downloader.download_papers(sample_papers)
    
    print("\nDownload results:")
    for result in results:
        status = "Success" if result['success'] else f"Failed: {result['error']}"
        print(f"- {result['title']}: {status}")


def example_classification():
    """Example: Paper classification"""
    print("=" * 60)
    print("Example 3: Paper classification")
    print("=" * 60)
    
    logger = setup_colored_logger("example", verbose=True)
    
    # Create test download results
    download_results = [
        {
            'title': 'RF Cavity Design for Linear Accelerators',
            'conference': 'LINAC',
            'year': 2023,
            'success': True,
            'file_path': './data/example/LINAC_2023_RF_Cavity.pdf',
            'abstract': 'This paper describes RF cavity design methods for linear accelerators'
        },
        {
            'title': 'Beam Position Monitor Development',
            'conference': 'IBIC',
            'year': 2023,
            'success': True,
            'file_path': './data/example/IBIC_2023_BPM.pdf',
            'abstract': 'Development of high precision beam position monitors'
        },
        {
            'title': 'Superconducting Magnet Technology',
            'conference': 'IPAC',
            'year': 2022,
            'success': True,
            'file_path': './data/example/IPAC_2022_SC_Magnet.pdf',
            'abstract': 'Advances in superconducting magnet technology for particle accelerators'
        }
    ]
    
    # Create classifier instance
    classifier = PaperClassifier(
        base_dir=Path("./data/example_classification"),
        logger=logger
    )
    
    # Classify papers
    classification_stats = classifier.classify_papers(download_results)
    
    print("\nClassification statistics:")
    for category, count in classification_stats.items():
        print(f"- {category}: {count} papers")
    
    # Generate classification report
    report = classifier.generate_classification_report()
    print("\nClassification report:")
    print(report)


async def run_examples():
    """Run all examples"""
    print("JACoW Crawler Example Program")
    print("=" * 60)
    
    choice = input("""
Please select the example to run:
1. Only crawl paper links
2. Download paper samples
3. Paper classification demo
4. Run all examples
Please enter your choice (1-4): """).strip()
    
    if choice == '1':
        await example_crawl_only()
    elif choice == '2':
        await example_download_sample()
    elif choice == '3':
        example_classification()
    elif choice == '4':
        await example_crawl_only()
        print("\n" + "=" * 60 + "\n")
        await example_download_sample()
        print("\n" + "=" * 60 + "\n")
        example_classification()
    else:
        print("Invalid choice, running all examples...")
        await example_crawl_only()
        print("\n" + "=" * 60 + "\n")
        await example_download_sample()
        print("\n" + "=" * 60 + "\n")
        example_classification()


if __name__ == "__main__":
    try:
        # Set event loop policy on Windows
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        asyncio.run(run_examples())
    except KeyboardInterrupt:
        print("\nExample program interrupted by user")
    except Exception as e:
        print(f"\nExample program execution error: {str(e)}")
        import traceback
        traceback.print_exc()
