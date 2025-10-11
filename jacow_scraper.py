#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal JACoW Conference Web Scraper

Author: Ming Liu
Date: October 9, 2025
Description: A comprehensive web scraper for all JACoW conference papers and abstracts.
             Automatically discovers conferences from JACoW proceedings page and scrapes
             paper information organized by sessions, downloads PDFs, and exports
             data in multiple formats (JSON, CSV, TXT).

Website: https://www.jacow.org/Main/Proceedings
Features:
- Automatic conference discovery
- Session-based paper extraction
- PDF download with validation
- Multi-format data export
- Robust error handling and retry mechanisms
- Comprehensive logging
"""

import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

class JACoWScraper:
    """
    Universal web scraper for JACoW conference proceedings.

    This scraper automatically discovers all conferences from the JACoW proceedings
    page and scrapes paper information from each conference that follows the
    standard JACoW format.
    """

    def __init__(self, base_url: str = "https://www.jacow.org/Main/Proceedings", output_dir: str = "JACoW_Data"):
        """
        Initialize the JACoW scraper.

        Args:
            base_url: Base URL of the JACoW proceedings page
            output_dir: Directory to store scraped data and PDFs
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('jacow_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Conference configurations
        self.conferences = []

        # Initialize directories and statistics
        self.create_directories()
        self.stats = {'total_conferences': 0, 'processed_conferences': 0, 'total_papers': 0,
                     'downloaded_presentations': 0, 'downloaded_papers': 0, 'downloaded_posters': 0,
                     'errors': 0, 'sessions_processed': 0}

        # Load conferences automatically
        self.load_conferences()

    def load_conferences(self):
        """Load all conferences from the JACoW proceedings page."""
        try:
            self.logger.info("Loading conferences from JACoW proceedings page...")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            conferences = []
            # Find all conference links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and 'proceedings.jacow.org' in href and href.endswith('/'):
                    conference_name = link.get_text().strip()
                    if conference_name and len(conference_name) > 2:  # Filter meaningful names
                        # Extract conference code from URL (e.g., 'srf2017' from 'https://proceedings.jacow.org/srf2017/')
                        conf_code = href.rstrip('/').split('/')[-1]
                        conferences.append({
                            'name': conference_name,
                            'code': conf_code,
                            'url': href,
                            'status': 'pending'  # pending, processing, completed, failed
                        })

            self.conferences = conferences
            self.stats['total_conferences'] = len(conferences)
            self.logger.info(f"Found {len(conferences)} conferences on JACoW")

        except Exception as e:
            self.logger.error(f"Failed to load conferences: {e}")
            self.conferences = []

    def check_conference_structure(self, conf_url: str) -> bool:
        """
        Check if a conference follows the standard JACoW structure.

        Args:
            conf_url: Conference URL to check

        Returns:
            True if the conference has the expected structure
        """
        try:
            # Try different session URL patterns
            session_urls = [
                f"{conf_url}html/sessi0n.htm",    # Standard pattern
                f"{conf_url}html/sessi0n1.htm",   # Alternative pattern (SRF2017)
                f"{conf_url}html/session.htm",    # Alternative spelling
                f"{conf_url}html/sessions.htm"    # Plural form
            ]

            for session_url in session_urls:
                try:
                    response = self.session.get(session_url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Check for session link or table
                        session_link = soup.find('a', href=lambda x: x and 'sessi0n' in x)
                        table = soup.find('table')
                        if session_link or table:
                            return True
                except:
                    continue

            return False

        except Exception as e:
            self.logger.warning(f"Failed to check conference structure for {conf_url}: {e}")
            return False

    def create_directories(self):
        """Create necessary directory structure for output files."""
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "Conferences").mkdir(exist_ok=True)
        (self.output_dir / "Presentations").mkdir(exist_ok=True)
        (self.output_dir / "Papers").mkdir(exist_ok=True)
        (self.output_dir / "Posters").mkdir(exist_ok=True)
        (self.output_dir / "Debug").mkdir(exist_ok=True)
        self.logger.info(f"Created output directory: {self.output_dir}")

    def safe_filename(self, filename: str, max_length: int = 60) -> str:
        """
        Convert filename to safe filesystem name.

        Args:
            filename: Original filename
            max_length: Maximum allowed filename length

        Returns:
            Safe filename string
        """
        if not filename:
            return "unknown"

        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*\r\n]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename)
        filename = filename.strip(' ._')

        # Truncate if too long
        if len(filename) > max_length:
            parts = filename.split(' - ', 1)
            if len(parts) == 2:
                paper_id_part = parts[0]
                title_part = parts[1]
                title_max = max_length - len(paper_id_part) - 3
                if title_max > 5:
                    title_part = title_part[:title_max].rsplit(' ', 1)[0] if ' ' in title_part[:title_max] else title_part[:title_max]
                    filename = f"{paper_id_part} - {title_part}"
                else:
                    filename = paper_id_part
            else:
                filename = filename[:max_length].rsplit(' ', 1)[0]

        return filename or "unknown"

    def get_page_content(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """
        Get webpage content with retry mechanism.

        Args:
            url: URL to fetch
            retries: Number of retry attempts

        Returns:
            BeautifulSoup object or None if failed
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                self.logger.warning(f"Failed to fetch page (attempt {attempt + 1}/{retries}) {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    self.logger.error(f"Final failure fetching page {url}: {e}")
                    self.stats['errors'] += 1
        return None

    def load_sessions_for_conference(self, conference: Dict[str, str]) -> List[Dict[str, str]]:
        """Load session configuration for a specific conference."""
        conf_url = conference['url']
        conf_code = conference['code']

        try:
            # Try different session URL patterns
            session_urls = [
                f"{conf_url}html/sessi0n.htm",    # Standard pattern
                f"{conf_url}html/sessi0n1.htm",   # Alternative pattern (SRF2017)
                f"{conf_url}html/session.htm",    # Alternative spelling
                f"{conf_url}html/sessions.htm"    # Plural form
            ]

            soup = None
            for session_url in session_urls:
                try:
                    response = self.session.get(session_url, timeout=10)
                    if response.status_code == 200:
                        temp_soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Check if page uses frames
                        if 'frames' in temp_soup.get_text().lower() or 'your browser doesn\'t support them' in temp_soup.get_text().lower():
                            self.logger.info(f"Page uses frames, trying alternative URL for {conf_code}")
                            continue
                        
                        soup = temp_soup
                        self.logger.info(f"Found session page for {conf_code}: {session_url}")
                        break
                except:
                    continue

            if not soup:
                self.logger.warning(f"No session page found for {conf_code}")
                return []

            sessions = []

            # Try to find session table
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        session_id = cols[0].get_text().strip()
                        session_name = cols[1].get_text().strip()

                        # Skip header rows and invalid entries
                        if (session_id and session_name and
                            session_id.isupper() and len(session_id) >= 4 and
                            session_id != 'Table' and 'Table of Sessions' not in session_id):
                            sessions.append({
                                'id': session_id,
                                'name': f"{session_id} - {session_name}",
                                'url': f"{conf_url}html/{session_id.lower()}.htm"
                            })

            # Fallback: if no table found, try text parsing
            if not sessions:
                page_text = soup.get_text()
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]

                i = 0
                while i < len(lines):
                    # Look for session ID patterns (4+ uppercase letters)
                    if len(lines[i]) >= 4 and lines[i].isupper() and lines[i].isalpha():
                        session_id = lines[i]
                        if i + 1 < len(lines):
                            session_name = lines[i + 1]
                            if session_name and not session_name.isupper():  # Avoid matching another session ID
                                sessions.append({
                                    'id': session_id,
                                    'name': f"{session_id} - {session_name}",
                                    'url': f"{conf_url}html/{session_id.lower()}.htm"
                                })
                        i += 2
                    else:
                        i += 1

            self.logger.info(f"Loaded {len(sessions)} sessions for {conf_code}")
            return sessions

        except Exception as e:
            self.logger.error(f"Failed to load sessions for {conf_code}: {e}")
            return []

    def extract_papers_from_session(self, soup: BeautifulSoup, session_id: str, conf_code: str) -> List[Dict[str, Any]]:
        """
        Extract paper information from a session page.

        Args:
            soup: BeautifulSoup object of the session page
            session_id: Session ID (e.g., 'MOXA')
            conf_code: Conference code (e.g., 'srf2017')

        Returns:
            List of paper dictionaries
        """
        papers = []
        page_text = soup.get_text()

        # Save debug information
        debug_file = self.output_dir / "Debug" / f"{conf_code}_{session_id}_page_text.txt"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(page_text)

        # Find all paper sections in the HTML
        paper_pattern = rf'{re.escape(session_id)}(\d+)'
        paper_matches = re.findall(paper_pattern, page_text)

        if not paper_matches:
            self.logger.warning(f"No papers found in session {session_id}")
            return papers

        # Remove duplicates and sort
        paper_nums = sorted(list(set(paper_matches)))
        self.logger.info(f"Found {len(paper_nums)} potential papers in session {session_id}")

        for paper_num in paper_nums:
            paper_id = f"{session_id}{paper_num}"

            # Extract paper details
            paper_info = self.extract_paper_details_from_page(soup, paper_id, conf_code)
            if paper_info:
                papers.append(paper_info)
                self.logger.info(f"  ✓ {paper_id}: {paper_info['title'][:50]}...")

        return papers

    def extract_paper_details_from_page(self, soup: BeautifulSoup, paper_id: str, conf_code: str) -> Dict[str, Any]:
        """
        Extract detailed information for a single paper from the session page.

        Args:
            soup: BeautifulSoup object of the session page
            paper_id: Paper ID (e.g., 'MOXA1')
            conf_code: Conference code (e.g., 'srf2017')

        Returns:
            Dictionary containing paper information
        """
        paper_info = {
            'paper_id': paper_id,
            'title': '',
            'authors': [],
            'institutions': [],
            'abstract': '',
            'presentation_url': f"https://proceedings.jacow.org/{conf_code}/talks/{paper_id.lower()}_talk.pdf",
            'paper_url': f"https://proceedings.jacow.org/{conf_code}/papers/{paper_id.lower()}.pdf",
            'poster_url': f"https://proceedings.jacow.org/{conf_code}/posters/{paper_id.lower()}_poster.pdf",
            'doi': f"https://doi.org/10.18429/JACoW-{conf_code.upper()}-{paper_id}",
            'page_number': '',
            'presentation_available': False,
            'paper_available': False,
            'poster_available': False
        }

        # Convert soup to text for easier parsing
        page_text = soup.get_text()

        # Find the paper section by looking for the paper ID
        paper_id_pattern = rf'{re.escape(paper_id)}\s*(\d*)'
        paper_match = re.search(paper_id_pattern, page_text)

        if not paper_match:
            self.logger.warning(f"Could not find paper section for {paper_id}")
            return paper_info

        # Extract text from the match position onwards
        start_pos = paper_match.end()
        remaining_text = page_text[start_pos:]

        # Find the next paper or end of content
        next_paper_pattern = r'[A-Z]{4,}\d+'
        next_match = re.search(next_paper_pattern, remaining_text)

        if next_match:
            paper_content = remaining_text[:next_match.start()]
        else:
            # Look for common end markers
            end_markers = ['DOI:', 'Received:', 'Accepted:', 'Paper:', 'Cite:', 'Export:']
            min_end = len(remaining_text)
            for marker in end_markers:
                marker_pos = remaining_text.find(marker)
                if marker_pos != -1 and marker_pos < min_end:
                    min_end = marker_pos
            paper_content = remaining_text[:min_end] if min_end < len(remaining_text) else remaining_text

        # Parse the paper content
        lines = [line.strip() for line in paper_content.split('\n') if line.strip()]

        # Extract title (usually the first line after paper ID)
        if lines:
            paper_info['title'] = lines[0]

        # Extract page number (look for pattern like "1" or "9")
        page_pattern = r'\b(\d{1,3})\b'
        for line in lines:
            if re.match(r'^\d{1,3}$', line):
                paper_info['page_number'] = line
                break

        # Extract authors and institutions
        author_lines = []
        institution_lines = []
        abstract_lines = []

        in_abstract = False

        for line in lines:
            # Skip title and page number
            if line == paper_info['title'] or line == paper_info['page_number']:
                continue

            # Check for author lines (contain commas and names)
            if ',' in line and len(line.split(',')) > 1 and not any(keyword in line.lower() for keyword in ['funding', 'doi', 'received', 'accepted']):
                author_lines.append(line)
            # Check for institution lines (contain institution keywords)
            elif any(keyword in line for keyword in ['University', 'Laboratory', 'Institute', 'Center', 'Corporation',
                                                   'School', 'Facility', 'National', 'Synchrotron', 'KEK', 'FRIB', 'LBNL',
                                                   'DESY', 'SLAC', 'CERN', 'Jefferson Lab', 'Argonne']):
                institution_lines.append(line)
            # Abstract content (longer lines that are not authors or institutions)
            elif len(line) > 20 and not line.startswith(('Funding:', 'DOI:', 'Received:', 'Accepted:')):
                abstract_lines.append(line)

        # Process authors
        if author_lines:
            all_authors = []
            for author_line in author_lines:
                authors = [a.strip() for a in author_line.split(',') if a.strip()]
                all_authors.extend(authors)
            paper_info['authors'] = all_authors

        # Process institutions
        if institution_lines:
            paper_info['institutions'] = institution_lines

        # Process abstract
        if abstract_lines:
            paper_info['abstract'] = ' '.join(abstract_lines)

        # Check availability of different file types
        paper_info['presentation_available'] = self.check_pdf_exists(paper_info['presentation_url'])
        paper_info['paper_available'] = self.check_pdf_exists(paper_info['paper_url'])
        paper_info['poster_available'] = self.check_pdf_exists(paper_info['poster_url'])

        return paper_info

    def check_pdf_exists(self, pdf_url: str) -> bool:
        """
        Check if PDF file exists and is accessible.

        Args:
            pdf_url: URL of the PDF file

        Returns:
            True if PDF exists and is accessible
        """
        try:
            response = self.session.head(pdf_url, timeout=10)
            return response.status_code == 200 and 'pdf' in response.headers.get('content-type', '').lower()
        except:
            return False

    def scrape_conference(self, conference: Dict[str, str]) -> Dict[str, Any]:
        """
        Scrape all papers from a single conference.

        Args:
            conference: Conference configuration dictionary

        Returns:
            Dictionary containing conference data
        """
        conf_code = conference['code']
        conf_name = conference['name']
        conf_url = conference['url']

        self.logger.info(f"Starting to scrape conference: {conf_name} ({conf_code})")

        # Load sessions for this conference
        sessions = self.load_sessions_for_conference(conference)
        if not sessions:
            self.logger.warning(f"No sessions found for {conf_code}")
            return {'conference': conference, 'sessions': [], 'papers': [], 'error': 'No sessions found'}

        all_papers = []
        session_data = []

        for session in sessions:
            try:
                self.logger.info(f"Processing session: {session['name']}")

                soup = self.get_page_content(session['url'])
                if not soup:
                    continue

                papers = self.extract_papers_from_session(soup, session['id'], conf_code)

                if papers:
                    # Save session data
                    session_dir = self.output_dir / "Conferences" / conf_code / "Sessions" / self.safe_filename(session['name'])
                    session_dir.mkdir(parents=True, exist_ok=True)

                    # JSON format
                    json_file = session_dir / "papers_data.json"
                    session_info = {
                        'session_info': session,
                        'papers': papers,
                        'paper_count': len(papers),
                        'scrape_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }

                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(session_info, f, ensure_ascii=False, indent=2)

                    # Download files for papers in this session
                    for paper in papers:
                        self.download_files(paper, session['name'], conf_code)

                    all_papers.extend(papers)
                    session_data.append(session_info)

                    self.logger.info(f"✅ Session {session['id']} completed: {len(papers)} papers")
                else:
                    self.logger.info(f"⚠️ Session {session['id']} found no papers")

                time.sleep(1)  # Avoid too frequent requests

            except Exception as e:
                self.logger.error(f"❌ Error processing session {session['name']}: {e}")
                self.stats['errors'] += 1
                continue

        # Save conference summary
        self.save_conference_summary(conference, session_data, all_papers)

        self.stats['processed_conferences'] += 1
        self.stats['total_papers'] += len(all_papers)

        self.logger.info(f"✅ Conference {conf_code} completed: {len(all_papers)} papers from {len(session_data)} sessions")

        return {
            'conference': conference,
            'sessions': session_data,
            'papers': all_papers,
            'paper_count': len(all_papers),
            'session_count': len(session_data)
        }

    def download_files(self, paper_info: Dict[str, Any], session_name: str, conf_code: str):
        """
        Download all available files (presentation, paper, poster) for a paper.

        Args:
            paper_info: Paper information dictionary
            session_name: Name of the session
            conf_code: Conference code
        """
        file_types = [
            ('presentation', paper_info['presentation_url'], paper_info['presentation_available'], 'Presentations'),
            ('paper', paper_info['paper_url'], paper_info['paper_available'], 'Papers'),
            ('poster', paper_info['poster_url'], paper_info['poster_available'], 'Posters')
        ]

        for file_type, url, available, folder in file_types:
            if available:
                success = self.download_single_file(url, paper_info, session_name, folder, file_type, conf_code)
                if success:
                    self.stats[f'downloaded_{file_type}s'] += 1

    def download_single_file(self, file_url: str, paper_info: Dict[str, Any], session_name: str, folder: str, file_type: str, conf_code: str) -> bool:
        """
        Download a single file (presentation, paper, or poster).

        Args:
            file_url: URL of the file
            paper_info: Paper information dictionary
            session_name: Name of the session
            folder: Target folder name
            file_type: Type of file (presentation, paper, poster)
            conf_code: Conference code

        Returns:
            True if download successful
        """
        try:
            session_dir = self.output_dir / folder / conf_code / self.safe_filename(session_name)
            session_dir.mkdir(exist_ok=True, parents=True)

            suffix = "_talk" if file_type == "presentation" else ("_poster" if file_type == "poster" else "")
            filename = f"{paper_info['paper_id']}{suffix} - {paper_info['title']}"
            safe_name = self.safe_filename(filename)
            if not safe_name.endswith('.pdf'):
                safe_name += '.pdf'

            filepath = session_dir / safe_name

            if filepath.exists():
                self.logger.info(f"{file_type.title()} already exists, skipping: {safe_name}")
                return True

            response = self.session.get(file_url, stream=True, timeout=60)
            response.raise_for_status()

            content_length = int(response.headers.get('content-length', 0))
            if content_length > 0 and content_length < 100:
                self.logger.warning(f"{file_type.title()} file too small ({content_length} bytes), skipping: {paper_info['paper_id']}")
                return False

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.logger.info(f"✅ Downloaded {file_type}: {safe_name} ({content_length} bytes)")
            return True

        except Exception as e:
            self.logger.error(f"Failed to download {file_type} {file_url}: {e}")
            self.stats['errors'] += 1
            return False

    def save_conference_summary(self, conference: Dict[str, str], session_data: List[Dict], all_papers: List[Dict[str, Any]]):
        """Save conference summary data."""
        conf_code = conference['code']
        conf_dir = self.output_dir / "Conferences" / conf_code
        conf_dir.mkdir(parents=True, exist_ok=True)

        # Conference JSON
        conf_json = conf_dir / "conference_data.json"
        conference_summary = {
            'conference_info': conference,
            'sessions': session_data,
            'all_papers': all_papers,
            'stats': {
                'total_sessions': len(session_data),
                'total_papers': len(all_papers),
                'scrape_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        with open(conf_json, 'w', encoding='utf-8') as f:
            json.dump(conference_summary, f, ensure_ascii=False, indent=2)

        # Conference CSV
        self.save_conference_csv(conf_dir, all_papers, conference)

        # Conference text summary
        self.save_conference_txt(conf_dir, conference, session_data, all_papers)

    def save_conference_csv(self, conf_dir: Path, papers: List[Dict[str, Any]], conference: Dict[str, str]):
        """Save conference data in CSV format."""
        import csv

        csv_file = conf_dir / "all_papers.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            if not papers:
                return

            fieldnames = ['conference_code', 'session_name', 'paper_id', 'title', 'authors', 'institutions',
                         'abstract', 'presentation_url', 'presentation_available', 'paper_url', 'paper_available',
                         'poster_url', 'poster_available', 'doi', 'page_number']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for paper in papers:
                row = {
                    'conference_code': conference['code'],
                    **paper
                }
                row['authors'] = '; '.join(paper['authors'])
                row['institutions'] = '; '.join(paper['institutions'])
                writer.writerow(row)

    def save_conference_txt(self, conf_dir: Path, conference: Dict[str, str], session_data: List[Dict], papers: List[Dict[str, Any]]):
        """Save conference data in text format."""
        txt_file = conf_dir / "conference_summary.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Conference: {conference['name']} ({conference['code']})\n")
            f.write(f"URL: {conference['url']}\n")
            f.write(f"Scrape time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Sessions processed: {len(session_data)}\n")
            f.write(f"Total papers: {len(papers)}\n")

            available_presentations = sum(1 for p in papers if p.get('presentation_available', False))
            available_papers_count = sum(1 for p in papers if p.get('paper_available', False))
            available_posters = sum(1 for p in papers if p.get('poster_available', False))

            f.write(f"Available presentations: {available_presentations}/{len(papers)}\n")
            f.write(f"Available papers: {available_papers_count}/{len(papers)}\n")
            f.write(f"Available posters: {available_posters}/{len(papers)}\n")
            f.write("=" * 80 + "\n\n")

            for session in session_data:
                session_info = session['session_info']
                session_papers = session['papers']
                f.write(f"Session: {session_info['name']}\n")
                f.write(f"  Papers: {len(session_papers)}\n")

                if session_papers:
                    f.write("  Paper list:\n")
                    for paper in session_papers:
                        status = []
                        if paper.get('presentation_available'): status.append('P')
                        if paper.get('paper_available'): status.append('R')
                        if paper.get('poster_available'): status.append('T')
                        status_str = f"[{' '.join(status)}]" if status else "[---]"
                        f.write(f"    {status_str} {paper['paper_id']}: {paper['title'][:60]}...\n")
                f.write("\n")

    def create_master_summary(self, all_conference_data: List[Dict]):
        """
        Create master summary report of all scraped conferences.

        Args:
            all_conference_data: List of all conference data dictionaries
        """
        # Calculate statistics
        total_presentations = sum(
            sum(1 for paper in conf['papers'] if paper.get('presentation_available', False))
            for conf in all_conference_data
        )
        total_papers = sum(
            sum(1 for paper in conf['papers'] if paper.get('paper_available', False))
            for conf in all_conference_data
        )
        total_posters = sum(
            sum(1 for paper in conf['papers'] if paper.get('poster_available', False))
            for conf in all_conference_data
        )

        # Master JSON
        master_json = self.output_dir / "JACoW_Master_Index.json"
        with open(master_json, 'w', encoding='utf-8') as f:
            json.dump({
                'scrape_info': {
                    'scrape_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'total_conferences': self.stats['total_conferences'],
                    'processed_conferences': self.stats['processed_conferences'],
                    'total_papers': self.stats['total_papers'],
                    'available_presentations': total_presentations,
                    'available_papers': total_papers,
                    'available_posters': total_posters,
                    'downloaded_presentations': self.stats['downloaded_presentations'],
                    'downloaded_papers': self.stats['downloaded_papers'],
                    'downloaded_posters': self.stats['downloaded_posters'],
                    'errors': self.stats['errors']
                },
                'conferences': all_conference_data
            }, f, ensure_ascii=False, indent=2)

        # Master CSV
        self.create_master_csv(all_conference_data)

        # Text summary
        summary_file = self.output_dir / "JACoW_Master_Report.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("JACoW Universal Conference Scraper - Master Report\n")
            f.write("=" * 80 + "\n")
            f.write(f"Scrape completion time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total conferences discovered: {self.stats['total_conferences']}\n")
            f.write(f"Conferences processed: {self.stats['processed_conferences']}\n")
            f.write(f"Total papers: {self.stats['total_papers']}\n")
            f.write(f"Available presentations: {total_presentations}\n")
            f.write(f"Available papers: {total_papers}\n")
            f.write(f"Available posters: {total_posters}\n")
            f.write(f"Successfully downloaded presentations: {self.stats['downloaded_presentations']}\n")
            f.write(f"Successfully downloaded papers: {self.stats['downloaded_papers']}\n")
            f.write(f"Successfully downloaded posters: {self.stats['downloaded_posters']}\n")
            f.write(f"Errors: {self.stats['errors']}\n\n")

            f.write("Conference summary:\n")
            f.write("-" * 60 + "\n")
            for conf_data in all_conference_data:
                conf = conf_data['conference']
                papers = conf_data['papers']
                available_presentations = sum(1 for p in papers if p.get('presentation_available', False))
                available_papers_count = sum(1 for p in papers if p.get('paper_available', False))
                available_posters = sum(1 for p in papers if p.get('poster_available', False))

                f.write(f"{conf['code']}: {conf['name']}\n")
                f.write(f"   Papers: {len(papers)}\n")
                f.write(f"   Available presentations: {available_presentations}\n")
                f.write(f"   Available papers: {available_papers_count}\n")
                f.write(f"   Available posters: {available_posters}\n")
                f.write(f"   URL: {conf['url']}\n")
                f.write("\n")

    def create_master_csv(self, all_conference_data: List[Dict]):
        """Create master CSV file containing all papers from all conferences."""
        import csv

        csv_file = self.output_dir / "JACoW_All_Papers.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['conference_code', 'conference_name', 'session_name', 'paper_id', 'title', 'authors', 'institutions',
                         'abstract', 'presentation_url', 'presentation_available', 'paper_url', 'paper_available',
                         'poster_url', 'poster_available', 'doi', 'page_number']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for conf_data in all_conference_data:
                conf = conf_data['conference']
                for paper in conf_data['papers']:
                    row = {
                        'conference_code': conf['code'],
                        'conference_name': conf['name'],
                        **paper
                    }
                    row['authors'] = '; '.join(paper['authors'])
                    row['institutions'] = '; '.join(paper['institutions'])
                    writer.writerow(row)

    def run(self, test_mode: bool = False, max_conferences: int = None, start_from: int = 0):
        """
        Run the main scraping process.

        Args:
            test_mode: If True, only process first few conferences for testing
            max_conferences: Maximum number of conferences to process (None for all)
            start_from: Index to start processing from (for resuming interrupted runs)
        """
        self.logger.info("Starting JACoW universal conference data scraping")
        start_time = time.time()

        try:
            conferences_to_process = self.conferences

            if test_mode:
                conferences_to_process = conferences_to_process[:3]  # Test with first 3 conferences
                self.logger.info("Test mode: processing first 3 conferences")

            if max_conferences:
                conferences_to_process = conferences_to_process[start_from:start_from + max_conferences]
                self.logger.info(f"Limited mode: processing conferences {start_from} to {start_from + max_conferences - 1}")

            self.logger.info(f"Prepared to process {len(conferences_to_process)} conferences")

            all_conference_data = []

            # Process each conference
            for i, conference in enumerate(conferences_to_process, 1):
                global_index = start_from + i
                self.logger.info(f"\n{'='*80}")
                self.logger.info(f"Processing conference {i}/{len(conferences_to_process)} (global {global_index}/149): {conference['name']} ({conference['code']})")

                try:
                    # Check if conference has the expected structure
                    if not self.check_conference_structure(conference['url']):
                        self.logger.warning(f"Conference {conference['code']} does not follow expected structure, skipping")
                        continue

                    conference_data = self.scrape_conference(conference)

                    if conference_data and conference_data['papers']:
                        all_conference_data.append(conference_data)
                        self.logger.info(f"✅ Conference {conference['code']} completed successfully")
                    else:
                        self.logger.warning(f"⚠️ Conference {conference['code']} found no papers")

                    time.sleep(2)  # Rest between conferences

                except Exception as e:
                    self.logger.error(f"❌ Critical error processing conference {conference['code']}: {e}")
                    self.stats['errors'] += 1
                    continue

            # Create master summary
            self.create_master_summary(all_conference_data)

            elapsed_time = time.time() - start_time
            self.logger.info(f"\n🎉 Scraping completed! Time elapsed: {elapsed_time:.2f} seconds")
            self.logger.info(f"📊 Final statistics:")
            self.logger.info(f"  ✅ Conferences processed: {self.stats['processed_conferences']}/{self.stats['total_conferences']}")
            self.logger.info(f"  📄 Total papers: {self.stats['total_papers']}")
            self.logger.info(f"  📊 Presentations downloaded: {self.stats['downloaded_presentations']}")
            self.logger.info(f"  📄 Papers downloaded: {self.stats['downloaded_papers']}")
            self.logger.info(f"  📋 Posters downloaded: {self.stats['downloaded_posters']}")
            self.logger.info(f"  ❌ Errors: {self.stats['errors']}")

            return all_conference_data

        except Exception as e:
            self.logger.error(f"Critical error during scraping process: {e}")
            raise


def main():
    """Main function to run the JACoW scraper."""
    print("JACoW Universal Conference Web Scraper")
    print("=" * 80)
    print("Comprehensive scraper for all JACoW conference papers")
    print("Author: Ming Liu")
    print()
    print("Found 149 JACoW conferences ready for scraping")
    print()

    scraper = JACoWScraper()

    try:
        print("Choose scraping mode:")
        print("  t - Test mode (first 3 conferences)")
        print("  l - Limited mode (10 conferences)")
        print("  b - Batch mode (process in batches of 20)")
        print("  a - All conferences (149 total - may take several hours)")
        print()

        choice = input("Enter your choice (t/l/b/a): ").lower().strip()

        if choice == 't':
            print("\nStarting test mode (3 conferences)...")
            results = scraper.run(test_mode=True)
        elif choice == 'l':
            print("\nStarting limited mode (10 conferences)...")
            results = scraper.run(test_mode=False, max_conferences=10)
        elif choice == 'b':
            print("\nStarting batch mode...")
            batch_size = 20
            total_conferences = len(scraper.conferences)
            batches = (total_conferences + batch_size - 1) // batch_size

            print(f"Total conferences: {total_conferences}")
            print(f"Batch size: {batch_size}")
            print(f"Number of batches: {batches}")
            print()

            start_batch = input(f"Enter starting batch number (1-{batches}): ").strip()
            try:
                start_batch = int(start_batch) - 1  # Convert to 0-based index
                if start_batch < 0 or start_batch >= batches:
                    print("Invalid batch number. Exiting...")
                    return

                start_index = start_batch * batch_size
                end_index = min(start_index + batch_size, total_conferences)
                actual_batch_size = end_index - start_index

                print(f"\nProcessing batch {start_batch + 1}/{batches}: conferences {start_index + 1}-{end_index}")
                print(f"Conferences in this batch: {actual_batch_size}")
                confirm = input("\nContinue? (yes/no): ").lower().strip()

                if confirm == 'yes':
                    results = scraper.run(test_mode=False, max_conferences=actual_batch_size, start_from=start_index)
                else:
                    print("\nCancelled. Exiting...")
                    return

            except ValueError:
                print("Invalid input. Exiting...")
                return

        elif choice == 'a':
            print("\n⚠️  WARNING: This will scrape ALL 149 JACoW conferences!")
            print("   Estimated time: 4-8 hours depending on connection speed")
            print("   Estimated data: 10,000+ papers, 50GB+ of PDFs")
            confirm = input("\nAre you sure you want to continue? (yes/no): ").lower().strip()
            if confirm == 'yes':
                print("\n🚀 Starting full scraping of all 149 conferences...")
                results = scraper.run(test_mode=False)
            else:
                print("\nCancelled. Exiting...")
                return
        else:
            print("\nInvalid choice. Exiting...")
            return

        if choice in ['t', 'l', 'a']:
            print("\n" + "="*80)
            print("Scraping completed successfully!")
            print(f"Output directory: {scraper.output_dir}")
            print("\nMain output files:")
            print("  📊 JACoW_Master_Report.txt - Complete scraping report")
            print("  📈 JACoW_All_Papers.csv - All papers from all conferences")
            print("  🗂️ JACoW_Master_Index.json - Complete data index")
            print("  📁 Conferences/ - Conference-organized detailed data")
            print("  📊 Presentations/ - Downloaded presentation files")
            print("  📁 Papers/ - Downloaded paper files")
            print("  📁 Posters/ - Downloaded poster files")
            print("  🔍 Debug/ - Debug information and page content")

    except KeyboardInterrupt:
        print("\n⏹️ User interrupted scraping")
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")


if __name__ == "__main__":
    main()