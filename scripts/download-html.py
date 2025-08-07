#!/usr/bin/env python3
"""
Download HTML pages and their resources using Playwright.

This script downloads JavaScript-rendered HTML pages and optionally downloads
associated resources like images, stylesheets, and other assets.

INSTALLATION REQUIREMENTS:
==========================

IMPORTANT: The conda-forge version of Playwright has missing driver files and will NOT work.
You must install the PyPI version of Playwright to use this script.

Option 1: Global Installation (Recommended for standalone use)
-------------------------------------------------------------
If you're using pixi and want to install Playwright globally:

1. Install pipx globally using pixi:
   pixi global install pipx

2. Install Playwright executable using pipx:
   pipx install playwright

3. Install browser binaries:
   playwright install chromium

4. Install Python API:
   pip install playwright

Option 2: Local pixi Environment (Recommended for project isolation)
--------------------------------------------------------------------
If you want to keep Playwright in your pixi project environment:

1. Add to your pixi.toml dependencies:
   [dependencies]
   nodejs = ">=20"

   [pypi-dependencies]  
   playwright = ">=1.54.0"

2. Install the environment:
   pixi install

3. Install browser binaries:
   pixi run python -m playwright install chromium

Common Issues:
--------------
- If you see "FileNotFoundError: [WinError 2] The system cannot find the file specified",
  this means you have the conda-forge version installed, which lacks the Node.js driver.
- Remove any conda-forge playwright packages and use PyPI version instead.
- Make sure Node.js is available in your environment when using local installation.

USAGE:
======

Basic HTML download:
    python download-html.py -u https://example.com -o output.html

Download HTML with images:
    python download-html.py -u https://example.com -o output/ --with-images

Download HTML with all resources (CSS, JS, images, etc.):
    python download-html.py -u https://example.com -o output/ --with-all

Auto-generate filename from URL:
    python download-html.py -u https://example.com

The script will:
- Download the fully-rendered HTML after JavaScript execution
- Optionally download associated resources with correct file extensions
- Handle modern web optimizations (e.g., WebP images served as PNG URLs)
- Organize resources by domain in subdirectories
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Optional, Set
from urllib.parse import urljoin, urlparse, unquote

from playwright.async_api import Page, Response, async_playwright  # type: ignore[import-untyped]


class HTMLDownloader:
    """Download HTML pages and resources using Playwright."""
    
    def __init__(self, url: str, output: str, with_all: bool = False, with_images: bool = False) -> None:
        """Initialize the HTML downloader.
        
        Args:
            url: The URL to download
            output: Output file path or directory
            with_all: Whether to download all resources
            with_images: Whether to download images only
        """
        self.url = url
        self.output = output
        self.with_all = with_all
        self.with_images = with_images
        self.downloaded_urls: Set[str] = set()
        self.resource_counter = 0
        
    def _get_output_paths(self) -> tuple[Path, Optional[Path]]:
        """Determine output paths for HTML file and resources directory.
        
        Returns:
            Tuple of (html_file_path, resources_dir_path)
        """
        output_path = Path(self.output)
        
        if output_path.is_dir() or self.output.endswith('/') or self.output.endswith('\\'):
            # Output is a directory
            html_file = output_path / "downloaded.html"
            if self.with_all or self.with_images:
                domain = urlparse(self.url).netloc
                resources_dir = output_path / domain
            else:
                resources_dir = None
        else:
            # Output is a file path
            html_file = output_path
            if self.with_all or self.with_images:
                domain = urlparse(self.url).netloc
                resources_dir = html_file.parent / domain
            else:
                resources_dir = None
                
        return html_file, resources_dir
    
    def _get_default_filename(self) -> str:
        """Generate a default filename based on URL."""
        parsed = urlparse(self.url)
        domain = parsed.netloc
        path = parsed.path.strip('/')
        
        if path:
            # Replace slashes and special characters
            safe_path = path.replace('/', '_').replace('\\', '_')
            filename = f"{domain}_{safe_path}.html"
        else:
            filename = f"{domain}.html"
            
        return filename
    
    def _get_resource_filename(self, url: str, content_type: str) -> str:
        """Generate a filename for a resource.
        
        Args:
            url: Resource URL
            content_type: MIME content type
            
        Returns:
            Filename for the resource
        """
        parsed = urlparse(url)
        base_filename = os.path.basename(unquote(parsed.path))
        
        # Extract base name without extension
        if base_filename and '.' in base_filename:
            name_without_ext = os.path.splitext(base_filename)[0]
        else:
            name_without_ext = base_filename or f"resource_{self.resource_counter + 1}"
            self.resource_counter += 1
        
        # Determine correct extension based on actual content type
        if 'image' in content_type.lower():
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            elif 'svg' in content_type:
                ext = '.svg'
            else:
                ext = '.jpg'  # default for images
        elif 'css' in content_type.lower():
            ext = '.css'
        elif 'javascript' in content_type.lower():
            ext = '.js'
        else:
            # If no specific content type, try to use original extension
            if base_filename and '.' in base_filename:
                ext = os.path.splitext(base_filename)[1]
            else:
                ext = '.bin'
        
        filename = f"{name_without_ext}{ext}"
        return filename
    
    def _should_download_resource(self, response: Response) -> bool:
        """Determine if a resource should be downloaded based on options.
        
        Args:
            response: Playwright response object
            
        Returns:
            True if resource should be downloaded
        """
        if not (self.with_all or self.with_images):
            return False
            
        content_type: str = response.headers.get("content-type", "").lower()
        
        if self.with_all:
            # Download all resources except HTML documents
            return not content_type.startswith("text/html")
        elif self.with_images:
            # Download only images
            return content_type.startswith("image/")
        
        return False
    
    async def _handle_response(self, response: Response, resources_dir: Path) -> None:
        """Handle a network response and optionally download the resource.
        
        Args:
            response: Playwright response object
            resources_dir: Directory to save resources
        """
        if not self._should_download_resource(response):
            return
            
        url = response.url
        if url in self.downloaded_urls:
            return
            
        try:
            content_type: str = response.headers.get("content-type", "")
            filename = self._get_resource_filename(url, content_type)
            filepath = resources_dir / filename
            
            # Create directory if it doesn't exist
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Download and save the resource
            buffer = await response.body()
            with open(filepath, "wb") as f:
                f.write(buffer)
                
            self.downloaded_urls.add(url)
            print(f"Downloaded resource: {filename}")
            
        except Exception as e:
            print(f"Error downloading resource {url}: {e}")
    
    async def download(self) -> None:
        """Download the HTML page and optionally its resources."""
        html_file, resources_dir = self._get_output_paths()
        
        # Create output directory if needed
        html_file.parent.mkdir(parents=True, exist_ok=True)
        if resources_dir:
            resources_dir.mkdir(parents=True, exist_ok=True)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                
                # Set up response handler for resource downloads
                if resources_dir:
                    page.on("response", lambda response: asyncio.create_task(
                        self._handle_response(response, resources_dir)
                    ))
                
                # Navigate to the page
                print(f"Loading page: {self.url}")
                await page.goto(self.url, wait_until="networkidle")
                
                # Get the rendered HTML content
                html_content = await page.content()
                
                # Save the HTML file
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                print(f"HTML saved to: {html_file}")
                
                if resources_dir:
                    print(f"Resources saved to: {resources_dir}")
                    
            finally:
                await browser.close()


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Download HTML pages and their resources using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  %(prog)s -u https://example.com -o page.html
    Download HTML only

  %(prog)s -u https://wikipedia.org -o wiki/ --with-images  
    Download HTML and images to wiki/ directory

  %(prog)s -u https://github.com -o github/ --with-all
    Download HTML and all resources (CSS, JS, images, etc.)

INSTALLATION:
  This script requires the PyPI version of Playwright (NOT conda-forge).
  See the script header for detailed installation instructions.
        """
    )
    
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="URL of the page to download"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file name or directory (default: generated from URL)"
    )
    
    parser.add_argument(
        "--with-all",
        action="store_true",
        help="Download all resources (images, stylesheets, etc.)"
    )
    
    parser.add_argument(
        "--with-images",
        action="store_true",
        help="Download HTML and images only"
    )
    
    args = parser.parse_args()
    
    # Set default output if not provided
    if not args.output:
        downloader = HTMLDownloader(args.url, "", args.with_all, args.with_images)
        args.output = downloader._get_default_filename()
    
    # Validate arguments
    if args.with_all and args.with_images:
        print("Error: --with-all and --with-images are mutually exclusive")
        sys.exit(1)
    
    # Create downloader and run
    downloader = HTMLDownloader(args.url, args.output, args.with_all, args.with_images)
    
    try:
        asyncio.run(downloader.download())
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(1)
    except ImportError as e:
        if "playwright" in str(e).lower():
            print("Error: Playwright is not installed or not properly configured.")
            print("\nInstallation options:")
            print("1. Global: pipx install playwright && playwright install chromium && pip install playwright")
            print("2. Local: Add nodejs and playwright to pixi.toml pypi-dependencies")
            print("\nSee script header for detailed instructions.")
        else:
            print(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        error_msg = str(e).lower()
        if "file not found" in error_msg or "winerror 2" in error_msg:
            print("Error: Playwright driver not found.")
            print("This usually means you have the conda-forge version installed.")
            print("Please install the PyPI version instead. See script header for instructions.")
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
