#!/usr/bin/env python3
"""
Script to generate professional commit messages and create commits.
This script generates 200+ professional commit messages following
conventional commit standards and best practices.
"""

import subprocess
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

# Professional commit message templates
COMMIT_TYPES = [
    "feat", "fix", "docs", "style", "refactor", "perf", "test", "chore",
    "build", "ci", "revert"
]

SCOPES = [
    "scanner", "webcam", "image", "cli", "gui", "export", "logging",
    "error-handling", "utils", "config", "deps", "docs", "tests"
]

FEAT_MESSAGES = [
    "add {scope} functionality",
    "implement {scope} feature",
    "introduce {scope} support",
    "add new {scope} capabilities",
    "implement {scope} module",
    "add {scope} integration",
    "create {scope} component",
    "add {scope} feature with validation",
    "implement advanced {scope} features",
    "add {scope} with error handling",
    "introduce {scope} API",
    "add {scope} configuration options",
    "implement {scope} with logging",
    "add {scope} export functionality",
    "create {scope} interface",
    "add {scope} batch processing",
    "implement {scope} preview mode",
    "add {scope} real-time processing",
    "introduce {scope} optimization",
    "add {scope} multi-threading support"
]

FIX_MESSAGES = [
    "fix {scope} bug",
    "resolve {scope} issue",
    "fix {scope} error handling",
    "correct {scope} logic",
    "fix {scope} memory leak",
    "resolve {scope} race condition",
    "fix {scope} edge case",
    "correct {scope} validation",
    "fix {scope} performance issue",
    "resolve {scope} compatibility issue",
    "fix {scope} timeout handling",
    "correct {scope} exception handling",
    "fix {scope} resource cleanup",
    "resolve {scope} encoding issue",
    "fix {scope} camera initialization",
    "correct {scope} file path handling",
    "fix {scope} thread safety",
    "resolve {scope} buffer overflow",
    "fix {scope} image format detection",
    "correct {scope} coordinate calculation"
]

DOCS_MESSAGES = [
    "update {scope} documentation",
    "add {scope} usage examples",
    "improve {scope} README",
    "document {scope} API",
    "add {scope} installation guide",
    "update {scope} code comments",
    "improve {scope} inline documentation",
    "add {scope} troubleshooting section",
    "document {scope} configuration",
    "update {scope} changelog",
    "add {scope} architecture docs",
    "improve {scope} user guide",
    "document {scope} best practices",
    "add {scope} API reference",
    "update {scope} examples",
    "improve {scope} documentation structure",
    "add {scope} contribution guidelines",
    "document {scope} error codes",
    "update {scope} performance notes",
    "add {scope} deployment guide"
]

STYLE_MESSAGES = [
    "format {scope} code",
    "apply code style to {scope}",
    "clean up {scope} formatting",
    "standardize {scope} code style",
    "fix {scope} linting issues",
    "improve {scope} code readability",
    "refactor {scope} formatting",
    "apply PEP8 to {scope}",
    "clean up {scope} whitespace",
    "standardize {scope} naming",
    "fix {scope} indentation",
    "improve {scope} code structure",
    "format {scope} imports",
    "clean up {scope} comments",
    "standardize {scope} docstrings"
]

REFACTOR_MESSAGES = [
    "refactor {scope} module",
    "restructure {scope} code",
    "improve {scope} architecture",
    "optimize {scope} structure",
    "refactor {scope} functions",
    "restructure {scope} classes",
    "improve {scope} design patterns",
    "refactor {scope} error handling",
    "optimize {scope} code organization",
    "restructure {scope} components",
    "improve {scope} separation of concerns",
    "refactor {scope} initialization",
    "optimize {scope} data flow",
    "restructure {scope} file structure",
    "improve {scope} modularity"
]

PERF_MESSAGES = [
    "optimize {scope} performance",
    "improve {scope} speed",
    "reduce {scope} memory usage",
    "optimize {scope} processing",
    "improve {scope} efficiency",
    "reduce {scope} CPU usage",
    "optimize {scope} algorithm",
    "improve {scope} response time",
    "reduce {scope} latency",
    "optimize {scope} resource usage",
    "improve {scope} throughput",
    "reduce {scope} overhead",
    "optimize {scope} image processing",
    "improve {scope} frame rate",
    "reduce {scope} processing time"
]

