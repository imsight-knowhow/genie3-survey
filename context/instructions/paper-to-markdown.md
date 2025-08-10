you are tasked to convert an academic paper into a markdown format. Follow these guidelines:

# Guidelines for Converting Paper to Markdown

This guide covers multiple approaches for converting papers to markdown:
- **Approach 1**: Using utility scripts for offline HTML files  
- **Approach 2**: Direct `markitdown` usage for simple conversions

Also, if you are given a URL, you can download the HTML content first and then convert it to markdown, see the section on how to get HTML online, and prefer to use `--with-images` to download all images.

## File Handling

### The `paper-dir` directory

by default, save the markdown file and related resources in the `<workspace>/tmp/papers` directory (this dir is referred to as `paper-master-dir`), and create a subdir with the paper name (this is referred to as `paper-subdir`) . Note that the user can specify a different `paper-master-dir` or `paper-subdir` in the prompt, so pay attention to it.

### If you are given a html file
- save the converted markdown file and name it as `paper-content.md` in `paper-subdir`, no images.

### If you are given an html directory
- save the converted markdown file as `paper-content.md` in `paper-subdir`,and all images in a subdirectory, with whatever name you see fit, as long as the links are not broken (the given html may have its own naming convention, respect that).
- if you are using the utility script, then just point the script to the `paper-subdir`, and it will handle the output filename and image organization automatically, just rename the markdown file to `paper-content.md` and DO NOT touch other generated files.

### If you are given a URL
- download the HTML content to a temporary directory, such as `tmp/downloads`, and then convert it to markdown, just like the above cases, give the utility script the downloaded html dir. For downloading HTML with utility script, use `--with-images` option to download all images.

### If you are given a PDF file

- convert the PDF to markdown using `markitdown` directly, let it also export the images, and save the markdown file as `paper-content.md` in `paper-subdir`, with images in a subdirectory determined by the `markitdown` tool.

## Prerequisites

Ensure `markitdown` is available in your environment:

**Check if already installed:**
```bash
# Direct Python
pip list | grep markitdown

# With pixi
pixi list | grep markitdown
```

**Install if needed:**
```bash
# Direct Python
pip install markitdown[all]

pixi add --pypi markitdown[all]
```

## Approach 1: Using the Utility Script (Recommended)

The preferred method is to use the enhanced utility script `convert-html-to-markdown.py` (find it workspace) which provides automatic image organization and path correction.

If you need the script, download it from: `https://raw.githubusercontent.com/igamenovoer/quick-tools/refs/heads/main/convert-html-to-markdown.py`

### Key Features

- **Automatic image organization**: Copies images to unified `images/` directory
- **Path correction**: Updates image references to correct relative paths
- **Batch processing**: Handles multiple HTML files at once
- **Smart tool detection**: Uses available `markitdown` installation

### Basic Usage

**Convert HTML files from a directory:**
```bash
# Direct Python
python scripts/convert-html-to-markdown.py -i ./paper-source -o ./output

# With pixi
pixi run python scripts/convert-html-to-markdown.py -i ./paper-source -o ./output
```

**Convert to specific filename:**
```bash
# Direct Python
python scripts/convert-html-to-markdown.py -i ./paper-source -o ./my-paper.md

# With pixi
pixi run python scripts/convert-html-to-markdown.py -i ./paper-source -o ./my-paper.md
```

**Non-interactive mode:**
```bash
# Direct Python
python scripts/convert-html-to-markdown.py -i ./source -o ./result.md --yes

# With pixi
pixi run python scripts/convert-html-to-markdown.py -i ./source -o ./result.md --yes
```

### Command Options

- `-i, --input`: Input directory with HTML files (required)
- `-o, --output`: Output directory or markdown filename (required)  
- `-y, --yes`: Auto-confirm overwrite prompts
- `--keep-original-images`: Don't reorganize image structure
- `--verbose`: Show detailed progress

### Input/Output Structure

