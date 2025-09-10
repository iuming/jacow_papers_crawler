#!/usr/bin/env python3
"""
诊断脚本 - 用于调试模块导入问题
"""

import sys
import os
from pathlib import Path


def diagnose_python_path():
    """诊断 Python 路径设置"""
    print("🔍 Python 路径诊断")
    print("=" * 50)

    print(f"Python 版本: {sys.version}")
    print(f"Python 可执行文件: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")

    print("\nPython 路径 (sys.path):")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")

    # 检查项目结构
    print(f"\n项目根目录: {Path(__file__).parent.parent}")
    project_root = Path(__file__).parent.parent

    print("\n项目结构:")
    for item in sorted(project_root.iterdir()):
        if item.is_dir():
            print(f"  📁 {item.name}/")
            if item.name in ["crawler", "utils"]:
                for subitem in sorted(item.iterdir()):
                    if subitem.suffix == ".py":
                        print(f"    📄 {subitem.name}")
        elif item.suffix == ".py":
            print(f"  📄 {item.name}")


def test_imports():
    """测试模块导入"""
    print("\n🧪 模块导入测试")
    print("=" * 50)

    # 添加项目根目录到路径
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ 已添加项目根目录到 Python 路径: {project_root}")

    modules = [
        "crawler",
        "crawler.spider",
        "crawler.downloader",
        "crawler.classifier",
        "utils",
        "utils.config",
        "utils.logger",
        "utils.helpers",
    ]

    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
        except Exception as e:
            print(f"⚠️  {module}: {type(e).__name__}: {e}")


def check_file_existence():
    """检查文件存在性"""
    print("\n📁 文件存在性检查")
    print("=" * 50)

    project_root = Path(__file__).parent.parent

    files_to_check = [
        "crawler/__init__.py",
        "crawler/spider.py",
        "crawler/downloader.py",
        "crawler/classifier.py",
        "utils/__init__.py",
        "utils/config.py",
        "utils/logger.py",
        "utils/helpers.py",
        "main.py",
        "config.ini",
    ]

    for file_path in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (不存在)")


def main():
    """主函数"""
    print("🩺 JACoW 项目诊断工具")
    print("=" * 50)

    diagnose_python_path()
    check_file_existence()
    test_imports()

    print("\n📋 诊断完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
