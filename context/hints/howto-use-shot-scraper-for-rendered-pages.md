# How to Use shot-scraper for JavaScript-Rendered Pages

shot-scraper is a powerful command-line tool built on Playwright that captures web pages after JavaScript execution and downloads all associated assets. This guide covers how to download rendered pages and extract assets in various formats.

## Installation

```bash
pip install shot-scraper
# Install required browser dependencies
shot-scraper install
```

## Basic Usage: Download Rendered HTML

### Simple HTML Download After JS Execution

```bash
# Download rendered HTML after all JavaScript has executed
shot-scraper html https://example.com/ -o rendered-page.html
```

### With Custom JavaScript Execution

```bash
# Execute custom JavaScript before capturing
shot-scraper html https://example.com/ \
  --javascript "document.querySelector('h1').innerText = 'Modified Title'" \
  -o modified-page.html
```

### Wait for Dynamic Content

```bash
# Wait 3 seconds for dynamic content to load
shot-scraper html https://example.com/ \
  --wait 3000 \
  -o page-after-wait.html

# Wait for specific elements to appear
shot-scraper html https://example.com/ \
  --wait-for "document.querySelector('#dynamic-content')" \
  -o page-with-content.html
```

## Download All Assets: HAR Files

### Method 1: HAR Archive (JSON format)

```bash
# Creates a .har file containing all network requests
shot-scraper har https://example.com/
# Output: example-com.har (JSON file with request/response data)

# Custom filename
shot-scraper har https://example.com/ -o my-site.har
```

### Method 2: HAR.zip Archive (HTML + Assets Directory)

```bash
# Creates a .har.zip file with JSON + all actual asset files
shot-scraper har https://example.com/ --zip -o complete-site.har.zip

# Or use .har.zip extension (auto-detects zip format)
shot-scraper har https://example.com/ -o site-assets.har.zip
```

### Extract HAR.zip Contents

```bash
# Extract the archive to get HTML + assets directory
unzip complete-site.har.zip

# List contents without extracting
unzip -l complete-site.har.zip
```

### Fix Broken Links After Extraction

When you extract a HAR.zip file, the HTML contains absolute URLs that won't work with local assets. Here are solutions:

#### Method 1: Python Script to Fix Links

```python
#!/usr/bin/env python3
import re
import os
from urllib.parse import urlparse
import json

def fix_html_links(html_file, base_url):
    """Fix absolute URLs in HTML to relative paths for local assets"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse base URL to get domain
    parsed_base = urlparse(base_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    # Fix different types of URLs
    patterns = [
        # CSS files
        (rf'{re.escape(base_domain)}(/[^"\'>\s]*\.css)', r'.\1'),
        # JavaScript files  
        (rf'{re.escape(base_domain)}(/[^"\'>\s]*\.js)', r'.\1'),
        # Images
        (rf'{re.escape(base_domain)}(/[^"\'>\s]*\.(png|jpg|jpeg|gif|svg|webp))', r'.\1'),
        # Other assets
        (rf'{re.escape(base_domain)}(/[^"\'>\s]*\.(woff|woff2|ttf|ico))', r'.\1'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Write fixed content back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Usage
fix_html_links('index.html', 'https://example.com')
```

#### Method 2: Organize Files by Domain Structure

```bash
#!/bin/bash
# Script to properly organize extracted HAR assets

SITE_URL="https://example.com"
HAR_ZIP="site.har.zip"
OUTPUT_DIR="offline-site"

# Extract HAR.zip
unzip "$HAR_ZIP" -d temp-extract/

# Create domain-based directory structure
mkdir -p "$OUTPUT_DIR"

# Find the main HTML file from HAR data
HTML_FILE=$(find temp-extract/ -name "*.html" | head -1)
cp "$HTML_FILE" "$OUTPUT_DIR/index.html"

# Copy assets maintaining relative paths
find temp-extract/ -type f \( -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.svg" \) -exec cp {} "$OUTPUT_DIR/" \;

# Fix links in HTML
python3 fix_links.py "$OUTPUT_DIR/index.html" "$SITE_URL"

# Clean up
rm -rf temp-extract/
```

#### Method 3: Use sed for Simple Replacements

