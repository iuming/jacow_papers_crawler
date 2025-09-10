# Python 版本更新说明

## 背景

由于 GitHub Actions 在 Ubuntu 24.04 上不再支持 Python 3.7，以及现代依赖包（如 pandas 2.x）需要更高版本，我们将项目的最低 Python 版本要求从 3.7 更新到 3.9。

## 更改内容

### 1. CI/CD 配置更新 (`.github/workflows/ci.yml`)
- 移除了 Python 3.7 和 3.8 的测试
- 现在测试 Python 3.9, 3.10, 3.11, 3.12
- 更新了矩阵配置以避免不支持的组合
- 添加了 Python 兼容性测试步骤

### 2. 项目文档更新
更新了所有文档中的 Python 版本要求：
- `README.md` - 徽章和系统要求
- `PROJECT_INFO.md` - 技术规格
- `CONTRIBUTING.md` - 开发环境要求
- `CHANGELOG.md` - 版本历史记录
- `docs/installation.md` - 安装指南
- `index.md` - 主页文档

### 3. 代码文件更新
- `setup.py` - 版本检查函数和注释
- `main.py` - 文档字符串中的系统要求
- `scripts/run.bat` 和 `scripts/run.sh` - 错误信息

### 4. 依赖项优化 (`requirements.txt`)
- 移除了 `asyncio==3.4.3`，因为 Python 3.8+ 内置了更新的 asyncio

### 5. 新增测试文件
- `tests/test_python_compatibility.py` - 验证 Python 3.8+ 特性支持

## Python 3.8+ 的优势

### 新特性支持
1. **海象操作符 (`:=`)** - 在表达式中赋值
2. **仅位置参数** - 更好的 API 设计
3. **改进的 asyncio** - 更稳定的异步编程
4. **更好的性能** - 优化的字典和列表操作

### 示例代码
```python
# 海象操作符
if (n := len(data)) > 10:
    print(f"数据很大: {n} 项")

# 仅位置参数
def process_data(data, /, *, format="json"):
    return format_data(data, format=format)
```

## 兼容性说明

### 支持的 Python 版本
- Python 3.8.x ✅
- Python 3.9.x ✅ 
- Python 3.10.x ✅
- Python 3.11.x ✅
- Python 3.12.x ✅

### 已测试的操作系统
- Ubuntu 20.04/22.04/24.04 ✅
- Windows 10/11 ✅
- macOS 11+ ✅

## 迁移指南

### 对于用户
如果您目前使用 Python 3.7，请升级到 Python 3.8 或更高版本：

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.8

# macOS (使用 Homebrew)
brew install python@3.8

# Windows
# 从 python.org 下载并安装 Python 3.8+
```

### 对于开发者
1. 更新您的开发环境到 Python 3.8+
2. 运行兼容性测试：
   ```bash
   python tests/test_python_compatibility.py
   ```
3. 验证所有功能正常工作

## 测试验证

运行以下命令验证更新：

```bash
# 检查 Python 版本
python --version

# 运行兼容性测试
python tests/test_python_compatibility.py

# 运行完整测试套件
python -m pytest tests/ -v
```

## 问题解决

### 常见问题

**Q: 我必须升级 Python 版本吗？**
A: 是的，为了获得最佳的兼容性和性能，建议使用 Python 3.8+。

**Q: Python 3.7 的代码还能工作吗？**
A: 大部分代码可以工作，但一些新特性和优化需要 Python 3.8+。

**Q: 如何检查我的 Python 版本？**
A: 运行 `python --version` 或 `python -c "import sys; print(sys.version)"`

### 获取帮助

如果您在升级过程中遇到问题，请：
1. 查看 [安装指南](docs/installation.md)
2. 运行 `python tests/test_python_compatibility.py` 检查兼容性
3. 在 GitHub Issues 中报告问题

---

**更新日期**: 2025年9月10日  
**影响**: CI/CD 管道，开发环境要求  
**紧急程度**: 中等 - 建议在下次部署时更新
