# Scripts

Useful scripts for many projects to get context information and convert documents.

## Available Scripts

### `convert-html-to-markdown.py`
Converts HTML files to Markdown using markitdown and properly organizes associated images with corrected relative paths.

**Features:**
- Automatic image organization and path correction
- Batch processing support
- Smart tool detection (markitdown/uvx fallback)
- Non-interactive mode support

**Usage:**
```bash
python convert-html-to-markdown.py -i ./paper-source -o ./output
python convert-html-to-markdown.py -i ./paper-source -o ./my-paper.md --yes
```

### `convert-pdf-to-markdown.py`
Converts PDF files to Markdown using markitdown with enhanced image extraction capabilities.

**Features:**
- Basic PDF to Markdown conversion
- Enhanced image extraction with PyMuPDF
- LLM-powered image descriptions (OpenAI integration)
- Azure Document Intelligence support
- Automatic image organization
- Batch processing support

**Usage:**
```bash
# Basic conversion
python convert-pdf-to-markdown.py -i ./paper.pdf -o ./output

# With enhanced image extraction
python convert-pdf-to-markdown.py -i ./paper.pdf -o ./output --extract-images

# With LLM image descriptions (requires OPENAI_API_KEY)
python convert-pdf-to-markdown.py -i ./paper.pdf -o ./output --use-llm

# With Azure Document Intelligence
python convert-pdf-to-markdown.py -i ./paper.pdf -o ./output --azure-endpoint "https://..."

# Batch process multiple PDFs
python convert-pdf-to-markdown.py -i ./pdfs/ -o ./converted/ --extract-images --yes
```

**Requirements:**
- `markitdown[all]` (required)
- `PyMuPDF` (optional, for enhanced image extraction)
- `openai` (optional, for LLM image descriptions)
- Azure endpoint (optional, for enhanced PDF processing)

### `download-html.py`
Downloads HTML content from URLs using Playwright for dynamic content rendering.

### `extract_references.py`
Extracts references from academic papers in markdown format.