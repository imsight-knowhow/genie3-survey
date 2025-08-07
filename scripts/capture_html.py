#!/usr/bin/env python3
"""
Capture rendered HTML from a webpage using Playwright headless browser.
Downloads all resources (images, CSS, JS) locally.
"""

import argparse
import asyncio
import sys
import os
import re
from pathlib import Path
from typing import Optional, Literal, Dict, Set
from urllib.parse import urljoin, urlparse, unquote
from playwright.async_api import async_playwright, Page, Response


class ResourceDownloader:
    def __init__(self, output_dir: Path, base_url: str):
        self.output_dir = output_dir
        self.base_url = base_url
        self.downloaded_urls: Dict[str, str] = {}  # url -> local_path
        self.resource_counter = 0
        
    def get_local_path(self, url: str, content_type: str = "") -> str:
        """Generate a local file path for a resource."""
        parsed = urlparse(url)
        
        # Get filename from URL
        filename = os.path.basename(unquote(parsed.path))
        
        # If no filename or extension, generate one based on content type
        if not filename or '.' not in filename:
            self.resource_counter += 1
            if 'image' in content_type.lower():
                ext = '.jpg' if 'jpeg' in content_type else '.png'
                if 'gif' in content_type: ext = '.gif'
                if 'webp' in content_type: ext = '.webp'
                if 'svg' in content_type: ext = '.svg'
            elif 'css' in content_type.lower():
                ext = '.css'
            elif 'javascript' in content_type.lower():
                ext = '.js'
            else:
                ext = '.bin'
            
            filename = f"resource_{self.resource_counter}{ext}"
        
        # Determine subdirectory based on content type
        if 'image' in content_type.lower():
            subdir = 'images'
        elif 'css' in content_type.lower():
            subdir = 'css'
        elif 'javascript' in content_type.lower():
            subdir = 'js'
        else:
            subdir = 'assets'
        
        return f"{subdir}/{filename}"
    
    async def download_resource(self, response: Response) -> None:
        """Download a resource and return its local path."""
        try:
            url = response.url
            
            # Skip if already downloaded
            if url in self.downloaded_urls:
                return
            
            # Get content type
            content_type = response.headers.get('content-type', '')
            
            # Only download certain types of resources
            if not any(t in content_type.lower() for t in ['image', 'css', 'javascript', 'font']):
                return
            
            # Get local path
            local_path = self.get_local_path(url, content_type)
            full_path = self.output_dir / local_path
            
            # Create directory if it doesn't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download the resource
            content = await response.body()
            full_path.write_bytes(content)
            
            # Store mapping
            self.downloaded_urls[url] = local_path
            
            print(f"Downloaded: {local_path}")
            
        except Exception as e:
            print(f"Error downloading {response.url}: {e}")
    
    def update_html_references(self, html: str) -> str:
        """Update HTML to reference local files."""
        updated_html = html
        
        for original_url, local_path in self.downloaded_urls.items():
            # Replace various URL references
            patterns = [
                f'src=["\']({re.escape(original_url)})["\']',
                f'href=["\']({re.escape(original_url)})["\']',
                f'url\\(["\']?({re.escape(original_url)})["\']?\\)',
            ]
            
            for pattern in patterns:
                updated_html = re.sub(
                    pattern,
                    lambda m: m.group(0).replace(original_url, local_path),
                    updated_html,
                    flags=re.IGNORECASE
                )
        
        return updated_html


