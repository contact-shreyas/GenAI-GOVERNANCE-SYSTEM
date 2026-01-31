#!/usr/bin/env python3
"""
Count pages in PDF
Usage: python count_pages.py main.pdf
"""

import sys
from pathlib import Path

def count_pdf_pages(pdf_file):
    """Count pages in PDF using PyPDF2"""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("Error: PyPDF2 not installed. Run: pip install PyPDF2")
        return None
    
    try:
        reader = PdfReader(pdf_file)
        return len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_pages.py main.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    if not Path(pdf_file).exists():
        print(f"Error: {pdf_file} not found")
        sys.exit(1)
    
    pages = count_pdf_pages(pdf_file)
    if pages is not None:
        print(f"\n📄 Page count: {pages} pages")
        
        if pages == 9:
            print("✅ PERFECT! Exactly 9 pages.")
        elif pages < 9:
            print(f"⚠️  TOO SHORT: Need {9 - pages} more page(s)")
            print("   → Add content: expand evaluation, add limitations, more related work")
        else:
            print(f"⚠️  TOO LONG: Need to remove {pages - 9} page(s)")
            print("   → Tighten: condense related work, merge discussion into results")
        print()

if __name__ == '__main__':
    main()
