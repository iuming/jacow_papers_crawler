#!/bin/bash
# JACoW 论文爬取器 Linux/Mac 启动脚本

echo "================================"
echo "JACoW 论文爬取器"
echo "================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查是否在虚拟环境中
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "当前在虚拟环境中: $VIRTUAL_ENV"
else
    echo "建议使用虚拟环境运行此程序"
    echo "创建虚拟环境: python3 -m venv venv"
    echo "激活虚拟环境: source venv/bin/activate"
    echo
fi

# 检查依赖是否安装
echo "检查依赖包..."
python3 -c "import requests, bs4, aiohttp, aiofiles" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "依赖安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

echo "依赖检查完成"
echo

# 显示使用说明
echo "使用说明:"
echo "1. 爬取所有论文:           python3 main.py"
echo "2. 指定输出目录:           python3 main.py --output-dir ./my_papers"
echo "3. 限制文件大小:           python3 main.py --max-size 50"
echo "4. 指定并发数:             python3 main.py --concurrent 3"
echo "5. 只下载特定年份:         python3 main.py --year 2023"
echo "6. 只下载特定会议:         python3 main.py --conference IPAC"
echo "7. 试运行模式:             python3 main.py --dry-run"
echo "8. 断点续传:               python3 main.py --resume"
echo "9. 详细输出:               python3 main.py --verbose"
echo

# 询问用户选择
read -p "请选择操作 (1-9) 或按 Enter 使用默认设置: " choice

case $choice in
    1)
        python3 main.py
        ;;
    2)
        read -p "请输入输出目录路径: " output_dir
        python3 main.py --output-dir "$output_dir"
        ;;
    3)
        read -p "请输入最大文件大小(MB): " max_size
        python3 main.py --max-size $max_size
        ;;
    4)
        read -p "请输入并发下载数: " concurrent
        python3 main.py --concurrent $concurrent
        ;;
    5)
        read -p "请输入年份: " year
        python3 main.py --year $year
        ;;
    6)
        read -p "请输入会议名称 (如 IPAC, LINAC): " conference
        python3 main.py --conference $conference
        ;;
    7)
        python3 main.py --dry-run
        ;;
    8)
        python3 main.py --resume
        ;;
    9)
        python3 main.py --verbose
        ;;
    *)
        echo "使用默认设置启动..."
        python3 main.py
        ;;
esac

echo
echo "程序执行完成"
