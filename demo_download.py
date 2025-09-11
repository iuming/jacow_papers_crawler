#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Demo Script: JACoW Paper Download Example
File: demo_download.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 11, 2025
Description: Demonstration script showing how to use the JACoW crawler
             to download conference papers with various configurations.

Usage:
    python demo_download.py
    python demo_download.py --demo-type quick
    python demo_download.py --demo-type preview
    python demo_download.py --demo-type conference
=============================================================================
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import setup_logger


def demo_quick_download():
    """Demo: Quick download of a few recent papers"""
    print("\n" + "="*60)
    print("🚀 DEMO 1: Quick Download - Recent Papers")
    print("="*60)
    print("This demo downloads the 5 most recent papers for preview.")
    print("Perfect for testing the crawler functionality.")
    print("\nCommand being executed:")
    cmd = [
        "python", "main.py",
        "--individual-papers",
        "--max-papers", "5",
        "--max-size", "50",
        "--verbose",
        "--output-dir", "./demo_data/quick_download"
    ]
    print(" ".join(cmd))
    return cmd


def demo_preview_mode():
    """Demo: Preview mode - see what would be downloaded"""
    print("\n" + "="*60)
    print("👀 DEMO 2: Preview Mode - Dry Run")
    print("="*60)
    print("This demo shows what papers would be downloaded without")
    print("actually downloading them. Great for exploring available content.")
    print("\nCommand being executed:")
    cmd = [
        "python", "main.py",
        "--individual-papers",
        "--conference", "IPAC",
        "--year", "2023",
        "--max-papers", "20",
        "--dry-run",
        "--verbose"
    ]
    print(" ".join(cmd))
    return cmd


def demo_conference_download():
    """Demo: Download papers from a specific conference"""
    print("\n" + "="*60)
    print("🎯 DEMO 3: Conference Specific Download")
    print("="*60)
    print("This demo downloads papers from a specific conference and year.")
    print("It demonstrates filtering capabilities.")
    print("\nCommand being executed:")
    cmd = [
        "python", "main.py",
        "--individual-papers",
        "--conference", "LINAC",
        "--year", "2022",
        "--max-papers", "10",
        "--max-size", "100",
        "--verbose",
        "--output-dir", "./demo_data/linac_2022"
    ]
    print(" ".join(cmd))
    return cmd


def demo_comprehensive_download():
    """Demo: Comprehensive download with all options"""
    print("\n" + "="*60)
    print("🔧 DEMO 4: Comprehensive Download")
    print("="*60)
    print("This demo showcases all available options and features.")
    print("Includes classification, resume capability, and detailed reporting.")
    print("\nCommand being executed:")
    cmd = [
        "python", "main.py",
        "--individual-papers",
        "--max-papers", "15",
        "--max-size", "75",
        "--concurrent", "3",
        "--delay", "1.5",
        "--resume",
        "--verbose",
        "--output-dir", "./demo_data/comprehensive"
    ]
    print(" ".join(cmd))
    return cmd


async def run_demo(demo_func):
    """Run a specific demo function"""
    try:
        # Setup logger for demo
        logger = setup_logger("demo", verbose=True)
        
        # Get command from demo function
        cmd = demo_func()
        
        print(f"\nPress Enter to execute the command, or Ctrl+C to skip...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nSkipping this demo...\n")
            return
        
        # Create output directory if specified
        if "--output-dir" in cmd:
            output_dir_idx = cmd.index("--output-dir") + 1
            if output_dir_idx < len(cmd):
                output_dir = Path(cmd[output_dir_idx])
                output_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created output directory: {output_dir}")
        
        # Import main function and run
        from main import main
        
        # Temporarily modify sys.argv
        original_argv = sys.argv.copy()
        sys.argv = cmd
        
        try:
            result = await main()
            if result == 0:
                print("✅ Demo completed successfully!")
            else:
                print("❌ Demo finished with errors.")
        finally:
            # Restore original argv
            sys.argv = original_argv
            
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"❌ Demo failed: {str(e)}")


def main():
    """Main demo runner"""
    parser = argparse.ArgumentParser(
        description="JACoW Paper Crawler Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Demo Types:
  quick       - Download 5 recent papers for testing
  preview     - Dry run to preview available papers
  conference  - Download from specific conference
  comprehensive - Full feature demonstration
  all         - Run all demos sequentially
        """
    )
    
    parser.add_argument(
        "--demo-type",
        choices=["quick", "preview", "conference", "comprehensive", "all"],
        default="all",
        help="Type of demo to run (default: all)"
    )
    
    args = parser.parse_args()
    
    print("🎉 Welcome to JACoW Paper Crawler Demo!")
    print("This script demonstrates different ways to use the crawler.")
    print("=" * 60)
    
    # Demo functions mapping
    demos = {
        "quick": demo_quick_download,
        "preview": demo_preview_mode,
        "conference": demo_conference_download,
        "comprehensive": demo_comprehensive_download
    }
    
    async def run_demos():
        try:
            if args.demo_type == "all":
                print("Running all demos sequentially...\n")
                for demo_name, demo_func in demos.items():
                    print(f"\n{'='*20} {demo_name.upper()} DEMO {'='*20}")
                    await run_demo(demo_func)
                    print(f"\nDemo '{demo_name}' finished. Press Enter to continue...")
                    try:
                        input()
                    except KeyboardInterrupt:
                        print("\nDemo sequence interrupted.")
                        break
            else:
                demo_func = demos[args.demo_type]
                await run_demo(demo_func)
            
            print("\n" + "="*60)
            print("🎉 Demo session completed!")
            print("📁 Check the ./demo_data/ directory for downloaded files.")
            print("📄 Check ./data/logs/ for detailed logs.")
            print("📖 Read docs/GitHub_Action_Download_Guide.md for automation setup.")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user. Goodbye! 👋")
    
    # Set event loop policy on Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(run_demos())


if __name__ == "__main__":
    main()
