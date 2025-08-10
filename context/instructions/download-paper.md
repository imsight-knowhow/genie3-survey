you are tasked to download a paper from a URL, do it following these instructions.

# Guide to Downloading Papers

- by default, we will download the paper in `<workspace>/tmp/papers`, creating a subdirectory with the paper name and save everything in it, this `<workspace>/tmp/papers` is called `paper-dir`. The user my specify a different `paper-dir` in the prompt, pay attention to it.

- we need to keep an index of downloaded papers in the `<workspace>/papers` dir, name it `papers-index.md`, which will contain the paper name, URL, and a brief description, and downloaded location (relative to the `<workspace>`). So after you download a paper, you should update this index file with the new paper information.

## If you are given a URL

- the paper is hosted as html, download it using `scripts\download-html.py`, including html and images (using `--with-images` option).
- save the output in `${paper-dir}/<paper-name>/` directory, within it, names are dictated by the `download-html.py` script, let it handle the naming.

## If you are given a PDF URL

- use `aria2c` to download the PDF file, into the `${paper-dir}/<paper-name>/` directory, name the file as `paper.pdf`.

## If you are given a paper name

- use Tavily to search for the paper by title, author, or keywords.
- if it is an arXiv paper, find out its html version URL (e.g., from `https://arxiv.org/abs/2401.12345` to `https://arxiv.org/html/2401.12345`), and prefer to download the HTML version with images.
- if html version is not available, download the PDF version using `aria2c` as described below.

# Tools and Commands

Here are the tools and commands you can use to download papers.

## How to download PDF with aria2c

**Check if aria2c is available:**
```powershell
aria2c --version
```

**Download PDF to paper directory:**
```powershell
# Create directory and download
New-Item -ItemType Directory -Force -Path "tmp/papers/paper-name"
aria2c -o "paper.pdf" -d "tmp/papers/paper-name" "https://example.com/paper.pdf"
```

**Faster download with multiple connections:**
```powershell
aria2c -o "paper.pdf" -d "tmp/papers/paper-name" -s 4 -x 4 "https://arxiv.org/pdf/2401.12345.pdf"
```

**Key options:**
- `-o filename`: Output filename
- `-d directory`: Download directory  
- `-s/-x connections`: Multiple connections for speed

## Finding Papers with Search Tools

### Using Tavily Search

Use Tavily to search for papers by topic, author, or keywords:

**Search for recent papers:**
```
Search query example: "Genie 3 video generation model 2024"
```

Tavily can help you:
- Find paper URLs from arXiv, conferences, or journals
- Discover related papers and recent publications
- Get paper abstracts and metadata

### Using Context7 for Library Documentation

Use Context7 to get comprehensive documentation about specific libraries or frameworks mentioned in papers:

**Example workflow:**
1. Identify libraries/frameworks from paper (e.g., PyTorch, TensorFlow, Transformers)
2. Use Context7 to get detailed documentation
3. Better understand implementation details mentioned in the paper

## Complete Workflow Examples

### For arXiv Papers

**HTML version (recommended for papers with figures):**
```powershell
# Step 1: Search for the paper
# Use Tavily: "paper title author year"

# Step 2: Convert arXiv abstract URL to HTML
# From: https://arxiv.org/abs/2401.12345
# To: https://arxiv.org/html/2401.12345

# Step 3: Download HTML with images
pixi run python scripts/download-html.py -u https://arxiv.org/html/2401.12345 -o tmp/papers/paper-name/ --with-images
```

**PDF version:**
```powershell
# Step 1: Get PDF URL from arXiv
# From: https://arxiv.org/abs/2401.12345
# To: https://arxiv.org/pdf/2401.12345.pdf

# Step 2: Download PDF
New-Item -ItemType Directory -Force -Path "tmp/papers/paper-name"
aria2c -o "paper.pdf" -d "tmp/papers/paper-name" "https://arxiv.org/pdf/2401.12345.pdf"
```

### For Conference/Journal Papers

**When you have a direct PDF link:**
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path "tmp/papers/paper-name"

# Download PDF
aria2c -o "paper.pdf" -d "tmp/papers/paper-name" "https://conference.org/papers/paper.pdf"
```

**When you need to find the paper:**
1. Use Tavily to search for the paper by title, author, or DOI
2. Look for PDF links in search results
3. Download using aria2c as above

## How to use `download-html.py`

The `download-html.py` script downloads JavaScript-rendered HTML pages and their resources using Playwright.

### Basic Usage

**Download HTML only:**
```powershell
# To specific file
pixi run python scripts/download-html.py -u https://example.com -o output.html

# To tmp directory with auto-generated filename
pixi run python scripts/download-html.py -u https://example.com -o tmp/
```

**Download HTML with images (Recommended for papers):**
```powershell
# To specific directory
pixi run python scripts/download-html.py -u https://arxiv.org/html/2401.12345 -o tmp/paper-name/ --with-images

# With auto-generated filename in current directory
pixi run python scripts/download-html.py -u https://example.com --with-images
```

**Download HTML with all resources (CSS, JS, images, etc.):**
```powershell
pixi run python scripts/download-html.py -u https://example.com -o tmp/paper-name/ --with-all
```

### Command Options

- `-u, --url`: URL of the page to download (required)
- `-o, --output`: Output file name or directory (optional, auto-generated if not provided)
- `--with-images`: Download HTML and images only
- `--with-all`: Download all resources (images, stylesheets, JavaScript, etc.)

### For arXiv Papers

For arXiv papers, convert the abstract URL to HTML format:
- **Abstract URL:** `https://arxiv.org/abs/2401.12345`
- **HTML URL:** `https://arxiv.org/html/2401.12345`

**Example workflow for arXiv paper:**
```powershell
# Step 1: Download with images to tmp
pixi run python scripts/download-html.py -u https://arxiv.org/html/2401.12345 -o tmp/genie3-paper/ --with-images

# Step 2: The script will create:
# tmp/genie3-paper/downloaded.html
# tmp/genie3-paper/arxiv.org/images/...
```

### Output Structure

**When downloading to a directory:**
```
output-directory/
├── downloaded.html          # Main HTML file
└── domain.com/             # Resources organized by domain
    ├── image1.jpg
    ├── image2.png
    └── style.css
```

**When downloading to a specific file:**
```
specified-file.html          # Main HTML file
domain.com/                 # Resources in adjacent directory
├── image1.jpg
└── image2.png
```

### Common Issues

**Error: "FileNotFoundError" or "WinError 2":**
- Ensure PyPI version of Playwright is installed (not conda-forge)

**Browser installation issues:**
- Run `pixi run python -m playwright install chromium`

### Resource Handling

The script automatically:
- Downloads fully-rendered HTML after JavaScript execution
- Handles modern web optimizations (e.g., WebP images served as PNG URLs)
- Organizes resources by domain in subdirectories
- Uses correct file extensions based on actual content type
- Avoids downloading duplicate resources
