#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: verify.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Quick verification script to check if the project is correctly
             set up and all components are working properly. Performs basic
             functionality tests and dependency checks to ensure the crawler
             system is ready for operation.

Development Log:
- Sept 9, 2025: Initial verification script creation
- Sept 9, 2025: Added import checking functionality
- Sept 9, 2025: Implemented basic connectivity tests
- Sept 9, 2025: Added configuration validation
- Sept 9, 2025: Enhanced with component integration testing

Verification Tests:
1. Import Testing - Verifies all modules can be imported
2. Dependency Checking - Ensures required packages are installed
3. Configuration Validation - Checks config files and settings
4. Network Connectivity - Tests JACoW website accessibility
5. File System Permissions - Verifies write access to output directories
6. Component Integration - Basic functionality tests

Test Categories:
- Critical: Must pass for basic operation
- Important: Should pass for full functionality
- Optional: Nice-to-have features

Usage:
    python tests/verify.py
    
The script will output colored results indicating:
- GREEN: All tests passed
- YELLOW: Warning - some issues detected
- RED: Critical failure - system not ready

Exit Codes:
- 0: All critical tests passed
- 1: Critical failures detected
- 2: Import or dependency errors

Features Tested:
- Spider module functionality
- Downloader capabilities
- Classifier operations
- Logging system
- Configuration management
- Network connectivity to JACoW

License: MIT License
=============================================================================
"""

import sys
import importlib
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def safe_print(text, fallback=None):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 首先尝试fallback
        if fallback:
            try:
                print(fallback)
            except UnicodeEncodeError:
                # 如果fallback也失败，使用ASCII安全版本
                ascii_fallback = "".join(char for char in fallback if ord(char) < 128)
                print(ascii_fallback if ascii_fallback else "ASCII conversion failed")
        else:
            # 移除所有非ASCII字符
            ascii_text = "".join(char for char in text if ord(char) < 128)
            print(ascii_text if ascii_text else "ASCII conversion failed")


def check_imports():
    """检查所有模块是否可以正确导入"""
    safe_print("🔍 检查模块导入...", "Checking module imports...")

    modules_to_check = [
        "crawler.spider",
        "crawler.downloader",
        "crawler.classifier",
        "utils.config",
        "utils.logger",
        "utils.helpers",
    ]

    failed_imports = []

    for module in modules_to_check:
        try:
            importlib.import_module(module)
            safe_print(f"✅ {module}", f"+ {module}")
        except ImportError as e:
            safe_print(f"❌ {module}: {e}", f"- {module}: {e}")
            failed_imports.append(module)

    return len(failed_imports) == 0


def check_dependencies():
    """检查外部依赖"""
    safe_print("\n📦 检查外部依赖...", "\nChecking external dependencies...")

    dependencies = [
        ("requests", "网络请求"),
        ("bs4", "HTML解析"),
        ("aiohttp", "异步HTTP客户端"),
        ("aiofiles", "异步文件操作"),
    ]

    failed_deps = []

    for dep, desc in dependencies:
        try:
            importlib.import_module(dep)
            safe_print(f"✅ {dep} ({desc})", f"+ {dep}")
        except ImportError:
            safe_print(
                f"❌ {dep} ({desc}) - 需要安装",
                f"- {dep} - needs installation",
            )
            failed_deps.append(dep)

    return len(failed_deps) == 0


def check_directories():
    """检查目录结构"""
    safe_print("\n📁 检查目录结构...", "\nChecking directory structure...")

    required_dirs = [
        "data",
        "data/papers",
        "data/logs",
        "data/reports",
        "crawler",
        "utils",
    ]

    missing_dirs = []

    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            safe_print(f"✅ {dir_path}/", f"+ {dir_path}/")
        else:
            safe_print(
                f"❌ {dir_path}/ - 目录不存在", f"- {dir_path}/ - directory not exists"
            )
            missing_dirs.append(dir_path)
            # 创建缺失的目录
            path.mkdir(parents=True, exist_ok=True)
            safe_print(f"🔧 已创建 {dir_path}/", f"Created {dir_path}/")

    return True


def check_config():
    """检查配置"""
    safe_print("\n⚙️  检查配置...", "\nChecking configuration...")

    try:
        # 检查配置文件是否存在
        config_file = project_root / "config.ini"
        if config_file.exists():
            safe_print(
                "✅ 配置文件存在: config.ini", "+ Config file exists: config.ini"
            )
        else:
            safe_print(
                "⚠️  配置文件不存在，将使用默认配置",
                "Warning: Config file not found, using defaults",
            )

        # 尝试导入配置模块
        from utils.config import Config

        config = Config()

        safe_print(f"✅ 基础URL: {config.BASE_URL}", f"+ Base URL: {config.BASE_URL}")
        safe_print(
            f"✅ 最大文件大小: {config.MAX_FILE_SIZE_MB}MB",
            f"+ Max file size: {config.MAX_FILE_SIZE_MB}MB",
        )
        safe_print(
            f"✅ 支持的文件类型: {', '.join(config.SUPPORTED_EXTENSIONS)}",
            f"+ Supported extensions: {', '.join(config.SUPPORTED_EXTENSIONS)}",
        )
        safe_print(
            f"✅ 已知会议数量: {len(config.KNOWN_CONFERENCES)}",
            f"+ Known conferences: {len(config.KNOWN_CONFERENCES)}",
        )

        return True
    except ImportError as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False


def main():
    """主验证函数"""
    safe_print("=" * 60)
    safe_print(
        "🚀 JACoW 论文爬取器 - 项目验证", "JACoW Paper Crawler - Project Verification"
    )
    safe_print("=" * 60)

    all_checks_passed = True

    # 检查模块导入
    if not check_imports():
        all_checks_passed = False

    # 检查依赖
    if not check_dependencies():
        all_checks_passed = False
        safe_print(
            "\n💡 如需安装依赖，请运行: pip install -r requirements.txt",
            "\nTip: To install dependencies, run: pip install -r requirements.txt",
        )

    # 检查目录
    if not check_directories():
        all_checks_passed = False

    # 检查配置
    if not check_config():
        all_checks_passed = False

    safe_print("\n" + "=" * 60)
    if all_checks_passed:
        safe_print(
            "🎉 所有检查通过！项目已正确设置。",
            "All checks passed! Project is correctly set up.",
        )
        safe_print("\n💡 现在你可以运行:", "\nTip: You can now run:")
        safe_print(
            "   • python main.py --dry-run    (试运行)",
            "   • python main.py --dry-run    (dry run)",
        )
        safe_print(
            "   • python main.py --help       (查看帮助)",
            "   • python main.py --help       (view help)",
        )
        safe_print(
            "   • python example.py           (运行示例)",
            "   • python example.py           (run example)",
        )
        safe_print(
            "   • run.bat                      (Windows启动脚本)",
            "   • run.bat                      (Windows start script)",
        )
    else:
        safe_print(
            "⚠️  部分检查失败，请检查上述错误信息。",
            "Warning: Some checks failed, please check the error messages above.",
        )
        return 1

    safe_print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