**Input directory:**
```
paper-source/
├── paper.html
├── images/
│   ├── figure1.png
│   └── diagram.jpg
```

**Output directory:**
```
output/
├── converted.md
├── images/
│   ├── figure1.png
│   └── diagram.jpg
└── README.md
```

The script automatically fixes image paths from `![alt](./images/figure1.png)` to `![alt](images/figure1.png)` in the markdown output.

## Approach 2: Direct `markitdown` Usage

For simple conversions without image organization, you can use `markitdown` directly.

### The CLI approach

#### Convert Offline HTML to Markdown

The simplest way to convert an offline HTML file to markdown using the CLI:

```bash
markitdown path-to-file.html
```

To save the output to a specific file:

```bash
markitdown path-to-file.html -o output.md
```

You can also pipe content:

**Bash:**
```bash
cat document.html | markitdown > output.md
```

**PowerShell:**
```powershell
Get-Content document.html | markitdown > output.md
```

**Examples:**

Convert a single HTML file:
```bash
markitdown research-paper.html -o research-paper.md
```

With pixi (if using pixi environment):
```bash
pixi run markitdown document.html -o document.md
```

Convert multiple files:

**Bash:**
```bash
# Convert multiple files (using shell globbing)
for file in *.html; do markitdown "$file" -o "${file%.html}.md"; done
```

**PowerShell:**
```powershell
# Convert multiple files (using PowerShell foreach)
Get-ChildItem *.html | ForEach-Object { markitdown $_.Name -o ($_.BaseName + ".md") }
```

### The Python approach

For more control and programmatic usage, you can use the Python API:

#### Basic HTML conversion

**Direct Python:**
```python
from markitdown import MarkItDown

# Initialize MarkItDown
md = MarkItDown()

# Convert HTML file
result = md.convert("path-to-file.html")
print(result.text_content)

# Save to file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

**With pixi:**
```bash
pixi run python -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('path-to-file.html')
with open('output.md', 'w', encoding='utf-8') as f:
    f.write(result.text_content)
print('Conversion completed')
"
```

#### Converting HTML with URL context

If you have an HTML file that was downloaded from a specific URL, you can provide the URL for better link resolution:

**Direct Python:**
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("wikipedia_page.html", url="https://en.wikipedia.org/wiki/Microsoft")
print(result.text_content)
```

**With pixi:**
```bash
pixi run python -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('wikipedia_page.html', url='https://en.wikipedia.org/wiki/Microsoft')
print(result.text_content)
"
```

#### Batch processing multiple HTML files

**Direct Python:**
```python
from markitdown import MarkItDown
import os
import glob

md = MarkItDown()

# Process all HTML files in a directory
html_files = glob.glob("*.html")
for html_file in html_files:
    try:
        result = md.convert(html_file)
        output_file = html_file.replace(".html", ".md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"Converted {html_file} to {output_file}")
    except Exception as e:
        print(f"Error converting {html_file}: {e}")
```

**With pixi (create a script file for complex operations):**
```bash
# Create batch_convert.py file first, then run:
pixi run python batch_convert.py
```

#### Error handling

**Direct Python:**
```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.html")
    if result.text_content:
        print("Conversion successful!")
        # Save or process the markdown content
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(result.text_content)
    else:
        print("Conversion resulted in empty content")
except Exception as e:
    print(f"Conversion failed: {e}")
```

**With pixi:**
```bash
pixi run python -c "
from markitdown import MarkItDown
md = MarkItDown()
try:
    result = md.convert('document.html')
    if result.text_content:
        with open('output.md', 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        print('Conversion successful!')
    else:
        print('Conversion resulted in empty content')
except Exception as e:
    print(f'Conversion failed: {e}')
"
``` 

## Converting Local PDFs to Markdown with Images

For local PDF files, you can use `markitdown` to convert them directly to markdown format while preserving embedded images. This is particularly useful for academic papers that contain figures, diagrams, and tables.

