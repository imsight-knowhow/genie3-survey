you are tasked to convert an academic paper into a markdown format. Follow these guidelines:

# Guidelines for Converting Paper to Markdown

## File Handling

by default, save the converted markdown file in the root of the workspace, unless specified otherwise, name it as `paper-title-year.md`, where `paper-title` is the title of the paper in lowercase, with spaces replaced by hyphens, `year` is the publication year of the paper. If the file already exists, append a number to the filename (e.g., `paper-title-year-1.md`, `paper-title-year-2.md`, etc.). Figures should be saved in a subdirectory following with the same name as the markdown file, unless you are using the utility script which will handle image organization automatically.

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

# With pixi
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

