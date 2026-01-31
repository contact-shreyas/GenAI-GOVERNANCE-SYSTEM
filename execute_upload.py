#!/usr/bin/env python3
import subprocess
import os
import sys

os.chdir(r"C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION")

print("=" * 70)
print("GITHUB UPLOAD - GenAI Governance System")
print("=" * 70)

commands = [
    ("git init", "Initialize Git repository"),
    ("git config user.name \"contact-shreyas\"", "Configure username"),
    ("git config user.email \"governance@example.com\"", "Configure email"),
    ("git add .", "Stage all files"),
    ("git commit -m \"Add: GenAI Governance System - Paper, Code, Datasets, Tests\"", "Create commit"),
    ("git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git", "Add remote"),
    ("git branch -M main", "Rename branch to main"),
    ("git push -u origin main", "Push to GitHub"),
]

for i, (cmd, desc) in enumerate(commands, 1):
    print(f"\n[{i}/{len(commands)}] {desc}")
    print(f"    Command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"    ✓ Success")
        if result.stdout:
            for line in result.stdout.strip().split('\n')[:3]:
                print(f"      {line}")
    else:
        print(f"    Output: {result.stderr[:200] if result.stderr else result.stdout[:200]}")

print("\n" + "=" * 70)
print("UPLOAD COMPLETE!")
print("=" * 70)
print(f"\nRepository: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM")
print(f"\nVisit the URL above to verify all files are uploaded.\n")
