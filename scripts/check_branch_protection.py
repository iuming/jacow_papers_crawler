#!/usr/bin/env python3
"""
分支保护状态检查脚本
检查当前仓库的分支保护设置
"""

import json
import subprocess
import sys
from typing import Dict, Any


def run_command(cmd: str) -> Dict[str, Any]:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}
    except FileNotFoundError:
        return {"success": False, "error": "Command not found"}


def check_gh_cli():
    """检查 GitHub CLI 是否可用"""
    result = run_command("gh --version")
    return result["success"]


def check_branch_protection():
    """检查分支保护设置"""
    print("🔍 检查分支保护设置...")

    if not check_gh_cli():
        print("❌ GitHub CLI 未安装或未配置")
        print("   请安装 GitHub CLI: https://cli.github.com/")
        return False

    # 检查当前仓库
    repo_result = run_command("gh repo view --json owner,name")
    if not repo_result["success"]:
        print("❌ 无法获取仓库信息")
        print(f"   错误: {repo_result['error']}")
        return False

    try:
        repo_info = json.loads(repo_result["output"])
        repo_name = f"{repo_info['owner']['login']}/{repo_info['name']}"
        print(f"📁 仓库: {repo_name}")
    except (json.JSONDecodeError, KeyError):
        print("❌ 无法解析仓库信息")
        return False

    # 检查主分支保护
    protection_result = run_command(
        f"gh api repos/{repo_name}/branches/main/protection"
    )

    if not protection_result["success"]:
        if "Branch not protected" in protection_result["error"]:
            print("⚠️  主分支未受保护")
            print_protection_recommendations()
            return False
        else:
            print(f"❌ 检查保护设置时出错: {protection_result['error']}")
            return False

    # 解析保护设置
    try:
        protection = json.loads(protection_result["output"])
        print("✅ 主分支已受保护")
        print_protection_details(protection)
        return True
    except json.JSONDecodeError:
        print("❌ 无法解析保护设置")
        return False


def print_protection_details(protection: Dict[str, Any]):
    """打印保护设置详情"""
    print("\n📋 当前保护设置:")

    # 状态检查
    if "required_status_checks" in protection:
        status_checks = protection["required_status_checks"]
        print(f"   ✅ 必需状态检查: {'启用' if status_checks else '禁用'}")
        if status_checks and "contexts" in status_checks:
            contexts = status_checks["contexts"]
            if contexts:
                print(f"      📝 检查项目: {', '.join(contexts)}")
            print(
                f"      🔄 要求分支最新: {'是' if status_checks.get('strict', False) else '否'}"
            )

    # PR 审查
    if "required_pull_request_reviews" in protection:
        pr_reviews = protection["required_pull_request_reviews"]
        if pr_reviews:
            print("   ✅ PR 审查: 启用")
            required_reviewers = pr_reviews.get("required_approving_review_count", 0)
            print(f"      👥 必需审查者数量: {required_reviewers}")
            dismiss_stale = pr_reviews.get("dismiss_stale_reviews", False)
            print(f"      🔄 自动取消过时审查: {'是' if dismiss_stale else '否'}")
        else:
            print("   ⚠️  PR 审查: 禁用")

    # 管理员强制
    enforce_admins = protection.get("enforce_admins", {}).get("enabled", False)
    print(f"   👨‍💼 管理员强制遵循规则: {'是' if enforce_admins else '否'}")

    # 限制
    if "restrictions" in protection:
        restrictions = protection["restrictions"]
        if restrictions:
            print("   🚫 推送限制: 启用")
        else:
            print("   🚫 推送限制: 禁用")


def print_protection_recommendations():
    """打印保护设置建议"""
    print("\n💡 建议的分支保护设置:")
    print("   1. 启用必需状态检查")
    print("      - JACoW Crawler CI/CD")
    print("      - 要求分支为最新")
    print("   2. 启用 PR 审查")
    print("      - 至少 1 个审查者（个人项目）")
    print("      - 自动取消过时审查")
    print("   3. 启用管理员强制")
    print("   4. 禁用强制推送和删除")
    print("\n🔧 设置方法:")
    print("   方法 1: GitHub Web 界面")
    print("      https://github.com/iuming/jacow_papers_crawler/settings/branches")
    print("   方法 2: 参考 BRANCH_PROTECTION_GUIDE.md")


def check_ci_status():
    """检查最近的 CI 状态"""
    print("\n🔄 检查最近的 CI 状态...")

    result = run_command("gh run list --limit 5 --json status,conclusion,workflowName")
    if not result["success"]:
        print("❌ 无法获取 CI 状态")
        return False

    try:
        runs = json.loads(result["output"])
        if not runs:
            print("   📝 没有找到 CI 运行记录")
            return True

        print("   📊 最近 5 次运行:")
        for run in runs:
            status = run.get("status", "unknown")
            conclusion = run.get("conclusion", "unknown")
            workflow = run.get("workflowName", "unknown")

            if status == "completed":
                if conclusion == "success":
                    status_icon = "✅"
                elif conclusion == "failure":
                    status_icon = "❌"
                else:
                    status_icon = "⚠️"
            else:
                status_icon = "🔄"

            print(f"      {status_icon} {workflow}: {status} ({conclusion})")

        return True
    except json.JSONDecodeError:
        print("❌ 无法解析 CI 状态")
        return False


def main():
    """主函数"""
    print("🛡️  JACoW 项目分支保护检查")
    print("=" * 50)

    # 检查分支保护
    protection_ok = check_branch_protection()

    # 检查 CI 状态
    ci_ok = check_ci_status()

    print("\n" + "=" * 50)
    if protection_ok:
        print("🎉 分支保护设置正常")
    else:
        print("⚠️  建议设置分支保护")

    if ci_ok:
        print("🎉 CI 状态检查完成")

    print("\n📚 相关文档:")
    print("   - BRANCH_PROTECTION_GUIDE.md")
    print("   - .github/CODEOWNERS")
    print("   - .github/pull_request_template.md")

    return 0 if protection_ok and ci_ok else 1


if __name__ == "__main__":
    sys.exit(main())
