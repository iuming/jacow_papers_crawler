# JACoW 论文自动下载 GitHub Action 使用指南

## 概述

这个GitHub Action可以自动下载JACoW会议的论文到 `data/papers` 目录中。支持手动触发和定时任务两种模式。

## 功能特点

- 🤖 **自动化下载**: 无需手动干预，自动爬取和下载论文
- 📅 **定时任务**: 每周日自动运行，获取最新论文
- 🎯 **灵活过滤**: 支持按会议、年份、论文数量等条件过滤
- 💾 **智能存储**: 自动分类存储下载的论文
- 📊 **详细报告**: 生成下载统计和错误报告
- 🔄 **断点续传**: 支持从中断处继续下载
- 🛡️ **安全机制**: 文件大小限制，下载速率控制

## 使用方法

### 1. 手动触发下载

在GitHub仓库页面：

1. 点击 `Actions` 标签页
2. 选择 `Download JACoW Conference Papers` workflow
3. 点击 `Run workflow` 按钮
4. 配置下载参数：
   - **Conference**: 会议名称（如：IPAC, LINAC, PAC），留空下载所有会议
   - **Year**: 年份（如：2023），留空下载所有年份
   - **Max Papers**: 最大下载论文数量，0表示无限制
   - **Dry Run**: 预览模式，只显示要下载的文件列表，不实际下载
   - **Max Size MB**: 单个文件最大大小限制（MB）

### 2. 自动定时下载

Action会在每周日凌晨3点（UTC时间）自动运行，下载最新的论文。

默认设置：
- 下载所有会议的论文
- 最多下载500篇论文
- 单个文件大小限制100MB
- 自动提交新下载的论文到仓库

## 下载参数说明

| 参数 | 说明 | 示例值 | 默认值 |
|------|------|--------|--------|
| conference | 会议名称过滤 | IPAC, LINAC, PAC | 空（所有会议） |
| year | 年份过滤 | 2023, 2022 | 空（所有年份） |
| max_papers | 最大下载数量 | 100, 500 | 0（无限制） |
| dry_run | 预览模式 | true, false | false |
| max_size_mb | 文件大小限制 | 50, 100, 200 | 100 |

## 支持的会议类型

- **IPAC** - International Particle Accelerator Conference
- **LINAC** - Linear Accelerator Conference  
- **PAC** - Particle Accelerator Conference
- **EPAC** - European Particle Accelerator Conference
- **DIPAC** - Beam Diagnostics and Instrumentation for Particle Accelerators
- **BIW** - Beam Instrumentation Workshop
- **SRF** - SRF Workshop
- **IBIC** - International Beam Instrumentation Conference
- **COOL** - Workshop on Beam Cooling and Related Topics
- **HB** - High Intensity and High Brightness Hadron Beams
- **CYCLOTRONS** - International Conference on Cyclotrons and their Applications
- **RuPAC** - Russian Particle Accelerator Conference
- **NA-PAC** - North American Particle Accelerator Conference
- **ICALEPCS** - International Conference on Accelerator and Large Experimental Physics Control Systems
- **PCaPAC** - International Workshop on Personal Computers and Particle Accelerator Controls
- **HIAT** - International Conference on Heavy Ion Accelerator Technology

## 下载结果

### 文件组织结构

```
data/
├── papers/           # 下载的论文文件
│   ├── IPAC/
│   ├── LINAC/
│   └── ...
├── logs/            # 运行日志
│   └── crawler.log
└── reports/         # 下载报告
    ├── download_report_YYYYMMDD_HHMMSS.json
    └── download_summary_YYYYMMDD_HHMMSS.txt
```

### Artifacts

每次运行后，会生成以下artifacts：

1. **jacow-papers-[run-id]**: 下载的论文文件和报告（保留30天）
2. **download-logs-[run-id]**: 运行日志（保留7天）

### 运行报告

每次运行都会生成详细的报告，包括：
- 下载统计信息（成功/失败数量、总大小）
- 错误和警告信息
- 论文分类统计
- 详细的下载列表

## 使用示例

### 示例1：下载2023年IPAC会议的所有论文

```yaml
conference: IPAC
year: 2023
max_papers: 0
dry_run: false
max_size_mb: 100
```

### 示例2：预览最新100篇LINAC论文

```yaml
conference: LINAC
year: 
max_papers: 100
dry_run: true
max_size_mb: 100
```

### 示例3：下载所有会议的最新50篇论文

```yaml
conference: 
year: 
max_papers: 50
dry_run: false
max_size_mb: 50
```

## 监控和故障排除

### 查看运行状态

1. 在GitHub仓库的 `Actions` 页面查看运行历史
2. 点击具体的运行记录查看详细日志
3. 下载artifacts查看下载的文件和详细报告

### 常见问题

**Q: 下载失败怎么办？**
A: 检查运行日志，常见原因包括网络问题、目标网站变更、文件过大等。Action会自动重试3次。

**Q: 如何限制下载大小？**
A: 通过 `max_size_mb` 参数限制单个文件大小，通过 `max_papers` 限制总论文数量。

**Q: 可以下载特定会议的特定年份吗？**
A: 可以，同时设置 `conference` 和 `year` 参数即可。

**Q: 如何避免重复下载？**
A: 程序会自动检查已存在的文件，避免重复下载。使用 `--resume` 参数支持断点续传。

### 失败通知

如果定时任务失败，Action会自动创建一个Issue通知管理员，包含详细的错误信息和运行链接。

## 安全性和限制

- 每次运行最长6小时超时
- 默认并发下载数为3，请求间隔2秒，避免对目标服务器造成过大负担
- 单个文件大小限制可配置（默认100MB）
- 使用合适的User-Agent和请求头，遵守robots.txt
- 自动重试机制处理临时网络错误

## 贡献和反馈

如果遇到问题或有改进建议，请：

1. 检查现有的Issues
2. 创建新的Issue描述问题
3. 提供详细的错误日志和运行参数
4. 考虑提交Pull Request改进功能

---

*最后更新: 2025年9月11日*
