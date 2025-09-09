#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project: JACoW Invincible Paper Crawler
File: classifier.py
Author: Ming Liu <mliu@ihep.ac.cn>
Created: Sept 9, 2025
Description: Intelligent paper classification and organization system for
             JACoW academic papers. Automatically categorizes downloaded
             papers by conference, year, topic, and other metadata to
             create a well-organized research library.

Development Log:
- Sept 9, 2025: Initial classification framework
- Sept 9, 2025: Added conference-based categorization
- Sept 9, 2025: Implemented year-based organization
- Sept 9, 2025: Added topic classification algorithms
- Sept 9, 2025: Enhanced with statistical reporting

Classification Strategies:
1. Conference-based: IPAC, LINAC, PAC, FEL, etc.
2. Year-based: Chronological organization
3. Topic-based: RF, magnets, beam physics, etc.
4. Author-based: Principal investigator groupings
5. Institution-based: Laboratory and university clusters

Features:
- Automatic directory structure creation
- Intelligent filename normalization
- Metadata extraction and preservation
- Duplicate detection and handling
- Statistical analysis and reporting
- Batch processing capabilities

File Organization Pattern:
- papers/
  ├── 2023/
  │   ├── IPAC/
  │   │   ├── individual_papers/
  │   │   └── proceedings/
  │   └── LINAC/
  └── 2022/

Classification Algorithms:
- Conference name extraction from metadata
- Year detection from paper titles and URLs
- Topic classification using keyword matching
- Author affiliation analysis
- Citation network analysis (future enhancement)

Technical Implementation:
- Uses regex patterns for metadata extraction
- File system operations with pathlib
- Statistical analysis with collections
- Error-safe file moving operations

