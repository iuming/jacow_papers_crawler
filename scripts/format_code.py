#!/usr/bin/env python3
"""
自动代码格式化脚本
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """运行命令并处理结果"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 完成")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} 失败")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ {description} 出错: {e}")
        return False


def main():
    """主函数"""
    print("🎨 JACoW 爬虫代码格式化工具")
    print("=" * 50)
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    
    # 切换到项目目录
    import os
    os.chdir(project_root)
    
    # 安装格式化工具（如果需要）
    print("📦 检查并安装格式化工具...")
    subprocess.run([sys.executable, "-m", "pip", "install", "black", "isort", "flake8"], 
                  capture_output=True)
    
    # 运行格式化工具
    steps = [
        ("python -m isort .", "导入排序 (isort)"),
        ("python -m black .", "代码格式化 (black)"),
        ("python -m flake8 . --statistics", "代码检查 (flake8)"),
    ]
    
    success_count = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1
    
    print(f"\n📊 完成情况: {success_count}/{len(steps)} 项成功")
    
    if success_count == len(steps):
        print("🎉 所有格式化步骤都已完成！")
        print("\n📝 建议运行以下命令验证:")
        print("   python -m black --check .")
        print("   python -m flake8 .")
    else:
        print("⚠️  部分步骤失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