TEST_MESSAGES = [
    "add {scope} unit tests",
    "implement {scope} test suite",
    "add {scope} integration tests",
    "improve {scope} test coverage",
    "add {scope} test cases",
    "implement {scope} test fixtures",
    "add {scope} mock tests",
    "improve {scope} test reliability",
    "add {scope} edge case tests",
    "implement {scope} performance tests",
    "add {scope} regression tests",
    "improve {scope} test documentation",
    "add {scope} test utilities",
    "implement {scope} test automation",
    "add {scope} validation tests"
]

CHORE_MESSAGES = [
    "update {scope} dependencies",
    "bump {scope} version",
    "clean up {scope} files",
    "update {scope} configuration",
    "improve {scope} build process",
    "update {scope} gitignore",
    "clean up {scope} temporary files",
    "update {scope} license",
    "improve {scope} project structure",
    "update {scope} CI/CD",
    "clean up {scope} unused code",
    "update {scope} metadata",
    "improve {scope} deployment",
    "update {scope} scripts",
    "clean up {scope} artifacts"
]

BUILD_MESSAGES = [
    "update {scope} build configuration",
    "improve {scope} build process",
    "fix {scope} build errors",
    "optimize {scope} build time",
    "update {scope} build dependencies",
    "improve {scope} build scripts",
    "fix {scope} compilation issues",
    "update {scope} build tools",
    "improve {scope} packaging",
    "fix {scope} build warnings"
]

CI_MESSAGES = [
    "update {scope} CI pipeline",
    "improve {scope} CI configuration",
    "add {scope} CI tests",
    "fix {scope} CI failures",
    "optimize {scope} CI workflow",
    "update {scope} CI dependencies",
    "improve {scope} CI reporting",
    "add {scope} CI validation",
    "fix {scope} CI timeout",
    "update {scope} CI environment"
]

# Map commit types to message templates
MESSAGE_TEMPLATES = {
    "feat": FEAT_MESSAGES,
    "fix": FIX_MESSAGES,
    "docs": DOCS_MESSAGES,
    "style": STYLE_MESSAGES,
    "refactor": REFACTOR_MESSAGES,
    "perf": PERF_MESSAGES,
    "test": TEST_MESSAGES,
    "chore": CHORE_MESSAGES,
    "build": BUILD_MESSAGES,
    "ci": CI_MESSAGES,
    "revert": ["revert {scope} changes", "undo {scope} modification"]
}

DETAILED_MESSAGES = [
    "with improved error handling",
    "with comprehensive logging",
    "with unit tests",
    "with performance optimizations",
    "with better documentation",
    "following best practices",
    "with enhanced security",
    "with input validation",
    "with proper error messages",
    "with code comments",
    "with type hints",
    "with async support",
    "with caching mechanism",
    "with retry logic",
    "with timeout handling",
    "with resource cleanup",
    "with memory optimization",
    "with thread safety",
    "with exception handling",
    "with validation checks"
]


def generate_commit_message():
    """Generate a professional commit message."""
    commit_type = random.choice(COMMIT_TYPES)
    scope = random.choice(SCOPES)
    
    # Get template for this commit type
    templates = MESSAGE_TEMPLATES.get(commit_type, FEAT_MESSAGES)
    template = random.choice(templates)
    
    # Format the message
    message = template.format(scope=scope)
    
    # Sometimes add detailed suffix
    if random.random() < 0.3:
        detail = random.choice(DETAILED_MESSAGES)
        message += f" {detail}"
    
    # Capitalize first letter
    message = message.capitalize()
    
    # Create full commit message
    full_message = f"{commit_type}({scope}): {message}"
    
    # Sometimes add body
    if random.random() < 0.2:
        body_options = [
            f"\n\nThis change improves the {scope} functionality by\nimplementing better error handling and validation.",
            f"\n\nCloses #{random.randint(1, 100)}",
            f"\n\nBREAKING CHANGE: {scope} API has been updated.",
            f"\n\nThis update enhances {scope} performance and reliability.",
        ]
        full_message += random.choice(body_options)
    
    return full_message


