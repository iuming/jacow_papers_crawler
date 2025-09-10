#!/usr/bin/env python3
"""
快速设置分支保护的脚本
"""

import subprocess
import sys
import json
from typing import Dict, Any


def run_command(cmd: str) -> Dict[str, Any]:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd.split(), 
            capture_output=True, 
            text=True, 
            check=True
        )
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}
    except FileNotFoundError:
        return {"success": False, "error": "Command not found"}


def check_gh_cli():
    """检查 GitHub CLI 是否可用"""
    result = run_command("gh --version")
    if not result["success"]:
        print("❌ GitHub CLI 未安装")
        print("请先安装 GitHub CLI:")
        print("  Windows: winget install --id GitHub.cli")
        print("  macOS: brew install gh")
        print("  Linux: https://github.com/cli/cli#installation")
        return False
    
    # 检查是否已认证
    auth_result = run_command("gh auth status")
    if not auth_result["success"]:
        print("❌ GitHub CLI 未认证")
        print("请运行: gh auth login")
        return False
    
    return True


def setup_branch_protection():
    """设置分支保护"""
    print("🛡️  设置主分支保护...")
    
    # 分支保护配置
    protection_config = {
        "required_status_checks": {
            "strict": True,
            "contexts": [
                "JACoW Crawler CI/CD / test",
                "JACoW Crawler CI/CD / security-scan",
                "JACoW Crawler CI/CD / build-docs"
            ]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
    # 获取仓库信息
    repo_result = run_command("gh repo view --json owner,name")
    if not repo_result["success"]:
        print(f"❌ 无法获取仓库信息: {repo_result['error']}")
        return False
    
    try:
        repo_info = json.loads(repo_result["output"])
        repo_name = f"{repo_info['owner']['login']}/{repo_info['name']}"
        print(f"📁 仓库: {repo_name}")
    except (json.JSONDecodeError, KeyError):
        print("❌ 无法解析仓库信息")
        return False
    
    # 应用保护设置
    config_json = json.dumps(protection_config)
    
    # 使用 gh api 设置分支保护
    cmd = f"gh api repos/{repo_name}/branches/main/protection --method PUT --input -"
    
    try:
        process = subprocess.Popen(
            cmd.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=config_json)
        
        if process.returncode == 0:
            print("✅ 分支保护设置成功!")
            return True
        else:
            print(f"❌ 设置失败: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 设置过程出错: {e}")
        return False


def main():
    """主函数"""
    print("🚀 JACoW 项目分支保护快速设置")
    print("=" * 50)
    
    # 检查前置条件
    if not check_gh_cli():
        return 1
    
    # 显示即将应用的设置
    print("\n📋 即将应用的分支保护设置:")
    print("   ✅ 必需状态检查 (CI/CD)")
    print("   ✅ 要求 PR 审查 (1 个审查者)")
    print("   ✅ 要求代码所有者审查")
    print("   ✅ 自动取消过时审查")
    print("   ✅ 管理员强制遵循")
    print("   ✅ 禁止强制推送")
    print("   ✅ 禁止删除分支")
    
    # 确认
    print("\n⚠️  注意: 设置后所有更改都需要通过 Pull Request")
    confirm = input("是否继续? (y/N): ").lower().strip()
    
    if confirm not in ['y', 'yes']:
        print("❌ 用户取消操作")
        return 0
    
    # 执行设置
    if setup_branch_protection():
        print("\n🎉 分支保护设置完成!")
        print("\n📚 后续步骤:")
        print("   1. 创建功能分支进行开发")
        print("   2. 通过 Pull Request 提交更改")
        print("   3. 等待 CI 检查通过")
        print("   4. 进行代码审查")
        print("   5. 合并到主分支")
        print("\n📖 详细指南: BRANCH_PROTECTION_GUIDE.md")
        return 0
    else:
        print("\n❌ 设置失败")
        print("\n🔧 手动设置:")
        print("   访问: https://github.com/iuming/jacow_papers_crawler/settings/branches")
        print("   参考: BRANCH_PROTECTION_GUIDE.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
