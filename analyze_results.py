#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SRF2017 Scraping Results Analysis and Report Generator

Author: Ming Liu
Description: Analyzes and generates summary reports from SRF2017 scraping results.
             Creates detailed statistics and CSV summaries for scraped conference data.
"""
import json
import os
from pathlib import Path

def analyze_results():
    results_dir = Path("SRF2017_Data")
    sessions_dir = results_dir / "Sessions"
    
    print("🎯 SRF2017 Conference Scraping Results Analysis")
    print("=" * 60)
    
    if not sessions_dir.exists():
        print("❌ Results directory does not exist")
        return
    
    total_papers = 0
    total_available_pdfs = 0
    session_stats = []
    
    # Analyze each Session
    for session_folder in sessions_dir.iterdir():
        if session_folder.is_dir():
            json_file = session_folder / "papers_data.json"
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                papers = data['papers']
                available_pdfs = sum(1 for p in papers if p.get('pdf_available', False))
                
                session_stats.append({
                    'name': data['session_info']['name'],
                    'paper_count': len(papers),
                    'available_pdfs': available_pdfs,
                    'papers': papers
                })
                
                total_papers += len(papers)
                total_available_pdfs += available_pdfs
    
    # Sort and display results
    session_stats.sort(key=lambda x: x['name'])
    
    print(f"📊 Overall Statistics:")
    print(f"  ✅ Sessions processed: {len(session_stats)}")
    print(f"  📄 Total papers: {total_papers}")
    print(f"  💾 Available PDFs: {total_available_pdfs}")
    print()
    
    print("📋 Detailed Session Results:")
    print("-" * 50)
    
    for session in session_stats:
        print(f"📂 {session['name']}")
        print(f"   📄 Paper count: {session['paper_count']}")
        print(f"   💾 Available PDFs: {session['available_pdfs']}")
        
        if session['papers']:
            print("   📝 Paper list:")
            for i, paper in enumerate(session['papers'], 1):
                pdf_icon = "📄" if paper.get('pdf_available', False) else "❌"
                title = paper['title'][:60] + "..." if len(paper['title']) > 60 else paper['title']
                print(f"     {pdf_icon} {paper['paper_id']}: {title}")
                
                # Show abstract preview
                if paper.get('abstract'):
                    abstract_preview = paper['abstract'][:100] + "..." if len(paper['abstract']) > 100 else paper['abstract']
                    print(f"        Abstract: {abstract_preview}")
        print()
    
    # Generate CSV summary
    print("📈 Generating CSV summary file...")
    csv_summary = results_dir / "Sessions_Summary.csv"
    with open(csv_summary, 'w', encoding='utf-8-sig') as f:
        f.write("Session Name,Paper Count,Available PDFs,Paper ID List\n")
        for session in session_stats:
            paper_ids = '; '.join([p['paper_id'] for p in session['papers']])
            f.write(f'"{session["name"]}",{session["paper_count"]},{session["available_pdfs"]},"{paper_ids}"\n')
    
    print(f"✅ CSV summary saved to: {csv_summary}")
    
    # Check PDF download status
    presentations_dir = results_dir / "Presentations"
    papers_dir = results_dir / "Papers"
    posters_dir = results_dir / "Posters"
    
    if presentations_dir.exists() or papers_dir.exists() or posters_dir.exists():
        print("\n📁 PDF Download Status:")
        
        for pdf_base_dir in [presentations_dir, papers_dir, posters_dir]:
            if pdf_base_dir.exists():
                dir_name = pdf_base_dir.name
                total_files = 0
                for session_dir in pdf_base_dir.iterdir():
                    if session_dir.is_dir():
                        pdf_files = list(session_dir.glob("*.pdf"))
                        if pdf_files:
                            print(f"  📂 {dir_name}/{session_dir.name}: {len(pdf_files)} PDF files")
                            total_files += len(pdf_files)
                
                print(f"  📊 Total {dir_name}: {total_files} files")

if __name__ == "__main__":
    analyze_results()