#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: helpers.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Comprehensive utility functions and helper classes for the
             JACoW paper crawler. Provides common functionality for file
             operations, string processing, validation, and data manipulation
             used throughout the crawler system.

Development Log:
- Sept 9, 2025: Initial utility functions collection
- Sept 9, 2025: Added file operation helpers
- Sept 9, 2025: Implemented string processing utilities
- Sept 9, 2025: Added validation and sanitization functions
- Sept 9, 2025: Enhanced with data format conversion utilities

Function Categories:

1. File Operations:
   - Safe filename sanitization
   - File size formatting and conversion
   - MIME type detection and validation
   - Path manipulation and validation

2. String Processing:
   - URL validation and normalization
   - Text cleaning and sanitization
   - Pattern matching and extraction
   - Encoding and decoding utilities

3. Data Validation:
   - Input validation functions
   - Data type checking and conversion
   - Range and format validation
   - Error handling and reporting

4. Network Utilities:
   - URL parsing and construction
   - Header manipulation
   - Response validation
   - Timeout and retry helpers

5. Format Conversion:
   - Size unit conversion (bytes, KB, MB, GB)
   - Time format conversion
   - Data structure serialization
   - CSV and JSON utilities

Usage Examples:
    safe_name = sanitize_filename("Paper: Title/With*Special?Chars")
    size_str = format_file_size(1048576)  # Returns "1.0 MB"
    is_valid = validate_url("https://example.com/paper.pdf")

Common Use Cases:
- Filename sanitization for cross-platform compatibility
- File size validation and reporting
- URL validation and normalization
- Text processing for metadata extraction

License: MIT License
=============================================================================
"""

import os
import re
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlparse, unquote
import unicodedata


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    清理文件名，移除非法字符

    Args:
        filename: 原始文件名
        max_length: 最大长度

    Returns:
        清理后的文件名
    """
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    filename = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", filename)  # 移除控制字符

    # 标准化Unicode字符
    filename = unicodedata.normalize("NFKD", filename)

    # 移除前后空格和点号
    filename = filename.strip(" .")

    # 限制长度
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[: max_length - len(ext)] + ext

    # 如果文件名为空，使用默认名称
    if not filename:
        filename = "untitled"

    return filename


def get_file_extension_from_url(url: str) -> str:
    """
    从URL中获取文件扩展名

    Args:
        url: 文件URL

    Returns:
        文件扩展名（包含点号）
    """
    parsed = urlparse(url)
    path = unquote(parsed.path)
    ext = os.path.splitext(path)[1].lower()

    # 如果没有扩展名，尝试从查询参数中获取
    if not ext and parsed.query:
        # 查找查询参数中的文件名
        if "filename=" in parsed.query:
            match = re.search(r"filename=([^&]+)", parsed.query)
            if match:
                filename = unquote(match.group(1))
                ext = os.path.splitext(filename)[1].lower()

    return ext


def get_file_size_mb(file_path: Path) -> float:
    """
    获取文件大小（MB）

    Args:
        file_path: 文件路径

    Returns:
        文件大小（MB）
    """
    try:
        size_bytes = file_path.stat().st_size
        return size_bytes / (1024 * 1024)
    except (OSError, FileNotFoundError):
        return 0.0


def calculate_file_hash(file_path: Path, algorithm: str = "md5") -> str:
    """
    计算文件哈希值

    Args:
        file_path: 文件路径
        algorithm: 哈希算法（md5, sha1, sha256等）

    Returns:
        文件哈希值
    """
    hash_obj = hashlib.new(algorithm)

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except (OSError, FileNotFoundError):
        return ""


def extract_year_from_text(text: str) -> Optional[int]:
    """
    从文本中提取年份

    Args:
        text: 输入文本

    Returns:
        提取的年份，如果未找到则返回None
    """
    # 查找4位数字的年份（1980-2050）
    year_match = re.search(r"\b(19[8-9]\d|20[0-5]\d)\b", text)
    if year_match:
        return int(year_match.group(1))
    return None


def extract_conference_from_text(
    text: str, known_conferences: List[str]
) -> Optional[str]:
    """
    从文本中提取会议名称

    Args:
        text: 输入文本
        known_conferences: 已知会议列表

    Returns:
        提取的会议名称，如果未找到则返回None
    """
    text_upper = text.upper()
    for conf in known_conferences:
        if conf.upper() in text_upper:
            return conf
    return None


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小显示

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        格式化的大小字符串
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def create_safe_directory(base_path: Path, dir_name: str) -> Path:
    """
    创建安全的目录名称

    Args:
        base_path: 基础路径
        dir_name: 目录名称

    Returns:
        创建的目录路径
    """
    safe_name = sanitize_filename(dir_name)
    dir_path = base_path / safe_name
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def is_valid_url(url: str) -> bool:
    """
    检查URL是否有效

    Args:
        url: 要检查的URL

    Returns:
        True如果URL有效，False否则
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def merge_dicts(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    合并多个字典

    Args:
        *dicts: 要合并的字典

    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    安全获取字典值

    Args:
        data: 字典数据
        key: 键名
        default: 默认值

    Returns:
        字典值或默认值
    """
    try:
        return data.get(key, default)
    except (AttributeError, TypeError):
        return default


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    将列表分块

    Args:
        lst: 要分块的列表
        chunk_size: 块大小

    Returns:
        分块后的列表
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_mime_type(file_path: Path) -> str:
    """
    获取文件MIME类型

    Args:
        file_path: 文件路径

    Returns:
        MIME类型字符串
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or "application/octet-stream"


def normalize_url(url: str, base_url: str = "") -> str:
    """
    标准化URL

    Args:
        url: 要标准化的URL
        base_url: 基础URL

    Returns:
        标准化的URL
    """
    if base_url and not url.startswith(("http://", "https://")):
        url = urljoin(base_url, url)
    return url.strip()


def extract_title_from_filename(filename: str) -> str:
    """
    从文件名提取标题

    Args:
        filename: 文件名

    Returns:
        提取的标题
    """
    # 移除扩展名
    title = os.path.splitext(filename)[0]

    # 替换下划线和连字符为空格
    title = re.sub(r"[_-]", " ", title)

    # 移除多余的空格
    title = re.sub(r"\s+", " ", title).strip()

    # 首字母大写
    title = title.title()

    return title