License: MIT License
=============================================================================
"""

import shutil
from pathlib import Path
from typing import List, Dict, Optional, Set
from collections import defaultdict, Counter
import re

from utils.config import Config
from utils.helpers import create_safe_directory, extract_year_from_text


class PaperClassifier:
    """论文分类器"""
    
    def __init__(self, base_dir: Path, logger=None):
        self.base_dir = Path(base_dir)
        self.logger = logger
        self.config = Config()
        
        # 分类统计
        self.classification_stats = defaultdict(int)
        
    def classify_papers(self, download_results: List[Dict[str, str]]) -> Dict[str, int]:
        """
        分类整理已下载的论文
        
        Args:
            download_results: 下载结果列表
        
        Returns:
            分类统计信息
        """
        if self.logger:
            self.logger.info("开始分类整理论文...")
        
        successful_downloads = [
            result for result in download_results 
            if result.get('success', False) and not result.get('skipped', False)
        ]
        
        if not successful_downloads:
            if self.logger:
                self.logger.info("没有需要分类的论文")
            return {}
        
        # 按会议和年份组织
        self._organize_by_conference_and_year(successful_downloads)
        
        # 按主题分类
        self._organize_by_topic(successful_downloads)
        
        # 生成分类报告
        if self.logger:
            self._log_classification_stats()
        
        return dict(self.classification_stats)
    
    def _organize_by_conference_and_year(self, papers: List[Dict[str, str]]):
        """
        按会议和年份组织论文
        
        Args:
            papers: 论文列表
        """
        for paper in papers:
            try:
                conference = paper.get('conference', 'Unknown')
                year = paper.get('year', 0)
                file_path = Path(paper.get('file_path', ''))
                
                if not file_path.exists():
                    continue
                
                # 创建目标目录结构: Conference/Year/
                if year and year > 1980:  # 有效年份
                    target_dir = create_safe_directory(
                        self.base_dir, 
                        f"{conference}/{year}"
                    )
                else:
                    target_dir = create_safe_directory(
                        self.base_dir, 
                        f"{conference}/Unknown_Year"
                    )
                
                # 移动文件
                target_path = target_dir / file_path.name
                if not target_path.exists():
                    shutil.move(str(file_path), str(target_path))
                    paper['file_path'] = str(target_path)  # 更新路径
                    
                    # 更新统计
                    category = f"{conference}/{year if year else 'Unknown_Year'}"
                    self.classification_stats[category] += 1
                    
                    if self.logger:
                        self.logger.debug(f"移动文件: {file_path.name} -> {target_dir}")
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"组织论文失败: {paper.get('title', '')} - {str(e)}")
    
    def _organize_by_topic(self, papers: List[Dict[str, str]]):
        """
        按主题分类论文
        
        Args:
            papers: 论文列表
        """
        topic_stats = defaultdict(int)
        
        for paper in papers:
            try:
                title = paper.get('title', '')
                abstract = paper.get('abstract', '')
                keywords = paper.get('keywords', '')
                
                # 使用配置中的分类方法
                topic = self.config.classify_by_keywords(title, abstract + ' ' + keywords)
                topic_stats[topic] += 1
                
                # 可选：创建按主题的软链接或副本
                if self._should_create_topic_links():
                    self._create_topic_link(paper, topic)
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"主题分类失败: {paper.get('title', '')} - {str(e)}")
        
        # 更新统计信息
        for topic, count in topic_stats.items():
            self.classification_stats[f"Topic_{topic}"] = count
    
    def _create_topic_link(self, paper: Dict[str, str], topic: str):
        """
        为论文创建主题分类链接
        
        Args:
            paper: 论文信息
            topic: 主题分类
        """
        try:
            file_path = Path(paper.get('file_path', ''))
            if not file_path.exists():
                return
            
            # 创建主题目录
            topic_dir = create_safe_directory(self.base_dir, f"Topics/{topic}")
            
            # 创建软链接（Windows上可能需要管理员权限）
            link_path = topic_dir / file_path.name
            
            if not link_path.exists():
                try:
                    # 尝试创建软链接
                    link_path.symlink_to(file_path.absolute())
                except (OSError, NotImplementedError):
                    # 如果软链接失败，创建硬链接或复制文件
                    try:
                        link_path.hardlink_to(file_path)
                    except (OSError, NotImplementedError):
                        # 最后选择复制文件
                        shutil.copy2(str(file_path), str(link_path))
                
                if self.logger:
                    self.logger.debug(f"创建主题链接: {link_path}")
        
        except Exception as e:
            if self.logger:
                self.logger.debug(f"创建主题链接失败: {str(e)}")
    
    def _should_create_topic_links(self) -> bool:
        """
        判断是否应该创建主题链接
        
        Returns:
            是否创建主题链接
        """
        # 可以基于配置或论文数量决定
        return len(self.classification_stats) > 10  # 如果论文数量超过10篇才创建主题链接
    
    def _log_classification_stats(self):
        """记录分类统计信息"""
        if not self.logger:
            return
        
        self.logger.info("=" * 50)
        self.logger.info("分类统计:")
        
        # 按会议统计
        conference_stats = defaultdict(int)
        year_stats = defaultdict(int)
        topic_stats = defaultdict(int)
        
        for category, count in self.classification_stats.items():
            if category.startswith('Topic_'):
                topic_name = category.replace('Topic_', '')
                topic_stats[topic_name] = count
            elif '/' in category:
                conf, year = category.split('/', 1)
                conference_stats[conf] += count
                if year != 'Unknown_Year':
                    year_stats[year] += count
        
        # 输出会议统计
        if conference_stats:
            self.logger.info("会议分布:")
            for conf, count in sorted(conference_stats.items()):
                self.logger.info(f"  {conf}: {count} 篇")
        
        # 输出年份统计
        if year_stats:
            self.logger.info("年份分布:")
            for year, count in sorted(year_stats.items(), reverse=True):
                self.logger.info(f"  {year}: {count} 篇")
        
        # 输出主题统计
        if topic_stats:
            self.logger.info("主题分布:")
            for topic, count in sorted(topic_stats.items(), key=lambda x: x[1], reverse=True):
                self.logger.info(f"  {topic}: {count} 篇")
        
        self.logger.info("=" * 50)
    
    def generate_classification_report(self, output_file: Optional[Path] = None) -> str:
        """
        生成分类报告
        
        Args:
            output_file: 输出文件路径
        
        Returns:
            报告内容
        """
        report_lines = []
        report_lines.append("JACoW 论文分类报告")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # 总体统计
        total_papers = sum(
            count for category, count in self.classification_stats.items()
            if not category.startswith('Topic_')
        )
        report_lines.append(f"总论文数: {total_papers}")
        report_lines.append("")
        
        # 按会议统计
        conference_stats = defaultdict(int)
        year_stats = defaultdict(int)
        topic_stats = defaultdict(int)
        
        for category, count in self.classification_stats.items():
            if category.startswith('Topic_'):
                topic_name = category.replace('Topic_', '')
                topic_stats[topic_name] = count
            elif '/' in category:
                conf, year = category.split('/', 1)
                conference_stats[conf] += count
                if year != 'Unknown_Year':
                    year_stats[year] += count
        
        # 会议统计
        if conference_stats:
            report_lines.append("会议分布:")
            report_lines.append("-" * 30)
            for conf, count in sorted(conference_stats.items()):
                percentage = (count / total_papers) * 100 if total_papers > 0 else 0
                report_lines.append(f"{conf:15} {count:5d} 篇 ({percentage:5.1f}%)")
            report_lines.append("")
        
        # 年份统计
        if year_stats:
            report_lines.append("年份分布:")
            report_lines.append("-" * 30)
            for year, count in sorted(year_stats.items(), reverse=True):
                percentage = (count / total_papers) * 100 if total_papers > 0 else 0
                report_lines.append(f"{year:15} {count:5d} 篇 ({percentage:5.1f}%)")
            report_lines.append("")
        
        # 主题统计
        if topic_stats:
            report_lines.append("主题分布:")
            report_lines.append("-" * 30)
            for topic, count in sorted(topic_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_papers) * 100 if total_papers > 0 else 0
                report_lines.append(f"{topic:20} {count:5d} 篇 ({percentage:5.1f}%)")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # 保存到文件
        if output_file:
            try:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                if self.logger:
                    self.logger.info(f"分类报告已保存到: {output_file}")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"保存分类报告失败: {str(e)}")
        
        return report_content
    
    def create_directory_structure_info(self) -> str:
        """
        创建目录结构信息
        
        Returns:
            目录结构信息字符串
        """
        info_lines = []
        info_lines.append("论文目录结构:")
        info_lines.append("=" * 30)
        
        try:
            for conf_dir in sorted(self.base_dir.iterdir()):
                if conf_dir.is_dir() and conf_dir.name != 'Topics':
                    info_lines.append(f"📁 {conf_dir.name}/")
                    
                    for year_dir in sorted(conf_dir.iterdir()):
                        if year_dir.is_dir():
                            file_count = len(list(year_dir.glob('*')))
                            info_lines.append(f"  📁 {year_dir.name}/ ({file_count} 个文件)")
            
            # 主题目录
            topics_dir = self.base_dir / 'Topics'
            if topics_dir.exists() and topics_dir.is_dir():
                info_lines.append("📁 Topics/")
                for topic_dir in sorted(topics_dir.iterdir()):
                    if topic_dir.is_dir():
                        file_count = len(list(topic_dir.glob('*')))
                        info_lines.append(f"  📁 {topic_dir.name}/ ({file_count} 个文件)")
        
        except Exception as e:
            info_lines.append(f"获取目录结构失败: {str(e)}")
        
        return "\n".join(info_lines)