async def capture_html_with_resources(
    url: str,
    output_file: str = "captured.html",
    delay: int = 0,
    timeout: int = 30000,
    wait_for_selector: Optional[str] = None,
    viewport_width: int = 1920,
    viewport_height: int = 1080,
    user_agent: Optional[str] = None,
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle",
    download_resources: bool = True
):
    """
    Capture rendered HTML from a webpage and optionally download all resources.
    """
    output_path = Path(output_file)
    output_dir = output_path.parent / output_path.stem
    
    downloader = None
    if download_resources:
        downloader = ResourceDownloader(output_dir, url)
    
    async with async_playwright() as p:
        browser = None
        try:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set up resource interception if downloading resources
            if download_resources and downloader:
                page.on("response", downloader.download_resource)
            
            # Set viewport
            await page.set_viewport_size({
                "width": viewport_width, 
                "height": viewport_height
            })
            
            # Set user agent if provided
            if user_agent:
                await page.set_extra_http_headers({"User-Agent": user_agent})
            
            print(f"Navigating to: {url}")
            
            # Navigate to the page
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # Wait for specific selector if provided
            if wait_for_selector:
                print(f"Waiting for selector: {wait_for_selector}")
                await page.wait_for_selector(wait_for_selector, timeout=10000)
            
            # Additional delay if specified
            if delay > 0:
                print(f"Waiting {delay} seconds...")
                await page.wait_for_timeout(delay * 1000)
            
            # Get the rendered HTML
            print("Capturing rendered HTML...")
            html = await page.content()
            
            # Update HTML with local resource references if we downloaded resources
            if download_resources and downloader:
                print("Updating HTML references to local resources...")
                html = downloader.update_html_references(html)
                print(f"Downloaded {len(downloader.downloaded_urls)} resources")
            
            # Save to file
            output_path.write_text(html, encoding='utf-8')
            
            # Show results
            file_size = output_path.stat().st_size / 1024
            print(f"HTML captured successfully!")
            print(f"Output file: {output_path.absolute()}")
            print(f"File size: {file_size:.2f} KB")
            
            if download_resources and downloader and downloader.downloaded_urls:
                print(f"Resources saved to: {output_dir.absolute()}")
            
        except Exception as e:
            print(f"Error capturing HTML: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if browser:
                await browser.close()
    """
    Capture rendered HTML from a webpage.
    
    Args:
        url: The URL to capture
        output_file: Output file path
        delay: Delay in seconds after page load
        timeout: Navigation timeout in milliseconds
        wait_for_selector: CSS selector to wait for before capturing
        viewport_width: Browser viewport width
        viewport_height: Browser viewport height
        user_agent: Custom user agent string
        wait_until: When to consider navigation done
    """
    async with async_playwright() as p:
        browser = None
        try:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set viewport
            await page.set_viewport_size({
                "width": viewport_width, 
                "height": viewport_height
            })
            
            # Set user agent if provided
            if user_agent:
                await page.set_extra_http_headers({"User-Agent": user_agent})
            
            print(f"Navigating to: {url}")
            
            # Navigate to the page
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # Wait for specific selector if provided
            if wait_for_selector:
                print(f"Waiting for selector: {wait_for_selector}")
                await page.wait_for_selector(wait_for_selector, timeout=10000)
            
            # Additional delay if specified
            if delay > 0:
                print(f"Waiting {delay} seconds...")
                await page.wait_for_timeout(delay * 1000)
            
            # Get the rendered HTML
            print("Capturing rendered HTML...")
            html = await page.content()
            
            # Save to file
            output_path = Path(output_file)
            output_path.write_text(html, encoding='utf-8')
            
            # Show results
            file_size = output_path.stat().st_size / 1024
            print(f"HTML captured successfully!")
            print(f"Output file: {output_path.absolute()}")
            print(f"File size: {file_size:.2f} KB")
            
        except Exception as e:
            print(f"Error capturing HTML: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if browser:
                await browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Capture rendered HTML from a webpage using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python capture_html.py https://example.com
  python capture_html.py https://example.com --output page.html --delay 3
  python capture_html.py https://example.com --wait-for "#content" --viewport 1280 720
  python capture_html.py https://example.com --user-agent "Custom Bot 1.0"
        """
    )
    
    parser.add_argument("url", help="The URL to capture")
    parser.add_argument(
        "--output", "-o", 
        default="captured.html",
        help="Output file path (default: captured.html)"
    )
    parser.add_argument(
        "--delay", "-d",
        type=int, 
        default=0,
        help="Delay in seconds after page load (default: 0)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30000,
        help="Navigation timeout in milliseconds (default: 30000)"
    )
    parser.add_argument(
        "--wait-for", "-w",
        help="CSS selector to wait for before capturing"
    )
    parser.add_argument(
        "--viewport",
        nargs=2,
        type=int,
        default=[1920, 1080],
        metavar=("WIDTH", "HEIGHT"),
        help="Viewport size (default: 1920 1080)"
    )
    parser.add_argument(
        "--user-agent", "-ua",
        help="Custom user agent string"
    )
    parser.add_argument(
        "--wait-until",
        choices=["load", "domcontentloaded", "networkidle"],
        default="networkidle",
        help="When to consider navigation done (default: networkidle)"
    )
    parser.add_argument(
        "--download-resources",
        action="store_true",
        default=True,
        help="Download all resources (images, CSS, JS) locally (default: True)"
    )
    parser.add_argument(
        "--no-download-resources",
        dest="download_resources",
        action="store_false",
        help="Don't download resources, only capture HTML"
    )
    
    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(capture_html_with_resources(
        url=args.url,
        output_file=args.output,
        delay=args.delay,
        timeout=args.timeout,
        wait_for_selector=args.wait_for,
        viewport_width=args.viewport[0],
        viewport_height=args.viewport[1],
        user_agent=args.user_agent,
        wait_until=args.wait_until,
        download_resources=args.download_resources
    ))


if __name__ == "__main__":
    main()
