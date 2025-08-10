# How to Use MarkItDown for PDF to Markdown Conversion with Images

This guide covers how to use Microsoft's MarkItDown tool to convert PDF files to Markdown format while preserving and properly linking images.

## Overview

MarkItDown is a Python utility developed by Microsoft that converts various file formats (PDF, DOCX, XLSX, HTML, images, audio) into Markdown. For PDFs, it can extract both text content and embedded images, making it suitable for academic papers and documents with visual content.

## Installation

### Basic Installation
```bash
# Install with all features
pip install 'markitdown[all]'

# Or install with specific features only
pip install 'markitdown[pdf, docx, pptx]'
```

### Virtual Environment Setup
```bash
# Standard Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or with conda
conda create -n markitdown python=3.12
conda activate markitdown
```

## Basic Usage

### Command Line Interface

**Simple PDF conversion:**
```bash
# Convert PDF to markdown (output to stdout)
markitdown document.pdf

# Save to specific file
markitdown document.pdf > output.md
markitdown document.pdf -o output.md

# Pipe content
cat document.pdf | markitdown > output.md
```

### Python API

**Basic conversion:**
```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert PDF file
result = md.convert("document.pdf")

# Access converted content
print(result.text_content)

# Save to file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

## Image Handling

### Current Limitations

⚠️ **Important**: As of the current version, MarkItDown has **limited built-in support for extracting and organizing images from PDFs**. The basic conversion primarily focuses on text extraction.

### Image Processing with LLM Integration

For better image handling, MarkItDown can integrate with Large Language Models to generate image descriptions:

```python
from markitdown import MarkItDown
from openai import OpenAI

# Configure with LLM for image descriptions
client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")

# Convert PDF with image descriptions
result = md.convert("document.pdf")
print(result.text_content)
```

### Azure Document Intelligence Integration

For enhanced PDF processing including better image extraction:

```python
from markitdown import MarkItDown

# Use Azure Document Intelligence
md = MarkItDown(docintel_endpoint="<your_azure_endpoint>")
result = md.convert("document.pdf")
```

**CLI with Azure:**
```bash
markitdown document.pdf -o output.md -d -e "<azure_endpoint>"
```

## Alternative Approaches for Images

### Using Third-Party Tools

For PDFs with important images, consider these alternatives:

1. **Marker** (vikparuchuri/marker) - Better PDF to Markdown with image preservation
2. **Manual extraction** - Extract images separately and reference them in markdown
3. **PDF to HTML first** - Convert PDF to HTML, then process HTML to markdown

### Manual Image Workflow

```python
import fitz  # PyMuPDF
from markitdown import MarkItDown
import os

def extract_pdf_with_images(pdf_path, output_dir):
    # Create output directory
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
    
    # Convert PDF to markdown
    md = MarkItDown()
    result = md.convert(pdf_path)
    
    # Save markdown with image references
    markdown_path = os.path.join(output_dir, "document.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)
        f.write("\n\n## Extracted Images\n\n")
        for img_ref in image_refs:
            f.write(f"![Image]({img_ref})\n\n")
    
    return markdown_path, image_refs
```

## Best Practices

### For Academic Papers

1. **Use HTML version when available** (e.g., arXiv HTML) for better image preservation
2. **Enable LLM integration** for image descriptions
3. **Consider Azure Document Intelligence** for complex layouts
4. **Post-process manually** for critical image placements

### File Organization

```
output/
├── document.md          # Main markdown file
├── images/             # Extracted images directory
│   ├── figure1.png
│   ├── table1.png
│   └── diagram1.png
└── original.pdf        # Keep original for reference
```

### Batch Processing

```python
import os
from markitdown import MarkItDown

def batch_convert_pdfs(input_dir, output_dir):
    md = MarkItDown()
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            result = md.convert(pdf_path)
            
            # Create output filename
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.md")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)
```

## Error Handling

```python
from markitdown import MarkItDown

def safe_convert(file_path):
    try:
        md = MarkItDown()
        result = md.convert(file_path)
        
        if result.text_content:
            return result.text_content
        else:
            print(f"Warning: No content extracted from {file_path}")
            return None
            
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return None
```

## Limitations and Considerations

### Current Limitations

- **Limited image extraction**: Basic PDF conversion focuses on text
- **Layout preservation**: Complex layouts may not convert perfectly
- **OCR dependency**: Scanned PDFs need pre-processing
- **Image quality**: Depends on source PDF quality

### When to Use Alternatives

- **Complex academic papers**: Consider HTML versions or specialized tools
- **Heavy image content**: Manual extraction may be necessary
- **Precise layout requirements**: PDF might be better kept as-is

## Related Tools

- **Marker**: Enhanced PDF to Markdown with better image support
- **Pandoc**: Alternative document converter
- **PyMuPDF**: For direct PDF manipulation and image extraction
- **PDF2image**: Convert PDF pages to images

## Source References

- [Microsoft MarkItDown GitHub Repository](https://github.com/microsoft/markitdown)
- [MarkItDown Documentation](https://github.com/microsoft/markitdown/blob/main/README.md)
- [Azure Document Intelligence](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/)
