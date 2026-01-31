#!/usr/bin/env python3
"""GitHub Upload Script - Direct Execution"""
import subprocess
import sys
import os

# Change to project directory
os.chdir(r"C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION")

print("\n" + "=" * 80)
print("GenAI GOVERNANCE SYSTEM - GITHUB UPLOAD")
print("=" * 80 + "\n")

# Try to find git in common locations
git_paths = [
    "git",  # System PATH
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
]

git_cmd = None
for path in git_paths:
    try:
        result = subprocess.run([path, "--version"], capture_output=True, timeout=2)
        if result.returncode == 0:
            git_cmd = path
            print(f"✓ Found Git: {path}\n")
            break
    except:
        pass

if not git_cmd:
    print("✗ Git not found in system PATH")
    print("\nPlease install Git from: https://git-scm.com/download/win")
    sys.exit(1)

# Git commands to execute
commands = [
    (f'"{git_cmd}" init', "Initialize repository"),
    (f'"{git_cmd}" config user.name "contact-shreyas"', "Set username"),
    (f'"{git_cmd}" config user.email "governance@example.com"', "Set email"),
    (f'"{git_cmd}" add .', "Stage all files"),
    (f'"{git_cmd}" commit -m "Add: GenAI Governance System - Paper, Code, Datasets, Tests"', "Create commit"),
    (f'"{git_cmd}" remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git', "Add remote"),
    (f'"{git_cmd}" branch -M main', "Set main branch"),
    (f'"{git_cmd}" push -u origin main', "Push to GitHub"),
]

# Execute each command
failed = False
for i, (cmd, description) in enumerate(commands, 1):
    print(f"[{i}/{len(commands)}] {description}...")
    print(f"  Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"  ✓ SUCCESS")
            if result.stdout:
                # Show first 2 lines of output
                lines = result.stdout.strip().split('\n')[:2]
                for line in lines:
                    print(f"    {line}")
        else:
            print(f"  ⚠ Output: {result.stderr[:150] if result.stderr else result.stdout[:150]}")
            
            # Some errors are non-fatal (like remote already exists)
            if "fatal" in result.stderr.lower() and i >= 6:
                failed = True
                break
    
    except subprocess.TimeoutExpired:
        print(f"  ✗ TIMEOUT (waiting for credentials)")
        print(f"  → When prompted, enter:")
        print(f"     Username: contact-shreyas")
        print(f"     Password: [Your PAT token]")
        failed = True
        break
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        failed = True
        break
    
    print()

# Final message
print("=" * 80)
if not failed:
    print("✓ UPLOAD COMPLETE!")
    print("\nRepository: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM")
    print("\nVisit the URL above to verify all files are uploaded.")
else:
    print("⚠ Upload may require manual credentials")
    print("\nIf you were prompted for credentials:")
    print("  Username: contact-shreyas")
    print("  Password: [Paste your GitHub PAT token]")
    print("\nVisit: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM")

print("=" * 80 + "\n")
