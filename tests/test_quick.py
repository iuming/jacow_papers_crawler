#!/usr/bin/env python3
"""
快速测试脚本 - 验证核心功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """测试基本导入"""
    print("🧪 基本导入测试...")
    
    try:
        import crawler
        print("✅ crawler 包导入成功")
    except Exception as e:
        print(f"❌ crawler 包导入失败: {e}")
        assert False, f"crawler包导入失败: {e}"
    
    try:
        import utils
        print("✅ utils 包导入成功")
    except Exception as e:
        print(f"❌ utils 包导入失败: {e}")
        assert False, f"utils包导入失败: {e}"

def test_module_imports():
    """测试模块导入"""
    print("\n🔬 模块导入测试...")
    
    modules = [
        ('crawler.spider', 'JACoWSpider'),
        ('utils.logger', 'setup_logger'),
        ('utils.config', 'Config')
    ]
    
    success_count = 0
    for module_name, class_or_function in modules:
        try:
            module = __import__(module_name, fromlist=[class_or_function])
            getattr(module, class_or_function)
            print(f"✅ {module_name}.{class_or_function}")
            success_count += 1
        except Exception as e:
            print(f"❌ {module_name}.{class_or_function}: {e}")
    
    assert success_count == len(modules), f"只有 {success_count}/{len(modules)} 个模块导入成功"

def test_basic_functionality():
    """测试基本功能"""
    print("\n⚡ 基本功能测试...")
    
    try:
        # 测试日志系统
        from utils.logger import setup_logger
        logger = setup_logger("test_logger")
        logger.info("测试日志系统")
        print("✅ 日志系统工作正常")
    except Exception as e:
        print(f"❌ 日志系统测试失败: {e}")
        assert False, f"日志系统测试失败: {e}"
    
    try:
        # 测试配置系统
        from utils.config import Config
        config = Config()
        assert hasattr(config, 'BASE_URL')
        print("✅ 配置系统工作正常")
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        assert False, f"配置系统测试失败: {e}"

def main():
    """主函数"""
    print("🚀 JACoW 快速测试")
    print("=" * 40)
    
    tests = [
        ("基本导入", test_basic_imports),
        ("模块导入", test_module_imports), 
        ("基本功能", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 出错: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
