#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: main.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Main entry point for the JACoW academic conference paper 
             crawling and download tool. Supports both individual paper 
             downloads and complete conference proceedings with intelligent 
             classification and size control.

Development Log:
- Sept 9, 2025: Initial creation with full CLI interface
- Sept 9, 2025: Added individual paper mode support
- Sept 9, 2025: Integrated conference batch download capability
- Sept 9, 2025: Added comprehensive error handling and reporting
- Sept 9, 2025: Internationalized to English interface

Features:
- Smart crawling with automatic paper type detection
- Concurrent downloads with network-friendly settings
- Automatic paper classification and organization
- Resume capability for interrupted downloads
- Comprehensive logging and progress reporting
- Dry-run mode for safe preview before downloading

Usage:
    python main.py --individual-papers --conference IPAC --year 2023
    python main.py --dry-run --verbose
    python main.py --help

Dependencies:
    - Python 3.7+
    - aiohttp for async HTTP requests
    - aiofiles for async file operations
    - BeautifulSoup4 for HTML parsing

License: MIT License
=============================================================================
"""

import argparse
import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from crawler.spider import JACoWSpider
from crawler.downloader import PaperDownloader
from crawler.classifier import PaperClassifier
from utils.logger import setup_logger
from utils.config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="JACoW Paper Crawling and Download Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  python main.py                              # Default settings to crawl all papers
  python main.py --output-dir ./my_papers     # Specify output directory
  python main.py --max-size 50                # Limit file size to 50MB
  python main.py --concurrent 3               # Use 3 concurrent downloads
  python main.py --year 2023                  # Only download papers from 2023
  python main.py --conference IPAC            # Only download IPAC conference papers
        """
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='./data/papers',
        help='Paper download directory (default: ./data/papers)'
    )
    
    parser.add_argument(
        '--max-size', '-s',
        type=int,
        default=100,
        help='Maximum file size limit in MB (default: 100)'
    )
    
    parser.add_argument(
        '--concurrent', '-c',
        type=int,
        default=5,
        help='Number of concurrent downloads (default: 5)'
    )
    
    parser.add_argument(
        '--year', '-y',
        type=int,
        help='Specify year (e.g.: 2023)'
    )
    
    parser.add_argument(
        '--conference',
        type=str,
        help='Specify conference name (e.g.: IPAC, LINAC, PAC)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Request delay time in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume download from last interruption'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run mode, only show files to be downloaded without actual downloading'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output mode'
    )
    
    parser.add_argument(
        '--individual-papers',
        action='store_true',
        help='Download individual papers instead of complete conference proceedings'
    )
    
    parser.add_argument(
        '--max-papers',
        type=int,
        help='Maximum number of papers to download (only for individual papers mode)'
    )
    
    return parser.parse_args()