```bash
# Quick fix for simple cases (replace example.com with current directory)
sed -i 's|https://example\.com/|./|g' index.html
sed -i 's|http://example\.com/|./|g' index.html

# Fix common asset paths
sed -i 's|src="/|src="./|g' index.html
sed -i 's|href="/|href="./|g' index.html
```

## Non-Compressed Solution: HTML + Assets Directory

While shot-scraper doesn't directly create an "HTML + assets folder" structure, you can achieve this by:

### Option 1: Combine HTML + HAR.zip Extraction

```bash
# Step 1: Get rendered HTML
shot-scraper html https://example.com/ \
  --wait 2000 \
  -o index.html

# Step 2: Get all assets in HAR.zip
shot-scraper har https://example.com/ \
  --wait 2000 \
  --zip \
  -o assets.har.zip

# Step 3: Extract assets
unzip assets.har.zip -d extracted-assets/
```

### Option 2: Use Log Requests for Asset URLs

```bash
# Log all network requests to see what assets were loaded
shot-scraper shot https://example.com/ \
  --log-requests requests.json \
  -o screenshot.png

# Then manually download assets using the logged URLs
```

## Advanced Options

### Browser Selection

```bash
# Use Firefox instead of Chromium
shot-scraper html https://example.com/ \
  --browser firefox \
  -o firefox-rendered.html
```

### Bypass Security Restrictions

```bash
# Bypass Content Security Policy for problematic sites
shot-scraper html https://example.com/ \
  --bypass-csp \
  -o unrestricted.html
```

### Authentication Support

```bash
# Create authentication file (opens browser for manual login)
shot-scraper auth https://example.com/login auth.json

# Use authentication for protected pages
shot-scraper html https://example.com/protected \
  --auth auth.json \
  -o protected-page.html
```

### Complex JavaScript Scenarios

```bash
# Execute complex JavaScript with promises for timing control
shot-scraper html https://example.com/ \
  --javascript "new Promise(resolve => {
    // Wait for specific conditions
    const checkCondition = () => {
      if (document.querySelector('.loaded-content')) {
        resolve();
      } else {
        setTimeout(checkCondition, 100);
      }
    };
    checkCondition();
  })" \
  -o fully-loaded.html
```

## Working with HAR Files

### Understanding HAR File Structure

- **HAR (.har)**: JSON file containing HTTP Archive data with all network requests
- **HAR.zip (.har.zip)**: Compressed archive containing the HAR JSON plus all actual asset files

### Extract Specific Information from HAR

```javascript
// Example JavaScript to parse HAR file
const harData = JSON.parse(fs.readFileSync('site.har', 'utf8'));
const entries = harData.log.entries;

// Get all image URLs
const imageUrls = entries
  .filter(entry => entry.response.content.mimeType.startsWith('image/'))
  .map(entry => entry.request.url);
```

## Best Practices

### For Dynamic Content

```bash
# Combine multiple wait strategies for complex pages
shot-scraper html https://spa-example.com/ \
  --wait 3000 \
  --wait-for "document.querySelector('.app-loaded')" \
  --javascript "window.scrollTo(0, document.body.scrollHeight)" \
  -o spa-complete.html
```

### For Large Sites

```bash
# Use timeout to prevent hanging on slow sites
shot-scraper har https://heavy-site.com/ \
  --timeout 30000 \
  --zip \
  -o heavy-site.har.zip
```

### Error Handling

```bash
# Skip pages that return HTTP errors
shot-scraper html https://example.com/ \
  --skip \
  -o page-if-successful.html

# Or fail explicitly on errors
shot-scraper html https://example.com/ \
  --fail \
  -o page-or-fail.html
```

## Example Workflow: Complete Site Download

```bash
#!/bin/bash
# Complete workflow for downloading a JavaScript-rendered site with fixed links

SITE_URL="https://example.com"
OUTPUT_DIR="downloaded-site"

mkdir -p "$OUTPUT_DIR"

# 1. Download rendered HTML
shot-scraper html "$SITE_URL" \
  --wait 3000 \
  --javascript "console.log('Page fully loaded')" \
  -o "$OUTPUT_DIR/index.html"

# 2. Download all assets
shot-scraper har "$SITE_URL" \
  --wait 3000 \
  --zip \
  -o "$OUTPUT_DIR/assets.har.zip"

# 3. Extract and organize assets
cd "$OUTPUT_DIR"
unzip assets.har.zip -d extracted/

# 4. Fix links in HTML to work with local assets
python3 << 'EOF'
import re
import os

def fix_html_links(html_file, base_url):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace absolute URLs with relative paths
    content = re.sub(r'https://example\.com/', './', content)
    content = re.sub(r'http://example\.com/', './', content)
    
    # Fix root-relative paths
    content = re.sub(r'src="/', 'src="./', content)
    content = re.sub(r'href="/', 'href="./', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

fix_html_links('index.html', 'https://example.com')
EOF

# 5. Copy assets to main directory
find extracted/ -type f \( -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.svg" -o -name "*.woff*" \) -exec cp {} . \;

# Clean up
rm -rf extracted/ assets.har.zip

echo "Site downloaded to $OUTPUT_DIR/ with fixed links"
echo "Open $OUTPUT_DIR/index.html in your browser"
```

