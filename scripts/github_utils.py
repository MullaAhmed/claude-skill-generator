#!/usr/bin/env python3
"""
GitHub Repository Utilities for github-to-skill plugin.

Provides deterministic functions for:
- Parsing and validating GitHub URLs
- Verifying repository existence via GitHub API
- Converting GitHub URLs to Codewiki URLs

Usage:
    python github_utils.py parse <github_url>
    python github_utils.py verify <github_url>
    python github_utils.py codewiki <github_url>
    python github_utils.py full <github_url>
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from typing import Optional
from dataclasses import dataclass, asdict


def parse_env_file(filepath: str) -> dict:
    """Parse a .env file and return key-value pairs."""
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    env_vars[key] = value
    except IOError:
        pass
    return env_vars


def get_github_token() -> Optional[str]:
    """
    Get GitHub token from multiple sources.

    Priority:
    1. .claude/config.json
    2. .env file in working directory
    3. Environment variable (GITHUB_TOKEN)

    Returns:
        Token string or None if not found
    """
    # Check .claude/config.json
    config_path = '.claude/config.json'
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                token = config.get('github_token', '')
                if token and token.strip():
                    return token.strip()
        except (json.JSONDecodeError, IOError):
            pass

    # Check .env file
    env_vars = parse_env_file('.env')
    if 'GITHUB_TOKEN' in env_vars:
        token = env_vars['GITHUB_TOKEN']
        if token and token.strip():
            return token.strip()

    # Check environment variable
    env_token = os.environ.get('GITHUB_TOKEN', '')
    if env_token and env_token.strip():
        return env_token.strip()

    return None


@dataclass
class ParsedGitHubURL:
    """Parsed components of a GitHub repository URL."""
    owner: str
    repo: str
    original_url: str
    normalized_url: str


@dataclass
class RepoMetadata:
    """Metadata from GitHub API response."""
    full_name: str
    description: Optional[str]
    default_branch: str
    topics: list
    license: Optional[str]
    homepage: Optional[str]
    stargazers_count: int
    fork: bool
    archived: bool
    language: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class VerificationResult:
    """Result of GitHub repository verification."""
    success: bool
    parsed: Optional[ParsedGitHubURL]
    metadata: Optional[RepoMetadata]
    codewiki_url: Optional[str]
    error: Optional[str]


def parse_github_url(url: str) -> tuple[Optional[ParsedGitHubURL], Optional[str]]:
    """
    Parse and validate a GitHub repository URL.

    Args:
        url: GitHub URL to parse (e.g., https://github.com/juliangarnier/anime)

    Returns:
        Tuple of (ParsedGitHubURL or None, error message or None)

    Supports formats:
        - https://github.com/juliangarnier/anime
        - https://github.com/juliangarnier/anime/
        - https://github.com/juliangarnier/anime.git
        - http://github.com/owner/repo
        - github.com/owner/repo
    """
    if not url or not isinstance(url, str):
        return None, "URL is required and must be a string"

    # Normalize URL
    url = url.strip()

    # Add https:// if missing
    if url.startswith("github.com"):
        url = "https://" + url
    elif url.startswith("http://github.com"):
        url = url.replace("http://", "https://")

    # Validate it's a GitHub URL
    github_pattern = r'^https://github\.com/([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+)(?:\.git)?/?$'
    match = re.match(github_pattern, url)

    if not match:
        # Check if it's a GitHub URL but malformed
        if "github.com" in url.lower():
            # Check for common issues
            if "/tree/" in url or "/blob/" in url:
                return None, "URL points to a specific file/branch. Use the repository root URL (e.g., https://github.com/juliangarnier/anime)"
            if url.count("/") < 4:
                return None, "URL appears to be missing the repository name. Format: https://github.com/juliangarnier/anime"
            return None, f"Invalid GitHub repository URL format: {url}"
        return None, f"Not a GitHub URL. Expected format: https://github.com/juliangarnier/anime"

    owner = match.group(1)
    repo = match.group(2)

    # Remove .git suffix if present
    if repo.endswith(".git"):
        repo = repo[:-4]

    # Validate owner and repo names
    if owner.startswith("-") or owner.startswith("."):
        return None, f"Invalid owner name: {owner}"
    if repo.startswith("-") or repo.startswith("."):
        return None, f"Invalid repository name: {repo}"

    normalized_url = f"https://github.com/{owner}/{repo}"

    return ParsedGitHubURL(
        owner=owner,
        repo=repo,
        original_url=url,
        normalized_url=normalized_url
    ), None


def verify_repository(owner: str, repo: str) -> tuple[Optional[RepoMetadata], Optional[str]]:
    """
    Verify repository exists and retrieve metadata via GitHub API.

    Args:
        owner: Repository owner (username or organization)
        repo: Repository name

    Returns:
        Tuple of (RepoMetadata or None, error message or None)
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Build headers with optional authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "skill-generator-plugin/1.0"
    }

    # Add auth token if available (increases rate limit from 60 to 5000 req/hour)
    token = get_github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(api_url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                return None, f"Unexpected status code: {response.status}"

            data = json.loads(response.read().decode("utf-8"))

            # Extract license info safely
            license_name = None
            if data.get("license") and isinstance(data["license"], dict):
                license_name = data["license"].get("spdx_id") or data["license"].get("name")

            return RepoMetadata(
                full_name=data.get("full_name", f"{owner}/{repo}"),
                description=data.get("description"),
                default_branch=data.get("default_branch", "main"),
                topics=data.get("topics", []),
                license=license_name,
                homepage=data.get("homepage"),
                stargazers_count=data.get("stargazers_count", 0),
                fork=data.get("fork", False),
                archived=data.get("archived", False),
                language=data.get("language"),
                created_at=data.get("created_at", ""),
                updated_at=data.get("updated_at", "")
            ), None

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, f"Repository not found: {owner}/{repo}. Verify the URL is correct and the repository is public."
        elif e.code == 403:
            # Check if rate limited
            remaining = e.headers.get("X-RateLimit-Remaining", "unknown")
            if remaining == "0":
                reset_time = e.headers.get("X-RateLimit-Reset", "unknown")
                return None, f"GitHub API rate limit exceeded. Resets at timestamp: {reset_time}. Consider using a GitHub token."
            return None, f"Access forbidden for {owner}/{repo}. The repository may be private."
        elif e.code == 401:
            return None, "GitHub API authentication error. Check your credentials."
        else:
            return None, f"GitHub API error (HTTP {e.code}): {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error connecting to GitHub API: {e.reason}"
    except json.JSONDecodeError as e:
        return None, f"Failed to parse GitHub API response: {e}"
    except Exception as e:
        return None, f"Unexpected error: {type(e).__name__}: {e}"


def github_to_codewiki_url(owner: str, repo: str) -> str:
    """
    Convert GitHub repository to Codewiki URL.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        Codewiki URL string
    """
    return f"https://codewiki.google/github.com/{owner}/{repo}"


def full_verification(url: str) -> VerificationResult:
    """
    Perform full verification pipeline on a GitHub URL.

    Args:
        url: GitHub repository URL

    Returns:
        VerificationResult with all data or error information
    """
    # Step 1: Parse URL
    parsed, error = parse_github_url(url)
    if error:
        return VerificationResult(
            success=False,
            parsed=None,
            metadata=None,
            codewiki_url=None,
            error=f"URL Parse Error: {error}"
        )

    # Step 2: Verify repository exists
    metadata, error = verify_repository(parsed.owner, parsed.repo)
    if error:
        return VerificationResult(
            success=False,
            parsed=parsed,
            metadata=None,
            codewiki_url=None,
            error=f"Verification Error: {error}"
        )

    # Step 3: Generate Codewiki URL
    codewiki_url = github_to_codewiki_url(parsed.owner, parsed.repo)

    return VerificationResult(
        success=True,
        parsed=parsed,
        metadata=metadata,
        codewiki_url=codewiki_url,
        error=None
    )


def result_to_json(result: VerificationResult) -> str:
    """Convert VerificationResult to JSON string."""
    def serialize(obj):
        if hasattr(obj, "__dict__"):
            return {k: serialize(v) for k, v in obj.__dict__.items() if v is not None}
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        return obj

    return json.dumps(serialize(result), indent=2)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nCommands:")
        print("  parse <url>     Parse and validate GitHub URL")
        print("  verify <url>    Verify repository exists via GitHub API")
        print("  codewiki <url>  Generate Codewiki URL from GitHub URL")
        print("  full <url>      Run full verification pipeline (parse + verify + codewiki)")
        sys.exit(1)

    command = sys.argv[1].lower()
    url = sys.argv[2]

    if command == "parse":
        parsed, error = parse_github_url(url)
        if error:
            print(json.dumps({"success": False, "error": error}))
            sys.exit(1)
        print(json.dumps({
            "success": True,
            "owner": parsed.owner,
            "repo": parsed.repo,
            "original_url": parsed.original_url,
            "normalized_url": parsed.normalized_url
        }, indent=2))

    elif command == "verify":
        parsed, error = parse_github_url(url)
        if error:
            print(json.dumps({"success": False, "error": error}))
            sys.exit(1)

        metadata, error = verify_repository(parsed.owner, parsed.repo)
        if error:
            print(json.dumps({"success": False, "error": error}))
            sys.exit(1)

        print(json.dumps({
            "success": True,
            "owner": parsed.owner,
            "repo": parsed.repo,
            **asdict(metadata)
        }, indent=2))

    elif command == "codewiki":
        parsed, error = parse_github_url(url)
        if error:
            print(json.dumps({"success": False, "error": error}))
            sys.exit(1)

        codewiki_url = github_to_codewiki_url(parsed.owner, parsed.repo)
        print(json.dumps({
            "success": True,
            "github_url": parsed.normalized_url,
            "codewiki_url": codewiki_url
        }, indent=2))

    elif command == "full":
        result = full_verification(url)
        print(result_to_json(result))
        sys.exit(0 if result.success else 1)

    else:
        print(f"Unknown command: {command}")
        print("Use: parse, verify, codewiki, or full")
        sys.exit(1)


if __name__ == "__main__":
    main()
