#!/usr/bin/env python3
"""
Count words per section in LaTeX document
Usage: python count_words.py main.tex
"""

import re
import sys
from pathlib import Path

def strip_latex_commands(text):
    """Remove LaTeX commands for word counting"""
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
    # Remove citations
    text = re.sub(r'\\cite\{[^}]+\}', '', text)
    text = re.sub(r'\\ref\{[^}]+\}', '', text)
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    # Remove commands
    text = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?', '', text)
    # Remove math
    text = re.sub(r'\$[^$]+\$', '', text)
    text = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', '', text, flags=re.DOTALL)
    # Remove figures/tables
    text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '', text, flags=re.DOTALL)
    return text

def count_words(text):
    """Count words in text"""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_sections(tex_file):
    """Extract sections from LaTeX file"""
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    abstract = abstract_match.group(1) if abstract_match else ""
    
    # Find sections
    section_pattern = r'\\section\{([^}]+)\}(.*?)(?=\\section|\\bibliographystyle|\\end\{document\})'
    sections = re.findall(section_pattern, content, re.DOTALL)
    
    return abstract, sections

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_words.py main.tex")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    if not Path(tex_file).exists():
        print(f"Error: {tex_file} not found")
        sys.exit(1)
    
    abstract, sections = extract_sections(tex_file)
    
    print("\n" + "="*80)
    print("WORD COUNT PER SECTION")
    print("="*80)
    
    # Count abstract
    abstract_clean = strip_latex_commands(abstract)
    abstract_words = count_words(abstract_clean)
    print(f"{'Abstract':<30} {abstract_words:>6} words")
    
    # Count sections
    total_words = abstract_words
    for title, content in sections:
        content_clean = strip_latex_commands(content)
        words = count_words(content_clean)
        total_words += words
        print(f"{title:<30} {words:>6} words")
    
    print("="*80)
    print(f"{'TOTAL (main content)':<30} {total_words:>6} words")
    print("="*80)
    
    # Estimate references word count (60 refs @ ~40 words each)
    refs_estimate = 60 * 40
    print(f"{'References (estimated)':<30} {refs_estimate:>6} words")
    print(f"{'GRAND TOTAL (estimated)':<30} {total_words + refs_estimate:>6} words")
    print("="*80)
    
    # Estimate pages (IEEE 2-column: ~900 words/page)
    pages_estimate = (total_words + refs_estimate) / 900
    print(f"\nEstimated pages (IEEE 2-col @ 900 words/page): {pages_estimate:.1f} pages")
    print()

if __name__ == '__main__':
    main()
