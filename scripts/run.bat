@echo off
chcp 65001 >nul
echo ================================
echo JACoW 论文爬取器
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
if defined VIRTUAL_ENV (
    echo 当前在虚拟环境中: %VIRTUAL_ENV%
) else (
    echo 建议使用虚拟环境运行此程序
    echo 创建虚拟环境: python -m venv venv
    echo 激活虚拟环境: venv\Scripts\activate
    echo.
)

REM 检查依赖是否安装
echo 检查依赖包...
python -c "import requests, bs4, aiohttp, aiofiles" >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo 依赖检查完成
echo.

REM 显示使用说明
echo 使用说明:
echo 1. 爬取所有论文:           python main.py
echo 2. 指定输出目录:           python main.py --output-dir ./my_papers
echo 3. 限制文件大小:           python main.py --max-size 50
echo 4. 指定并发数:             python main.py --concurrent 3
echo 5. 只下载特定年份:         python main.py --year 2023
echo 6. 只下载特定会议:         python main.py --conference IPAC
echo 7. 试运行模式:             python main.py --dry-run
echo 8. 断点续传:               python main.py --resume
echo 9. 详细输出:               python main.py --verbose
echo.

REM 询问用户选择
set /p choice="请选择操作 (1-9) 或按 Enter 使用默认设置: "

if "%choice%"=="1" (
    python main.py
) else if "%choice%"=="2" (
    set /p output_dir="请输入输出目录路径: "
    python main.py --output-dir "%output_dir%"
) else if "%choice%"=="3" (
    set /p max_size="请输入最大文件大小(MB): "
    python main.py --max-size %max_size%
) else if "%choice%"=="4" (
    set /p concurrent="请输入并发下载数: "
    python main.py --concurrent %concurrent%
) else if "%choice%"=="5" (
    set /p year="请输入年份: "
    python main.py --year %year%
) else if "%choice%"=="6" (
    set /p conference="请输入会议名称 (如 IPAC, LINAC): "
    python main.py --conference %conference%
) else if "%choice%"=="7" (
    python main.py --dry-run
) else if "%choice%"=="8" (
    python main.py --resume
) else if "%choice%"=="9" (
    python main.py --verbose
) else (
    echo 使用默认设置启动...
    python main.py
)

echo.
echo 程序执行完成
pause
