#!/usr/bin/env python3
"""
Simple Git uploader - executes git commands directly
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command and report results"""
    print(f"\n[*] {description}")
    print(f"    Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    ✓ Success")
            if result.stdout:
                print(f"    {result.stdout[:200]}")
        else:
            print(f"    ✗ Failed: {result.stderr[:200]}")
        return result.returncode == 0
    except Exception as e:
        print(f"    ✗ Error: {str(e)}")
        return False

def main():
    project_dir = r"C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"
    os.chdir(project_dir)
    
    print("=" * 60)
    print("GitHub Upload Script")
    print("=" * 60)
    
    # Check if git is available
    result = subprocess.run("where git", shell=True, capture_output=True)
    if result.returncode != 0:
        print("\n✗ Git is not installed!")
        print("  Download from: https://git-scm.com/download/win")
        sys.exit(1)
    
    print(f"\n✓ Git found: {result.stdout.decode().strip()}")
    
    # Step 1: Initialize git (if needed)
    if not os.path.exists(".git"):
        run_command("git init", "Step 1/6: Initializing repository")
    else:
        print("\n[*] Step 1/6: Repository already initialized")
    
    # Step 2: Configure git user
    run_command('git config user.name "GenAI Governance"', "Step 2/6: Setting git username")
    run_command('git config user.email "governance@example.com"', "Step 2/6: Setting git email")
    
    # Step 3: Add files
    run_command("git add .", "Step 3/6: Adding all files")
    
    # Step 4: Check status before commit
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    files_to_commit = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    print(f"\n[*] Step 4/6: Files ready to commit: {files_to_commit}")
    
    # Step 5: Commit
    if files_to_commit > 0:
        run_command('git commit -m "Add: GenAI Governance System - Paper, Code, Datasets"', 
                   "Step 5/6: Creating commit")
    else:
        print("\n[*] Step 5/6: No new files to commit")
    
    # Step 6: Setup remote and push
    print("\n[*] Step 6/6: Setting up remote and pushing")
    
    # Remove old remote if exists
    subprocess.run("git remote remove origin", shell=True, capture_output=True)
    
    # Add remote
    run_command("git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git",
               "Adding remote repository")
    
    # Set default branch
    subprocess.run("git branch -M main", shell=True, capture_output=True)
    
    # Push to GitHub
    print("\n[!] Pushing to GitHub...")
    print("    You will be prompted for credentials:")
    print("    Username: contact-shreyas")
    print("    Password: [Paste your GitHub PAT token]")
    print()
    
    result = subprocess.run("git push -u origin main", shell=True)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ SUCCESS! Files uploaded to GitHub")
        print("=" * 60)
        print("\nRepository: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM")
        print("\nYour project is now public!")
    else:
        print("\n" + "=" * 60)
        print("✗ Upload may have failed")
        print("=" * 60)
        print("\nPossible issues:")
        print("1. Token doesn't have 'repo' scope")
        print("2. Repository doesn't exist yet")
        print("3. Wrong credentials provided")

if __name__ == "__main__":
    main()
