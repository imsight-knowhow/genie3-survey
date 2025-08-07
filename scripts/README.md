# HTML Downloader with Playwright

A robust Python script for downloading JavaScript-rendered HTML pages and their associated resources (images, CSS, JS) using Playwright.

## Features

- Downloads fully-rendered HTML after JavaScript execution
- Optional resource downloading (images only or all resources)
- Handles modern web optimizations (WebP served as PNG, etc.)
- Organizes resources by domain in subdirectories
- Generates sensible filenames based on URLs
- Comprehensive error handling and installation guidance

## Installation

⚠️ **Important**: The conda-forge version of Playwright has missing driver files and will NOT work. You must use the PyPI version.

### Option 1: Global Installation (Recommended for standalone use)

```bash
# Install pipx globally using pixi
pixi global install pipx

# Install Playwright executable using pipx
pipx install playwright

# Install browser binaries
playwright install chromium

# Install Python API
pip install playwright
```

### Option 2: Local pixi Environment (Recommended for project isolation)

Add to your `pixi.toml`:

```toml
[dependencies]
nodejs = ">=20"

[pypi-dependencies]  
playwright = ">=1.54.0"
```

Then run:

```bash
# Install the environment
pixi install

# Install browser binaries
pixi run python -m playwright install chromium
```

## Usage

### Basic Examples

```bash
# Download HTML only
python scripts/download-html.py -u https://example.com -o page.html

# Download HTML with images
python scripts/download-html.py -u https://wikipedia.org -o wiki/ --with-images

# Download HTML with all resources (CSS, JS, images, etc.)
python scripts/download-html.py -u https://github.com -o github/ --with-all

# Auto-generate filename from URL
python scripts/download-html.py -u https://example.com
```

### Command Line Options

- `-u, --url URL`: URL of the page to download (required)
- `-o, --output OUTPUT`: Output file name or directory (default: generated from URL)
- `--with-images`: Download HTML and images only
- `--with-all`: Download all resources (images, stylesheets, etc.)
- `-h, --help`: Show help message

## How It Works

1. **Launches Chromium**: Uses Playwright to launch a real browser
2. **Executes JavaScript**: Waits for page to fully load including dynamic content
3. **Captures Resources**: Intercepts network requests to download assets
4. **Smart Naming**: Uses actual content-type headers for correct file extensions
5. **Organizes Output**: Saves HTML and resources in organized directory structure

## Troubleshooting

### "FileNotFoundError: [WinError 2] The system cannot find the file specified"

This error indicates you have the conda-forge version of Playwright installed, which lacks the Node.js driver. Solution:

1. Remove conda-forge playwright packages
2. Install PyPI version using instructions above

### "Import Error: No module named 'playwright'"

Playwright Python API is not installed. Run:
```bash
pip install playwright
```

### "Browser not found"

Browser binaries are not installed. Run:
```bash
playwright install chromium
```

## File Format Handling

The script automatically detects and handles:

- **WebP images** served with PNG URLs
- **SVG files** with various extensions
- **CSS and JavaScript** files
- **Binary resources** with appropriate extensions

Files are saved with correct extensions based on their actual content-type, not just the URL.