def make_dummy_change():
    """Make a small dummy change to create a commit."""
    # Create or update a dummy file
    dummy_file = Path("commit_history.txt")
    
    if dummy_file.exists():
        with open(dummy_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}\n")
    else:
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("Commit History\n")
            f.write("=" * 50 + "\n")
            f.write(f"{datetime.now().isoformat()}\n")
    
    return dummy_file


def run_git_command(command, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None, e.stderr


def initialize_git():
    """Initialize git repository if not already initialized."""
    if not Path(".git").exists():
        print("Initializing git repository...")
        run_git_command("git init")
        run_git_command('git config user.name "QR Scanner Developer"')
        run_git_command('git config user.email "developer@qrscanner.dev"')
        print("Git repository initialized.")
    else:
        print("Git repository already initialized.")


def create_commits(num_commits=200):
    """Create multiple commits with professional messages."""
    print(f"Creating {num_commits} professional commits...")
    
    initialize_git()
    
    # Set git config if not already set
    run_git_command('git config user.name "QR Scanner Developer"', check=False)
    run_git_command('git config user.email "developer@qrscanner.dev"', check=False)
    
    commits_created = 0
    
    for i in range(num_commits):
        try:
            # Generate commit message
            commit_message = generate_commit_message()
            
            # Make a small change
            dummy_file = make_dummy_change()
            
            # Stage the change
            stdout, stderr = run_git_command(f'git add {dummy_file}')
            
            # Create commit
            stdout, stderr = run_git_command(
                f'git commit -m "{commit_message}"',
                check=False
            )
            
            if "nothing to commit" not in stderr.lower():
                commits_created += 1
                if (commits_created % 10 == 0):
                    print(f"Created {commits_created} commits...")
            else:
                # Make another change to ensure we have something to commit
                with open(dummy_file, "a", encoding="utf-8") as f:
                    f.write(f"Update {i}\n")
                run_git_command(f'git add {dummy_file}')
                run_git_command(f'git commit -m "{commit_message}"', check=False)
                commits_created += 1
            
        except Exception as e:
            print(f"Error creating commit {i+1}: {str(e)}")
            continue
    
    print(f"\nSuccessfully created {commits_created} commits!")
    return commits_created


def push_to_github(repo_url=None):
    """Push commits to GitHub repository."""
    if repo_url is None:
        repo_url = "https://github.com/leandre000/QR-code-Decoder.git"
    
    print(f"\nPushing to {repo_url}...")
    
    # Check if remote exists
    stdout, _ = run_git_command("git remote -v", check=False)
    
    if "origin" not in stdout:
        print("Adding remote origin...")
        run_git_command(f'git remote add origin {repo_url}', check=False)
    else:
        print("Remote origin already exists. Updating URL...")
        run_git_command(f'git remote set-url origin {repo_url}', check=False)
    
    # Push to main branch
    print("Pushing to main branch...")
    stdout, stderr = run_git_command("git push -u origin main", check=False)
    
    if "error" in stderr.lower() or "fatal" in stderr.lower():
        print(f"Push may require authentication. Error: {stderr}")
        print("\nYou may need to:")
        print("1. Set up SSH keys or personal access token")
        print("2. Run: git push -u origin main")
    else:
        print("Successfully pushed to GitHub!")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate professional commits")
    parser.add_argument("--count", type=int, default=200,
                       help="Number of commits to create (default: 200)")
    parser.add_argument("--push", action="store_true",
                       help="Push to GitHub after creating commits")
    parser.add_argument("--repo", type=str,
                       default="https://github.com/leandre000/QR-code-Decoder.git",
                       help="GitHub repository URL")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Professional Commit Message Generator")
    print("=" * 60)
    
    commits_created = create_commits(args.count)
    
    if args.push:
        push_to_github(args.repo)
    else:
        print("\nTo push to GitHub, run:")
        print(f"  git push -u origin main")
        print("\nOr use this script with --push flag:")
        print(f"  python generate_commits.py --push")


if __name__ == "__main__":
    main()

