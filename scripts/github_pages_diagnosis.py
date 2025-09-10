#!/usr/bin/env python3
"""
GitHub Pages部署诊断脚本
检查GitHub Pages设置和工作流状态
"""


def check_github_pages_setup():
    """检查GitHub Pages设置"""
    print("📋 GitHub Pages设置检查清单:")
    print()
    print("1. 📂 仓库设置:")
    print("   - 访问: https://github.com/iuming/jacow_papers_crawler/settings/pages")
    print("   - 确保 Source 设置为: 'GitHub Actions'")
    print()
    print("2. 🔄 工作流检查:")
    print("   - 访问: https://github.com/iuming/jacow_papers_crawler/actions")
    print("   - 查看 'Deploy Documentation' 工作流状态")
    print("   - 如果失败，查看错误日志")
    print()
    print("3. 🚀 手动触发部署:")
    print("   - 在 Actions 页面点击 'Deploy Documentation'")
    print("   - 点击 'Run workflow' → 'Run workflow'")
    print()
    print("4. 📝 提交当前修复:")
    print("   - git add .")
    print("   - git commit -m 'Fix MkDocs configuration and add docs'")
    print("   - git push origin main")
    print()
    print("5. ⏱️ 等待部署:")
    print("   - GitHub Pages通常需要2-10分钟部署")
    print("   - 在Actions页面监控部署进度")
    print()
    print("6. 🌐 访问网站:")
    print("   - https://iuming.github.io/jacow_papers_crawler/")
    print()


def check_local_build():
    """检查本地构建"""
    import os
    import subprocess

    print("🔧 本地构建检查:")
    print()

    if os.path.exists("site"):
        print("✅ site/ 目录存在")
        if os.path.exists("site/index.html"):
            print("✅ index.html 已生成")
        else:
            print("❌ index.html 不存在")
    else:
        print("❌ site/ 目录不存在")
        print("   运行: python -m mkdocs build")

    print()
    print("📊 文件统计:")
    if os.path.exists("site"):
        files = []
        for root, dirs, filenames in os.walk("site"):
            files.extend(filenames)
        print(f"   生成文件数: {len(files)}")
        html_files = [f for f in files if f.endswith(".html")]
        print(f"   HTML文件数: {len(html_files)}")
    else:
        print("   无法统计（site目录不存在）")


if __name__ == "__main__":
    print("🔍 JACoW Papers Crawler - GitHub Pages诊断")
    print("=" * 50)
    print()

    check_local_build()
    print()
    check_github_pages_setup()
