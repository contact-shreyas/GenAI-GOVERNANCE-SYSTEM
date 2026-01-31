#!/usr/bin/env python3
"""
Verify PDF is exactly 9 pages (strict check for submission)
Usage: python verify_9pages.py main.pdf
"""

import sys
from pathlib import Path

def count_pdf_pages(pdf_file):
    """Count pages in PDF"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_file)
        return len(reader.pages)
    except ImportError:
        print("Error: PyPDF2 not installed. Run: pip install PyPDF2")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_9pages.py main.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    if not Path(pdf_file).exists():
        print(f"Error: {pdf_file} not found")
        sys.exit(1)
    
    pages = count_pdf_pages(pdf_file)
    
    print("\n" + "="*80)
    print("PAGE COUNT VERIFICATION")
    print("="*80)
    print(f"File: {pdf_file}")
    print(f"Pages: {pages}")
    print("="*80)
    
    if pages == 9:
        print("✅ SUCCESS: Paper is exactly 9 pages!")
        print("="*80)
        sys.exit(0)
    else:
        print(f"❌ FAILURE: Paper is {pages} pages (required: 9 pages exactly)")
        if pages < 9:
            print(f"   Need to ADD {9 - pages} page(s)")
        else:
            print(f"   Need to REMOVE {pages - 9} page(s)")
        print("="*80)
        sys.exit(1)

if __name__ == '__main__':
    main()
