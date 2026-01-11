#!/usr/bin/env python3
"""
Firecrawl Utility for skill-generator plugin.

Scrapes web pages using the Firecrawl API for enhanced documentation extraction.
Falls back gracefully if API key is not available.

Usage:
    python firecrawl_utils.py scrape <url> [--api-key <key>] [--config <path>] [--max-chars <int>] [--output <path>]
    python firecrawl_utils.py scrape <url> --config .claude/config.json

Examples:
    python firecrawl_utils.py scrape https://codewiki.google/github.com/juliangarnier/anime
    python firecrawl_utils.py scrape https://example.com --api-key fc-xxx
    python firecrawl_utils.py scrape https://codewiki.google/github.com/juliangarnier/anime --max-chars 200000 --output .claude/tmp/firecrawl/anime.md
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1/scrape"


def parse_env_file(filepath: str) -> dict:
    """
    Parse a .env file and return key-value pairs.

    Args:
        filepath: Path to the .env file

    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Parse KEY=value format
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    env_vars[key] = value
    except IOError:
        pass

    return env_vars


def get_api_key(config_path: str = None) -> str:
    """
    Get Firecrawl API key from multiple sources.

    Priority:
    1. Provided config file (.claude/config.json)
    2. .env file in working directory
    3. Environment variable (FIRECRAWL_API_KEY)

    Returns:
        API key string or None if not found
    """
    # Check config file first
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                key = config.get('firecrawl_api_key', '')
                if key and key.strip():
                    return key.strip()
        except (json.JSONDecodeError, IOError):
            pass

    # Check default config location
    default_config = '.claude/config.json'
    if os.path.exists(default_config):
        try:
            with open(default_config, 'r') as f:
                config = json.load(f)
                key = config.get('firecrawl_api_key', '')
                if key and key.strip():
                    return key.strip()
        except (json.JSONDecodeError, IOError):
            pass

    # Check .env file in working directory
    env_vars = parse_env_file('.env')
    if 'FIRECRAWL_API_KEY' in env_vars:
        key = env_vars['FIRECRAWL_API_KEY']
        if key and key.strip():
            return key.strip()

    # Check environment variable
    env_key = os.environ.get('FIRECRAWL_API_KEY', '')
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def scrape_url(url: str, api_key: str, formats: list = None) -> dict:
    """
    Scrape a URL using the Firecrawl API.

    Args:
        url: The URL to scrape
        api_key: Firecrawl API key
        formats: List of output formats (default: ["markdown"])

    Returns:
        dict with 'success', 'content', and 'error' keys
    """
    if not api_key:
        return {
            "success": False,
            "content": None,
            "error": "No API key provided. Set FIRECRAWL_API_KEY or add to .claude/config.json"
        }

    if formats is None:
        formats = ["markdown"]

    payload = {
        "url": url,
        "formats": formats,
        "onlyMainContent": True
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = Request(FIRECRAWL_API_URL, data=data, headers=headers, method='POST')

        with urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

            if result.get('success'):
                content = result.get('data', {}).get('markdown', '')
                return {
                    "success": True,
                    "content": content,
                    "metadata": result.get('data', {}).get('metadata', {}),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "content": None,
                    "error": result.get('error', 'Unknown error from Firecrawl API')
                }

    except HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        if e.code == 401:
            return {
                "success": False,
                "content": None,
                "error": f"Unauthorized: Invalid API key. Get one at https://firecrawl.dev"
            }
        elif e.code == 402:
            return {
                "success": False,
                "content": None,
                "error": "Payment required: Firecrawl API quota exceeded"
            }
        elif e.code == 429:
            return {
                "success": False,
                "content": None,
                "error": "Rate limited: Too many requests to Firecrawl API"
            }
        else:
            return {
                "success": False,
                "content": None,
                "error": f"HTTP {e.code}: {error_body or str(e)}"
            }

    except URLError as e:
        return {
            "success": False,
            "content": None,
            "error": f"Network error: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "content": None,
            "error": f"Unexpected error: {str(e)}"
        }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command != "scrape":
        print(f"Unknown command: {command}")
        print("Usage: python firecrawl_utils.py scrape <url>")
        sys.exit(1)

    url = sys.argv[2]

    # Parse optional arguments
    api_key = None
    config_path = None
    max_chars = None
    output_path = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--api-key" and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--config" and i + 1 < len(sys.argv):
            config_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--max-chars" and i + 1 < len(sys.argv):
            try:
                max_chars = int(sys.argv[i + 1])
            except ValueError:
                print("Invalid value for --max-chars. Must be an integer.")
                sys.exit(1)
            if max_chars < 0:
                print("Invalid value for --max-chars. Must be >= 0.")
                sys.exit(1)
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Get API key if not provided
    if not api_key:
        api_key = get_api_key(config_path)

    # Scrape the URL
    result = scrape_url(url, api_key)

    if result.get("success"):
        content = result.get("content") or ""
        content_length = len(content)

        if output_path:
            try:
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                result["content_path"] = output_path
            except OSError as e:
                result = {
                    "success": False,
                    "content": None,
                    "error": f"Failed to write output file: {e}"
                }

        if result.get("success") and max_chars is not None:
            if content_length > max_chars:
                result["content"] = content[:max_chars]
                result["content_truncated"] = True
            else:
                result["content_truncated"] = False
            result["content_length"] = content_length

    # Output as JSON
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
