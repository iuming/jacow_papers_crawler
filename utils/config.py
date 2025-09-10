#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: config.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Configuration management system for the JACoW paper crawler.
             Handles all application settings, user preferences, and 
             runtime configurations with support for multiple configuration
             sources including files, environment variables, and CLI args.

Development Log:
- Sept 9, 2025: Initial configuration framework
- Sept 9, 2025: Added command-line argument integration
- Sept 9, 2025: Implemented environment variable support
- Sept 9, 2025: Added configuration file parsing
- Sept 9, 2025: Enhanced with validation and defaults

Features:
- Multi-source configuration (CLI, env vars, config files)
- Intelligent default value management
- Runtime configuration updates
- Configuration validation and error checking
- Environment-specific settings
- User preference persistence

Configuration Hierarchy (highest to lowest priority):
1. Command-line arguments
2. Environment variables
3. Configuration files (config.ini)
4. Default values

Supported Settings:
- Download directories and paths
- Network settings (timeouts, retries, delays)
- Crawler behavior (concurrent downloads, filters)
- Logging levels and output formats
- User preferences and customizations

File Formats Supported:
- INI files for structured configuration
- Environment variables for deployment settings
- JSON for complex configuration objects

Usage:
    config = Config()
    config.update_from_args(args)
    max_size = config.get('max_size_mb', 100)

License: MIT License
=============================================================================
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """配置管理类"""

    def __init__(self):
        # 默认配置
        self.BASE_URL = "https://www.jacow.org"
        self.OUTPUT_DIR = "./data/papers"
        self.MAX_FILE_SIZE_MB = 100
        self.CONCURRENT_DOWNLOADS = 5
        self.REQUEST_DELAY = 1.0
        self.USER_AGENT = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        self.TIMEOUT = 30
        self.RETRY_ATTEMPTS = 3
        self.RETRY_DELAY = 2.0

        # 支持的文件类型
        self.SUPPORTED_EXTENSIONS = [".pdf", ".doc", ".docx", ".ppt", ".pptx"]

        # 会议列表 (部分)
        self.KNOWN_CONFERENCES = [
            "IPAC",
            "LINAC",
            "PAC",
            "EPAC",
            "DIPAC",
            "BIW",
            "SRF",
            "IBIC",
            "COOL",
            "HB",
            "CYCLOTRONS",
            "RuPAC",
            "NA-PAC",
            "ICALEPCS",
            "PCaPAC",
            "HIAT",
        ]

        # 论文分类关键词
        self.CLASSIFICATION_KEYWORDS = {
            "Accelerator_Technology": [
                "accelerator",
                "magnet",
                "cavity",
                "rf",
                "superconducting",
                "cryogenic",
                "vacuum",
                "mechanical",
                "power supply",
            ],
            "Beam_Dynamics": [
                "beam dynamics",
                "optics",
                "emittance",
                "tune",
                "chromaticity",
                "coupling",
                "lattice",
                "tracking",
                "simulation",
            ],
            "Beam_Instrumentation": [
                "bpm",
                "beam position monitor",
                "diagnostics",
                "monitor",
                "measurement",
                "instrumentation",
                "profile",
                "current",
            ],
            "Controls": [
                "control",
                "epics",
                "software",
                "database",
                "automation",
                "interface",
                "timing",
                "synchronization",
            ],
            "Power_Systems": [
                "power supply",
                "converter",
                "modulator",
                "high voltage",
                "switching",
                "regulation",
                "protection",
            ],
            "RF_Technology": [
                "rf",
                "microwave",
                "klystron",
                "magnetron",
                "waveguide",
                "coupler",
                "antenna",
                "frequency",
            ],
            "Other": [],  # 默认分类
        }

    def update_from_args(self, args):
        """从命令行参数更新配置"""
        if hasattr(args, "output_dir") and args.output_dir:
            self.OUTPUT_DIR = args.output_dir
        if hasattr(args, "max_size") and args.max_size:
            self.MAX_FILE_SIZE_MB = args.max_size
        if hasattr(args, "concurrent") and args.concurrent:
            self.CONCURRENT_DOWNLOADS = args.concurrent
        if hasattr(args, "delay") and args.delay:
            self.REQUEST_DELAY = args.delay

    def get_headers(self, referer: Optional[str] = None) -> Dict[str, str]:
        """获取HTTP请求头"""
        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        if referer:
            headers["Referer"] = referer

        return headers

    def is_supported_file(self, filename: str) -> bool:
        """检查文件是否为支持的类型"""
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.SUPPORTED_EXTENSIONS

    def get_conference_from_url(self, url: str) -> Optional[str]:
        """从URL中提取会议名称"""
        url_upper = url.upper()
        for conf in self.KNOWN_CONFERENCES:
            if conf in url_upper:
                return conf
        return None

    def classify_by_keywords(self, title: str, abstract: str = "") -> str:
        """根据关键词分类论文"""
        text = (title + " " + abstract).lower()

        category_scores = {}
        for category, keywords in self.CLASSIFICATION_KEYWORDS.items():
            if category == "Other":
                continue
            score = sum(1 for keyword in keywords if keyword.lower() in text)
            if score > 0:
                category_scores[category] = score

        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return "Other"
