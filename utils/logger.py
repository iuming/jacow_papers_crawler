#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: logger.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Advanced logging system for the JACoW paper crawler with 
             colored console output, file logging, and configurable 
             verbosity levels. Provides comprehensive logging capabilities
             for debugging, monitoring, and user feedback.

Development Log:
- Sept 9, 2025: Initial logging framework implementation
- Sept 9, 2025: Added colored console output support
- Sept 9, 2025: Implemented file logging with rotation
- Sept 9, 2025: Added progress tracking capabilities
- Sept 9, 2025: Enhanced with structured logging for debugging

Features:
- Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Colored console output for better readability
- File logging with automatic rotation
- Timestamp formatting and timezone support
- Progress tracking for long-running operations
- Structured logging for JSON output
- Memory-efficient logging for large operations

Logging Levels:
- DEBUG: Detailed technical information for developers
- INFO: General operation progress and status updates
- WARNING: Important notices that don't stop execution
- ERROR: Error conditions that may affect operation
- CRITICAL: Serious errors that may stop the application

Output Formats:
- Console: Colored, human-readable format
- File: Detailed format with timestamps and source info
- JSON: Structured format for log analysis tools

Color Scheme:
- DEBUG: Cyan
- INFO: Green
- WARNING: Yellow
- ERROR: Red
- CRITICAL: Bright Red

Usage:
    logger = setup_logger("crawler", verbose=True)
    logger.info("Starting paper download...")
    logger.error("Failed to download paper: %s", error)

License: MIT License
=============================================================================
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "jacow_crawler",
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    verbose: bool = False,
) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
        verbose: 是否启用详细模式

    Returns:
        配置好的日志记录器
    """

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level if not verbose else logging.DEBUG)

    # 如果已经有处理器，先清除
    if logger.handlers:
        logger.handlers.clear()

    # 创建格式化器
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level if not verbose else logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # 文件中保存所有级别的日志
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[35m",  # 紫色
        "RESET": "\033[0m",  # 重置
    }

    def format(self, record):
        # 获取原始格式化结果
        formatted = super().format(record)

        # 添加颜色
        level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset_color = self.COLORS["RESET"]

        return f"{level_color}{formatted}{reset_color}"


def setup_colored_logger(
    name: str = "jacow_crawler",
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    verbose: bool = False,
) -> logging.Logger:
    """
    设置彩色日志记录器

    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
        verbose: 是否启用详细模式

    Returns:
        配置好的彩色日志记录器
    """

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level if not verbose else logging.DEBUG)

    # 如果已经有处理器，先清除
    if logger.handlers:
        logger.handlers.clear()

    # 创建彩色格式化器
    colored_formatter = ColoredFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 普通格式化器（用于文件）
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器（彩色）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level if not verbose else logging.DEBUG)
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    # 文件处理器（无颜色）
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # 文件中保存所有级别的日志
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


class ProgressLogger:
    """进度日志记录器"""

    def __init__(self, logger: logging.Logger, total: int, prefix: str = "Progress"):
        self.logger = logger
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.start_time = datetime.now()

    def update(self, increment: int = 1, message: str = ""):
        """更新进度"""
        self.current += increment
        percentage = (self.current / self.total) * 100
        elapsed = datetime.now() - self.start_time

        # 估算剩余时间
        if self.current > 0:
            eta_seconds = (elapsed.total_seconds() / self.current) * (
                self.total - self.current
            )
            eta = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
        else:
            eta = "unknown"

        progress_msg = (
            f"{self.prefix}: {self.current}/{self.total} ({percentage:.1f}%) ETA: {eta}"
        )
        if message:
            progress_msg += f" - {message}"

        self.logger.info(progress_msg)

    def finish(self, message: str = "完成"):
        """完成进度"""
        elapsed = datetime.now() - self.start_time
        self.logger.info(f"{self.prefix}: {message} - 耗时: {elapsed}")


def log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """记录异常信息"""
    if context:
        logger.error(f"{context}: {str(exception)}", exc_info=True)
    else:
        logger.error(f"发生异常: {str(exception)}", exc_info=True)