### Basic PDF Conversion

**Command Line Interface:**
```bash
# Simple PDF to markdown conversion
markitdown document.pdf -o output.md

# With pixi
pixi run markitdown document.pdf -o output.md

# Convert and save to paper subdirectory
markitdown research-paper.pdf -o tmp/papers/my-paper/paper-content.md
```

**PowerShell batch conversion:**
```powershell
# Convert all PDFs in a directory
Get-ChildItem *.pdf | ForEach-Object { 
    markitdown $_.Name -o ($_.BaseName + ".md") 
}
```

### Python API for PDF Conversion

**Basic PDF conversion:**
```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert PDF file
result = md.convert("research-paper.pdf")

# Save to paper subdirectory
import os
os.makedirs("tmp/papers/my-paper", exist_ok=True)
with open("tmp/papers/my-paper/paper-content.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

### Enhanced PDF Conversion with Image Descriptions

For better image handling, integrate with Large Language Models to generate descriptions:

```python
from markitdown import MarkItDown
from openai import OpenAI

# Configure with LLM for image descriptions
client = OpenAI()  # Requires OPENAI_API_KEY environment variable
md = MarkItDown(llm_client=client, llm_model="gpt-4o")

# Convert PDF with enhanced image processing
result = md.convert("academic-paper.pdf")
with open("tmp/papers/enhanced-paper/paper-content.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

### Azure Document Intelligence Integration

For complex academic papers with advanced layouts:

```python
from markitdown import MarkItDown

# Use Azure Document Intelligence (requires Azure endpoint)
md = MarkItDown(docintel_endpoint="<your_azure_endpoint>")
result = md.convert("complex-paper.pdf")
```

**CLI with Azure:**
```bash
markitdown document.pdf -o output.md -d -e "<azure_endpoint>"
```

### Manual Image Extraction Workflow

For PDFs where precise image handling is critical, combine `markitdown` with manual image extraction:

```python
import fitz  # PyMuPDF
from markitdown import MarkItDown
import os

def convert_pdf_with_manual_images(pdf_path, output_dir):
    """Convert PDF to markdown and extract images separately."""
    
    # Create output directory structure
    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Extract images with PyMuPDF
    pdf_doc = fitz.open(pdf_path)
    image_refs = []
    
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            pix = fitz.Pixmap(pdf_doc, xref)
            
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_filename = f"page_{page_num+1}_img_{img_index+1}.png"
                img_path = os.path.join(images_dir, img_filename)
                pix.save(img_path)
                image_refs.append(f"images/{img_filename}")
            
            pix = None
    
    pdf_doc.close()
    
    # Convert PDF to markdown with markitdown
    md = MarkItDown()
    result = md.convert(pdf_path)
    
    # Save markdown as paper-content.md
    markdown_path = os.path.join(output_dir, "paper-content.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)
        
        # Append extracted images section
        if image_refs:
            f.write("\n\n## Extracted Images\n\n")
            for img_ref in image_refs:
                f.write(f"![Image]({img_ref})\n\n")
    
    return markdown_path, image_refs

# Usage example
pdf_file = "research-paper.pdf"
output_directory = "tmp/papers/research-paper"
convert_pdf_with_manual_images(pdf_file, output_directory)
```

### Batch PDF Processing

**Process multiple PDFs with automatic organization:**
```python
import os
from markitdown import MarkItDown
from pathlib import Path

def batch_convert_pdfs(input_dir, paper_master_dir="tmp/papers"):
    """Convert all PDFs in directory to organized paper subdirectories."""
    
    md = MarkItDown()
    
    for pdf_file in Path(input_dir).glob("*.pdf"):
        try:
            # Create paper subdirectory
            paper_name = pdf_file.stem
            paper_subdir = os.path.join(paper_master_dir, paper_name)
            os.makedirs(paper_subdir, exist_ok=True)
            
            # Convert PDF
            result = md.convert(str(pdf_file))
            
            # Save as paper-content.md
            output_path = os.path.join(paper_subdir, "paper-content.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)
            
            print(f"Converted {pdf_file.name} to {output_path}")
            
        except Exception as e:
            print(f"Error converting {pdf_file.name}: {e}")

# Usage
batch_convert_pdfs("path/to/pdf/files")
```

### PDF Conversion Best Practices

1. **File Organization**: Always save converted files as `paper-content.md` in the paper subdirectory
2. **Image Handling**: For critical images, consider manual extraction or LLM-enhanced conversion
3. **Quality Check**: Review converted markdown for formatting issues, especially with complex layouts
4. **Backup Original**: Keep the original PDF file in the paper subdirectory for reference

### Error Handling for PDF Conversion

```python
from markitdown import MarkItDown
import os

def safe_pdf_convert(pdf_path, output_dir):
    """Safely convert PDF with comprehensive error handling."""
    
    try:
        # Validate input
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("Input file must be a PDF")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert PDF
        md = MarkItDown()
        result = md.convert(pdf_path)
        
        if not result.text_content.strip():
            print(f"Warning: No text content extracted from {pdf_path}")
            return None
        
        # Save result
        output_path = os.path.join(output_dir, "paper-content.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"Successfully converted {pdf_path} to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error converting PDF {pdf_path}: {e}")
        return None

# Usage
pdf_file = "research-paper.pdf"
output_dir = "tmp/papers/research-paper"
safe_pdf_convert(pdf_file, output_dir)
```

### Requirements for PDF Processing

Ensure you have the necessary dependencies installed:

```bash
# For basic PDF support
pip install markitdown[all]

# For enhanced image extraction (optional)
pip install PyMuPDF  # fitz

# With pixi
pixi add --pypi markitdown[all]
pixi add --pypi PyMuPDF
```

## How to Get HTML Online

For online papers or web pages, you can use the `download-html.py` script to download the web content to the `tmp` directory before converting to markdown.

Note that we will need to use `playwright` with `chromium` to download the HTML content, so ensure you have it installed. For the guide, see the script's documentation.

### Download Examples to tmp Directory

**Download HTML only to tmp:**
```bash
# Direct Python
python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/paper.html

# With pixi
pixi run python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/paper.html
```

**Download HTML with images to tmp:**
```bash
# Direct Python
python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/ --with-images

# With pixi
pixi run python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/ --with-images
```

**Download HTML with all resources to tmp:**
```bash
# Direct Python
python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/ --with-all

# With pixi
pixi run python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/ --with-all
```

**Auto-generate filename in tmp directory:**
```bash
# This will create a file like tmp/arxiv.org_abs_2401.12345.html
# Direct Python
python scripts/download-html.py -u https://arxiv.org/abs/2401.12345
mv arxiv.org_abs_2401.12345.html tmp/

# With pixi
pixi run python scripts/download-html.py -u https://arxiv.org/abs/2401.12345
Move-Item arxiv.org_abs_2401.12345.html tmp/
```

### Complete Workflow Example

Here's a complete example of downloading and converting an arXiv paper:

```bash
# Step 1: Download the HTML with images to tmp
pixi run python scripts/download-html.py -u https://arxiv.org/abs/2401.12345 -o tmp/genie3-paper/ --with-images

# Step 2: Convert to markdown (using Approach 1 below)
pixi run python scripts/convert-html-to-markdown.py -i ./tmp/genie3-paper -o ./genie3-survey-2024.md

# Step 3: Clean up temporary files (optional)
Remove-Item -Recurse -Force tmp/genie3-paper
```

## Useful links:

### arXiv html version

given a paper link like this: `https://arxiv.org/abs/2402.15391v1`, the html version can be found at `https://arxiv.org/html/2402.15391v1`, so the pattern is `https://arxiv.org/html/<arxiv_id>`, where `<arxiv_id>` is the part after `/abs/` in the original link.