## Advanced Link Fixing

### Handle Complex URL Structures

```python
#!/usr/bin/env python3
"""
Advanced link fixer for extracted HAR files
Handles complex URL structures and maintains proper relative paths
"""
import re
import os
import json
from urllib.parse import urlparse, urljoin
from pathlib import Path

def analyze_har_structure(har_file):
    """Analyze HAR file to understand asset structure"""
    with open(har_file, 'r') as f:
        har_data = json.load(f)
    
    urls = []
    for entry in har_data['log']['entries']:
        urls.append(entry['request']['url'])
    
    return urls

def create_asset_mapping(urls, base_url):
    """Create mapping of absolute URLs to local paths"""
    mapping = {}
    parsed_base = urlparse(base_url)
    
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc == parsed_base.netloc:
            # Extract filename from path
            path_parts = parsed.path.strip('/').split('/')
            filename = path_parts[-1] if path_parts[-1] else 'index.html'
            mapping[url] = f'./{filename}'
    
    return mapping

def fix_complex_links(html_file, asset_mapping):
    """Fix links using comprehensive asset mapping"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sort URLs by length (longest first) to avoid partial replacements
    sorted_urls = sorted(asset_mapping.keys(), key=len, reverse=True)
    
    for abs_url in sorted_urls:
        rel_path = asset_mapping[abs_url]
        content = content.replace(abs_url, rel_path)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Usage example
if __name__ == "__main__":
    har_file = "extracted/site.har"
    html_file = "index.html"
    base_url = "https://example.com"
    
    urls = analyze_har_structure(har_file)
    mapping = create_asset_mapping(urls, base_url)
    fix_complex_links(html_file, mapping)
```

## References

- [shot-scraper Official Documentation](https://shot-scraper.datasette.io/)
- [shot-scraper GitHub Repository](https://github.com/simonw/shot-scraper)
- [HTTP Archive (HAR) Format Specification](https://w3c.github.io/web-performance/specs/HAR/Overview.html)
- [Playwright Documentation](https://playwright.dev/) (underlying engine)

## Troubleshooting

### Common Issues

1. **Page not fully loaded**: Increase `--wait` time or use `--wait-for` with specific selectors
2. **JavaScript errors**: Use `--bypass-csp` for CSP-protected sites
3. **Authentication required**: Use `shot-scraper auth` to create authentication context
4. **Large assets**: Use `--timeout` to prevent hanging on slow downloads
5. **Broken links after extraction**: Use the link-fixing scripts provided above

### Link Fixing Issues

#### CSS @import Rules
```bash
# Fix CSS @import statements
sed -i 's|@import url("https://example\.com/|@import url("./|g' *.css
sed -i "s|@import url('https://example\.com/|@import url('./|g" *.css
```

#### JavaScript Dynamic URLs
```javascript
// For JavaScript files that construct URLs dynamically
// Manual editing may be required, or use a more sophisticated replacement
// Replace in JS files:
// var baseUrl = "https://example.com";
// with:
// var baseUrl = ".";
```

#### Base64 Encoded Assets
```bash
# Some HAR files contain base64 encoded images
# These are already embedded and don't need fixing
# Look for: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
```

### Debugging

```bash
# Enable console logging to see JavaScript errors
shot-scraper html https://example.com/ \
  --log-console \
  -o debug-page.html

# Check what assets were actually downloaded
unzip -l assets.har.zip | grep -E '\.(css|js|png|jpg|gif)$'

# Verify link fixes worked
grep -n "https://example.com" index.html || echo "All absolute links fixed!"
```
