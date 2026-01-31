#!/usr/bin/env python3
import subprocess
import os

os.chdir(r"C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION")

commands = [
    ("git init", "Initialize repository"),
    ('git config user.name "GenAI Governance"', "Set username"),
    ('git config user.email "governance@example.com"', "Set email"),
    ("git add .", "Add all files"),
    ('git commit -m "Add: GenAI Governance System - Paper, Code, Datasets"', "Commit files"),
    ("git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git", "Add remote"),
    ("git branch -M main", "Set main branch"),
    ("git push -u origin main", "Push to GitHub"),
]

print("=" * 70)
print("GitHub Upload - GenAI Governance System")
print("=" * 70)

for i, (cmd, desc) in enumerate(commands, 1):
    print(f"\n[{i}/{len(commands)}] {desc}")
    print(f"Running: {cmd}\n")
    subprocess.run(cmd, shell=True)

print("\n" + "=" * 70)
print("✓ Upload Complete!")
print("=" * 70)
print("\nRepository: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM")
