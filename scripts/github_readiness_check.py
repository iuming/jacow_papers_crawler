#!/usr/bin/env python3
"""
Pre-GitHub Upload Checker

This script performs comprehensive checks to ensure the project is ready for GitHub upload.

Author: Ming Liu
Email: mliu@ihep.ac.cn
Institution: Institute of High Energy Physics (IHEP), Chinese Academy of Sciences
Date: September 9, 2025
Version: 1.0.0
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message: str, status: str = "INFO") -> None:
    """Print formatted status message."""
    colors = {
        "PASS": Colors.GREEN,
        "FAIL": Colors.RED,
        "WARN": Colors.YELLOW,
        "INFO": Colors.BLUE
    }
    color = colors.get(status, Colors.BLUE)
    print(f"{color}[{status}]{Colors.ENDC} {message}")

def check_file_exists(filepath: str, required: bool = True) -> bool:
    """Check if file exists."""
    exists = Path(filepath).exists()
    status = "PASS" if exists else ("FAIL" if required else "WARN")
    print_status(f"File {filepath}: {'Found' if exists else 'Missing'}", status)
    return exists

def check_directory_structure() -> bool:
    """Check if project has proper directory structure."""
    print_status("Checking directory structure...", "INFO")
    
    required_dirs = [
        "crawler",
        "utils",
        "docs",
        "tests",
        "scripts",
        "examples",
        ".github",
        ".github/workflows",
        ".github/ISSUE_TEMPLATE"
    ]
    
    optional_dirs = [
        "data",
        "data/papers",
        "data/logs"
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        exists = Path(dir_path).exists()
        if not exists:
            print_status(f"Required directory {dir_path}: Missing", "FAIL")
            all_good = False
        else:
            print_status(f"Required directory {dir_path}: Found", "PASS")
    
    for dir_path in optional_dirs:
        exists = Path(dir_path).exists()
        print_status(f"Optional directory {dir_path}: {'Found' if exists else 'Missing'}", "PASS" if exists else "INFO")
    
    return all_good

def check_essential_files() -> bool:
    """Check if all essential files exist."""
    print_status("Checking essential files...", "INFO")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "setup.py",
        "README.md",
        "LICENSE",
        "config.ini",
        ".gitignore",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md"
    ]
    
    optional_files = [
        "Dockerfile",
        "docker-compose.yml",
        "_config.yml",
        "index.md"
    ]
    
    all_good = True
    
    for filepath in required_files:
        if not check_file_exists(filepath, required=True):
            all_good = False
    
    for filepath in optional_files:
        check_file_exists(filepath, required=False)
    
    return all_good

def check_github_files() -> bool:
    """Check GitHub-specific files."""
    print_status("Checking GitHub files...", "INFO")
    
    github_files = [
        ".github/workflows/ci.yml",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/pull_request_template.md"
    ]
    
    all_good = True
    for filepath in github_files:
        if not check_file_exists(filepath, required=True):
            all_good = False
    
    return all_good

def check_code_headers() -> bool:
    """Check if Python files have proper headers."""
    print_status("Checking code headers...", "INFO")
    
    python_files = [
        "main.py",
        "setup.py",
        "crawler/spider.py",
        "crawler/downloader.py",
        "crawler/classifier.py",
        "crawler/individual_spider.py",
        "utils/config.py",
        "utils/logger.py",
        "utils/helpers.py"
    ]
    
    required_header_elements = [
        "Author: Ming Liu",
        "mliu@ihep.ac.cn",
        "September 9, 2025"
    ]
    
    all_good = True
    
    for filepath in python_files:
        if not Path(filepath).exists():
            print_status(f"File {filepath}: Missing", "FAIL")
            all_good = False
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_header = all(element in content for element in required_header_elements)
        if has_header:
            print_status(f"Header in {filepath}: Complete", "PASS")
        else:
            print_status(f"Header in {filepath}: Missing elements", "FAIL")
            all_good = False
    
    return all_good

def check_documentation() -> bool:
    """Check documentation completeness."""
    print_status("Checking documentation...", "INFO")
    
    doc_files = [
        "docs/installation.md",
        "docs/usage.md",
        "docs/configuration.md"
    ]
    
    all_good = True
    for filepath in doc_files:
        if not check_file_exists(filepath, required=True):
            all_good = False
    
    # Check README.md content
    if Path("README.md").exists():
        with open("README.md", 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        required_sections = [
            "# JACoW Invincible Paper Crawler",
            "✨ Features",
            "Installation",
            "Usage",
            "Contributing"
        ]
        
        for section in required_sections:
            if section in readme_content:
                print_status(f"README section '{section}': Found", "PASS")
            else:
                print_status(f"README section '{section}': Missing", "FAIL")
                all_good = False
    
    return all_good

def check_dependencies() -> bool:
    """Check if dependencies are properly defined."""
    print_status("Checking dependencies...", "INFO")
    
    all_good = True
    
    # Check requirements.txt
    if Path("requirements.txt").exists():
        with open("requirements.txt", 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        required_packages = [
            "aiohttp",
            "aiofiles", 
            "beautifulsoup4",
            "rich"
        ]
        
        for package in required_packages:
            if package in requirements:
                print_status(f"Package {package}: Found in requirements.txt", "PASS")
            else:
                print_status(f"Package {package}: Missing from requirements.txt", "FAIL")
                all_good = False
    else:
        print_status("requirements.txt: Missing", "FAIL")
        all_good = False
    
    # Check setup.py
    if Path("setup.py").exists():
        with open("setup.py", 'r', encoding='utf-8') as f:
            setup_content = f.read()
        
        if "install_requires" in setup_content:
            print_status("setup.py install_requires: Found", "PASS")
        else:
            print_status("setup.py install_requires: Missing", "WARN")
    
    return all_good

def check_no_sensitive_data() -> bool:
    """Check for sensitive data that shouldn't be in the repository."""
    print_status("Checking for sensitive data...", "INFO")
    
    sensitive_patterns = [
        r'password\s*=\s*["\'].*["\']',
        r'api_key\s*=\s*["\'].*["\']',
        r'secret\s*=\s*["\'].*["\']',
        r'token\s*=\s*["\'].*["\']'
    ]
    
    files_to_check = []
    for ext in ['*.py', '*.ini', '*.json', '*.yml', '*.yaml']:
        files_to_check.extend(Path('.').rglob(ext))
    
    issues_found = False
    
    for filepath in files_to_check:
        if '.git' in str(filepath):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    print_status(f"Potential sensitive data in {filepath}", "WARN")
                    issues_found = True
        except Exception:
            continue
    
    if not issues_found:
        print_status("No sensitive data found", "PASS")
    
    return not issues_found

