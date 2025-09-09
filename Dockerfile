# 使用Python 3.9官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/data/papers /app/data/logs /app/data/reports

# 设置数据目录为卷
VOLUME ["/app/data"]

# 暴露端口（如果将来需要Web界面）
EXPOSE 8080

# 默认命令
CMD ["python", "main.py", "--help"]

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 标签
LABEL maintainer="JACoW Crawler"
LABEL version="1.0"
LABEL description="JACoW论文爬取和下载工具"