async def main():
    """Main function"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logger(
        name="jacow_crawler",
        log_file="data/logs/crawler.log",
        verbose=args.verbose
    )
    
    logger.info("=" * 60)
    logger.info("JACoW Paper Crawler Starting")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = Config()
        config.update_from_args(args)
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Output directory: {output_dir.absolute()}")
        logger.info(f"Maximum file size: {args.max_size}MB")
        logger.info(f"Concurrent downloads: {args.concurrent}")
        logger.info(f"Request delay: {args.delay} seconds")
        
        if args.year:
            logger.info(f"Specified year: {args.year}")
        if args.conference:
            logger.info(f"Specified conference: {args.conference}")
        if args.dry_run:
            logger.info("Dry run mode: Only showing list of files to download")
        
        # Initialize spider
        if args.individual_papers:
            from crawler.individual_spider import JACoWIndividualPaperSpider
            spider = JACoWIndividualPaperSpider(
                delay=args.delay,
                year_filter=args.year,
                conference_filter=args.conference,
                logger=logger
            )
            logger.info("Using individual paper spider mode")
        else:
            spider = JACoWSpider(
                delay=args.delay,
                year_filter=args.year,
                conference_filter=args.conference,
                logger=logger
            )
            logger.info("Using conference proceedings spider mode")
        
        # Initialize downloader
        downloader = PaperDownloader(
            output_dir=output_dir,
            max_size_mb=args.max_size,
            concurrent_downloads=args.concurrent,
            logger=logger
        )
        
        # Initialize classifier
        classifier = PaperClassifier(
            base_dir=output_dir,
            logger=logger
        )
        
        # Start crawling paper links
        logger.info("Starting to crawl paper links...")
        if args.individual_papers:
            paper_links = await spider.crawl_individual_papers(
                year=args.year,
                conference=args.conference,
                max_papers=args.max_papers
            )
        else:
            paper_links = await spider.crawl_papers()
        
        if not paper_links:
            logger.warning("No paper links found")
            return
        
        logger.info(f"Found {len(paper_links)} papers")
        
        # Dry run mode
        if args.dry_run:
            logger.info("Dry run mode - Paper list:")
            for i, paper in enumerate(paper_links[:20], 1):  # Only show first 20
                logger.info(f"{i:3d}. {paper['title']}")
                logger.info(f"     Conference: {paper['conference']} ({paper['year']})")
                logger.info(f"     Link: {paper['download_url']}")
                logger.info("")
            
            if len(paper_links) > 20:
                logger.info(f"... {len(paper_links) - 20} more papers")
            
            logger.info("Dry run complete")
            return
        
        # Start downloading papers
        logger.info("Starting to download papers...")
        download_results = await downloader.download_papers(
            paper_links, 
            resume=args.resume
        )
        
        # Classify and organize papers
        logger.info("Starting to classify and organize papers...")
        classification_results = classifier.classify_papers(download_results)
        
        # Generate download report
        await generate_report(
            download_results, 
            classification_results, 
            output_dir, 
            logger
        )
        
        logger.info("=" * 60)
        logger.info("JACoW Paper Crawling Complete!")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Program execution error: {str(e)}", exc_info=True)
        return 1
    
    return 0


async def generate_report(download_results, classification_results, output_dir, logger):
    """Generate download report"""
    try:
        from datetime import datetime
        import json
        
        report_dir = Path("data/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"download_report_{timestamp}.json"
        
        # Statistics
        total_papers = len(download_results)
        successful_downloads = len([r for r in download_results if r.get('success', False)])
        failed_downloads = total_papers - successful_downloads
        total_size_mb = sum(r.get('size_mb', 0) for r in download_results if r.get('success', False))
        
        report_data = {
            "timestamp": timestamp,
            "summary": {
                "total_papers": total_papers,
                "successful_downloads": successful_downloads,
                "failed_downloads": failed_downloads,
                "total_size_mb": round(total_size_mb, 2),
                "output_directory": str(output_dir.absolute())
            },
            "classification": classification_results,
            "download_details": download_results
        }
        
        # Save JSON report
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # Generate simple text report
        txt_report_file = report_dir / f"download_summary_{timestamp}.txt"
        with open(txt_report_file, 'w', encoding='utf-8') as f:
            f.write("JACoW Paper Download Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Download time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total papers: {total_papers}\n")
            f.write(f"Successful downloads: {successful_downloads}\n")
            f.write(f"Failed downloads: {failed_downloads}\n")
            f.write(f"Total size: {total_size_mb:.2f} MB\n")
            f.write(f"Output directory: {output_dir.absolute()}\n\n")
            
            if classification_results:
                f.write("Classification statistics:\n")
                f.write("-" * 30 + "\n")
                for category, count in classification_results.items():
                    f.write(f"{category}: {count} papers\n")
        
        logger.info(f"Download report generated: {report_file}")
        logger.info(f"Summary report generated: {txt_report_file}")
        logger.info(f"Successfully downloaded {successful_downloads}/{total_papers} papers, total size {total_size_mb:.2f} MB")
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    try:
        # Set event loop policy on Windows
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        sys.exit(1)