def check_git_configuration() -> bool:
    """Check Git configuration."""
    print_status("Checking Git configuration...", "INFO")
    
    all_good = True
    
    # Check if .gitignore exists and has proper content
    if Path(".gitignore").exists():
        with open(".gitignore", 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        required_ignores = [
            "__pycache__",
            "*.pyc",
            ".env",
            "data/",
            "logs/"
        ]
        
        for ignore in required_ignores:
            if ignore in gitignore_content:
                print_status(f".gitignore includes {ignore}: Yes", "PASS")
            else:
                print_status(f".gitignore includes {ignore}: No", "WARN")
    else:
        print_status(".gitignore: Missing", "FAIL")
        all_good = False
    
    return all_good

def check_version_consistency() -> bool:
    """Check version consistency across files."""
    print_status("Checking version consistency...", "INFO")
    
    version_files = {
        "setup.py": r'version\s*=\s*["\']([^"\']+)["\']',
        "CHANGELOG.md": r'## \[([^\]]+)\]',
        "main.py": r'Version:\s*([^\n]+)'
    }
    
    versions = {}
    
    for filepath, pattern in version_files.items():
        if Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(pattern, content)
            if match:
                versions[filepath] = match.group(1).strip()
            else:
                print_status(f"Version not found in {filepath}", "WARN")
    
    if len(set(versions.values())) <= 1:
        print_status("Version consistency: Good", "PASS")
        return True
    else:
        print_status("Version consistency: Issues found", "WARN")
        for filepath, version in versions.items():
            print_status(f"  {filepath}: {version}", "INFO")
        return False

def run_syntax_check() -> bool:
    """Run Python syntax check on all Python files."""
    print_status("Running syntax checks...", "INFO")
    
    python_files = list(Path('.').rglob('*.py'))
    all_good = True
    
    for filepath in python_files:
        if '.git' in str(filepath) or 'venv' in str(filepath):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                compile(f.read(), str(filepath), 'exec')
            print_status(f"Syntax check {filepath}: OK", "PASS")
        except SyntaxError as e:
            print_status(f"Syntax error in {filepath}: {e}", "FAIL")
            all_good = False
        except Exception as e:
            print_status(f"Error checking {filepath}: {e}", "WARN")
    
    return all_good

def generate_report() -> Dict:
    """Generate comprehensive pre-upload report."""
    print_status("=" * 60, "INFO")
    print_status("JACoW Invincible Paper Crawler - GitHub Upload Readiness Check", "INFO")
    print_status("=" * 60, "INFO")
    
    checks = {
        "Directory Structure": check_directory_structure(),
        "Essential Files": check_essential_files(),
        "GitHub Files": check_github_files(),
        "Code Headers": check_code_headers(),
        "Documentation": check_documentation(),
        "Dependencies": check_dependencies(),
        "Sensitive Data": check_no_sensitive_data(),
        "Git Configuration": check_git_configuration(),
        "Version Consistency": check_version_consistency(),
        "Syntax Check": run_syntax_check()
    }
    
    print_status("=" * 60, "INFO")
    print_status("SUMMARY", "INFO")
    print_status("=" * 60, "INFO")
    
    passed = 0
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "PASS" if result else "FAIL"
        print_status(f"{check_name}: {status}", status)
        if result:
            passed += 1
    
    print_status(f"\nOverall: {passed}/{total} checks passed", "INFO")
    
    if passed == total:
        print_status("🎉 Project is ready for GitHub upload!", "PASS")
        return {"ready": True, "checks": checks}
    else:
        print_status("❌ Please fix the failing checks before uploading", "FAIL")
        return {"ready": False, "checks": checks}

def main():
    """Main function."""
    if not Path('.').is_dir():
        print_status("Please run this script from the project root directory", "FAIL")
        sys.exit(1)
    
    report = generate_report()
    
    # Save report to file
    with open("github_readiness_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print_status(f"\nDetailed report saved to: github_readiness_report.json", "INFO")
    
    if not report["ready"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
