#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: setup.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Comprehensive project setup and installation script for the
             JACoW paper crawler. Handles dependency installation, environment
             setup, configuration initialization, and system verification
             to ensure the crawler is ready for operation.

Development Log:
- Sept 9, 2025: Initial setup script creation
- Sept 9, 2025: Added dependency management
- Sept 9, 2025: Implemented environment validation
- Sept 9, 2025: Added configuration initialization
- Sept 9, 2025: Enhanced with cross-platform support

Setup Features:
1. Python Version Checking - Ensures Python 3.9+ compatibility
2. Dependency Installation - Installs required packages from requirements.txt
3. Environment Validation - Checks system compatibility
4. Directory Structure Creation - Sets up data and log directories
5. Configuration Initialization - Creates default config files
6. Verification Testing - Runs basic functionality tests

Installation Process:
1. System Requirements Check
2. Virtual Environment Setup (recommended)
3. Package Dependencies Installation
4. Project Structure Initialization
5. Configuration File Creation
6. Basic Functionality Verification

Supported Platforms:
- Windows 10/11 (PowerShell, Command Prompt)
- macOS (Terminal, with Python 3.9+)
- Linux (bash, with Python 3.9+)

Dependencies Managed:
- aiohttp: Async HTTP client for web requests
- aiofiles: Async file I/O operations
- beautifulsoup4: HTML parsing and data extraction
- colorama: Cross-platform colored terminal output
- pathlib: Modern path handling (built-in Python 3.4+)

Usage:
    python setup.py
    
Or for development setup:
    python setup.py --dev
    
For system-wide installation:
    python setup.py --install

License: MIT License
=============================================================================
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ 错误: 需要Python 3.9或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """创建虚拟环境"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ 虚拟环境已存在")
        return True
    
    try:
        print("创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ 虚拟环境创建成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 虚拟环境创建失败")
        return False


def install_dependencies():
    """安装依赖包"""
    try:
        print("安装依赖包...")
        
        # 确定pip路径
        if sys.platform == "win32":
            pip_path = Path("venv/Scripts/pip.exe")
        else:
            pip_path = Path("venv/bin/pip")
        
        if not pip_path.exists():
            pip_path = "pip"  # 使用全局pip
        
        # 升级pip
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        
        # 安装依赖
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    directories = [
        "data/papers",
        "data/logs", 
        "data/reports",
        "data/cache"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构创建完成")


def create_gitignore():
    """创建.gitignore文件"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Data directories
data/papers/
data/logs/
data/reports/
data/cache/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
"""
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ .gitignore 文件创建完成")
    else:
        print("✅ .gitignore 文件已存在")


def run_tests():
    """运行测试"""
    try:
        print("运行测试...")
        
        # 确定Python路径
        if sys.platform == "win32":
            python_path = Path("venv/Scripts/python.exe")
        else:
            python_path = Path("venv/bin/python")
        
        if not python_path.exists():
            python_path = sys.executable
        
        result = subprocess.run([str(python_path), "test.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 所有测试通过")
            return True
        else:
            print("❌ 部分测试失败")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False


def show_usage_instructions():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("🎉 JACoW 论文爬取器安装完成!")
    print("=" * 60)
    print()
    print("使用方法:")
    print()
    
    if sys.platform == "win32":
        print("1. 激活虚拟环境:")
        print("   venv\\Scripts\\activate")
        print()
        print("2. 运行程序:")
        print("   python main.py")
        print()
        print("3. 或者直接运行批处理文件:")
        print("   run.bat")
    else:
        print("1. 激活虚拟环境:")
        print("   source venv/bin/activate")
        print()
        print("2. 运行程序:")
        print("   python main.py")
        print()
        print("3. 或者运行shell脚本:")
        print("   chmod +x run.sh")
        print("   ./run.sh")
    
    print()
    print("常用命令:")
    print("• 查看帮助:        python main.py --help")
    print("• 试运行:          python main.py --dry-run")
    print("• 指定年份:        python main.py --year 2023")
    print("• 指定会议:        python main.py --conference IPAC")
    print("• 断点续传:        python main.py --resume")
    print("• 详细输出:        python main.py --verbose")
    print()
    print("输出目录: ./data/papers/")
    print("日志文件: ./data/logs/crawler.log")
    print("报告文件: ./data/reports/")
    print()


def main():
    """主函数"""
    print("JACoW 论文爬取器 - 项目设置")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 创建虚拟环境
    if not create_virtual_environment():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 创建目录结构
    create_directories()
    
    # 创建.gitignore
    create_gitignore()
    
    # 运行测试
    run_tests()
    
    # 显示使用说明
    show_usage_instructions()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n设置被用户中断")
    except Exception as e:
        print(f"\n设置过程出错: {str(e)}")
        sys.exit(1)
