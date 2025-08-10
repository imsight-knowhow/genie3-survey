#!/usr/bin/env python3
"""
PDF to Markdown Converter with Image Extraction

This script converts PDF files to Markdown using markitdown and properly extracts
and organizes embedded images. The output is a clean markdown file with all image
references pointing to an organized 'images/' directory.

Author: AI Assistant
Version: 1.0
Date: 2024

Usage:
    python convert-pdf-to-markdown.py -i /path/to/input.pdf -o /path/to/output/dir
    python convert-pdf-to-markdown.py --input /path/to/pdfs/dir --output /path/to/output/dir

Requirements:
    - markitdown must be available in system PATH, or uvx/uv available as fallback
    - Install with: pipx install markitdown[all] (recommended) or pip install markitdown[all]
    - Alternative: install uv and use 'uvx markitdown' (automatic installation)
    - For enhanced image extraction: pip install PyMuPDF (fitz)
    - For LLM-enhanced image descriptions: OpenAI API key

Output:
    - Clean markdown files with extracted images
    - Organized images directory
    - README documentation
"""

import argparse
import os
import shutil
import subprocess
import sys
import re
import tempfile
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict

# Optional imports for enhanced features
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    fitz = None
    PYMUPDF_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False


def check_markitdown_available() -> bool:
    """Check if markitdown is available in system PATH."""
    try:
        result = subprocess.run(['markitdown', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_uvx_available() -> bool:
    """Check if uvx is available in system PATH."""
    try:
        result = subprocess.run(['uvx', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_markitdown_command(auto_yes: bool = False) -> Tuple[List[str], str]:
    """
    Determine the markitdown command to use.
    
    Returns:
        Tuple of (command_list, command_description)
    """
    # First try direct markitdown
    if check_markitdown_available():
        return (['markitdown'], 'markitdown')
    
    # If direct markitdown fails, try uvx as fallback
    if check_uvx_available():
        if auto_yes:
            print("markitdown not found directly, using 'uvx markitdown' (may install if not cached)")
            return (['uvx', 'markitdown'], 'uvx markitdown')
        else:
            print("markitdown is not directly available, but 'uvx' is detected.")
            print("This can run 'uvx markitdown' which may automatically install markitdown if needed.")
            if confirm_overwrite(Path("uvx-install-confirmation"), auto_yes):
                print("Using 'uvx markitdown'...")
                return (['uvx', 'markitdown'], 'uvx markitdown')
            else:
                print("User declined to use uvx. Please install markitdown manually.")
                return ([], '')
    
    # Neither available
    return ([], '')


def confirm_overwrite(path: Path, auto_yes: bool = False) -> bool:
    """Ask user for confirmation to overwrite existing file/directory or use uvx."""
    # Special case for uvx confirmation
    if path.name == "uvx-install-confirmation":
        if auto_yes:
            return True
        
        while True:
            response = input("Do you want to use 'uvx markitdown'? (This may install markitdown automatically) (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please answer 'y' or 'n'")
    
    # Regular file/directory overwrite confirmation
    if not path.exists():
        return True
    
    if auto_yes:
        print(f"Overwriting existing: {path}")
        return True
    
    while True:
        response = input(f"'{path}' already exists. Overwrite? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please answer 'y' or 'n'")


def determine_output_paths(output_arg: str) -> Tuple[Path, Path, str]:
    """
    Determine output directory, markdown file path, and filename from output argument.
    
    Returns:
        Tuple of (output_directory, markdown_file_path, markdown_filename)
    """
    output_path = Path(output_arg).resolve()
    
    if output_arg.endswith('.md'):
        # Output is a specific markdown filename
        markdown_file = output_path
        output_dir = markdown_file.parent
        markdown_filename = markdown_file.name
    else:
        # Output is a directory
        output_dir = output_path
        markdown_filename = "paper-content.md"
        markdown_file = output_dir / markdown_filename
    
    return output_dir, markdown_file, markdown_filename


def find_pdf_files(input_path: Path) -> List[Path]:
    """Find all PDF files in the input path (file or directory)."""
    pdf_files = []
    
    if input_path.is_file() and input_path.suffix.lower() == '.pdf':
        pdf_files.append(input_path)
    elif input_path.is_dir():
        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == '.pdf':
                pdf_files.append(file_path)
    
    return pdf_files


def extract_images_with_pymupdf(pdf_path: Path, images_dir: Path) -> List[str]:
    """Extract images from PDF using PyMuPDF and return list of image filenames."""
    if not PYMUPDF_AVAILABLE or fitz is None:
        print("PyMuPDF not available. Skipping manual image extraction.")
        return []
    
    print(f"Extracting images from PDF using PyMuPDF...")
    
    try:
        pdf_doc = fitz.open(str(pdf_path))
        image_refs = []
        
        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(pdf_doc, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_filename = f"page_{page_num+1}_img_{img_index+1}.png"
                    img_path = images_dir / img_filename
                    pix.save(str(img_path))
                    image_refs.append(img_filename)
                    print(f"  Extracted: {img_filename}")
                
                pix = None
        
        pdf_doc.close()
        print(f"Total images extracted: {len(image_refs)}")
        return image_refs
        
    except Exception as e:
        print(f"Error extracting images with PyMuPDF: {e}")
        return []


def convert_pdf_to_markdown(pdf_file: Path, output_dir: Path, temp_dir: Path, 
                          markitdown_cmd: List[str], use_llm: bool = False,
                          azure_endpoint: Optional[str] = None) -> Optional[Path]:
    """Convert PDF file to Markdown using markitdown."""
    temp_output_file = temp_dir / f"{pdf_file.stem}_temp.md"
    
    try:
        print(f"Converting: {pdf_file.name}")
        command = markitdown_cmd + [str(pdf_file), '-o', str(temp_output_file)]
        
        # Add Azure Document Intelligence if provided
        if azure_endpoint:
            command.extend(['-d', '-e', azure_endpoint])
            print(f"Using Azure Document Intelligence endpoint")
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"Successfully converted to temporary file")
            return temp_output_file
        else:
            print(f"Error converting {pdf_file.name}: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Timeout while converting {pdf_file.name}")
        return None
    except Exception as e:
        print(f"Unexpected error converting {pdf_file.name}: {e}")
        return None


def convert_pdf_with_python_api(pdf_file: Path, output_dir: Path, use_llm: bool = False,
                               azure_endpoint: Optional[str] = None) -> Optional[str]:
    """Convert PDF using Python API for enhanced features."""
    try:
        from markitdown import MarkItDown
        
        # Configure MarkItDown with optional features
        md_kwargs = {}
        
        if use_llm and OPENAI_AVAILABLE and OpenAI is not None:
            try:
                client = OpenAI()  # Uses OPENAI_API_KEY from environment
                md_kwargs['llm_client'] = client
                md_kwargs['llm_model'] = 'gpt-4o'
                print("Using LLM for enhanced image descriptions")
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
        
        if azure_endpoint:
            md_kwargs['docintel_endpoint'] = azure_endpoint
            print("Using Azure Document Intelligence")
        
        md = MarkItDown(**md_kwargs)
        
        print(f"Converting {pdf_file.name} using Python API...")
        result = md.convert(str(pdf_file))
        
        if result.text_content:
            return result.text_content
        else:
            print(f"Warning: No content extracted from {pdf_file.name}")
            return None
            
    except ImportError:
        print("markitdown not available for Python API. Using CLI instead.")
        return None
    except Exception as e:
        print(f"Error in Python API conversion: {e}")
        return None


def append_extracted_images(markdown_content: str, image_filenames: List[str]) -> str:
    """Append extracted images section to markdown content."""
    if not image_filenames:
        return markdown_content
    
    images_section = "\n\n## Extracted Images\n\n"
    for img_filename in image_filenames:
        images_section += f"![Image](images/{img_filename})\n\n"
    
    return markdown_content + images_section


def create_readme(output_dir: Path, converted_files: List[Path], images_dir: Optional[Path],
                 processing_info: Dict[str, str]):
    """Create a README file explaining the conversion results."""
    readme_path = output_dir / "README.md"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# PDF to Markdown Conversion Results\n\n")
        f.write("This directory contains the results of PDF to Markdown conversion.\n\n")
        
        f.write("## Converted Files\n\n")
        for file_path in converted_files:
            f.write(f"- `{file_path.name}`\n")
        
        if images_dir and images_dir.exists():
            image_count = len(list(images_dir.glob("*")))
            f.write(f"\n## Images\n\n")
            f.write(f"- **Location**: `images/` directory\n")
            f.write(f"- **Count**: {image_count} files\n")
            f.write("- Images were extracted from the PDF and organized in this directory\n")
        
        f.write("\n## Processing Information\n\n")
        for key, value in processing_info.items():
            f.write(f"- **{key}**: {value}\n")
        
        f.write("\n## Notes\n\n")
        f.write("- Markdown files contain the text content extracted from PDFs\n")
        f.write("- Image paths use relative references for portability\n")
        f.write("- For best results with complex layouts, consider using Azure Document Intelligence\n")
    
    print(f"Created documentation: {readme_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown with image extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i ./paper.pdf -o ./output
  %(prog)s -i ./pdfs/ -o ./converted/
  %(prog)s -i ./paper.pdf -o ./my-paper.md
  %(prog)s -i ./paper.pdf -o ./output --use-llm
  %(prog)s -i ./paper.pdf -o ./output --azure-endpoint "https://..."
  %(prog)s -i ./pdfs/ -o ./output --extract-images --yes

Features:
  - Basic PDF to Markdown conversion using markitdown
  - Enhanced image extraction with PyMuPDF (if available)
  - LLM-powered image descriptions (requires OpenAI API key)
  - Azure Document Intelligence integration (requires endpoint)
  - Automatic image organization and path correction
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Input PDF file or directory containing PDF files'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output directory or markdown filename. If directory, creates "paper-content.md". If filename ending with .md, uses that name.'
    )
    
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Answer yes to all prompts (non-interactive mode)'
    )
    
    parser.add_argument(
        '--extract-images',
        action='store_true',
        help='Extract images manually using PyMuPDF (requires PyMuPDF installation)'
    )
    
    parser.add_argument(
        '--use-llm',
        action='store_true',
        help='Use LLM for enhanced image descriptions (requires OpenAI API key in environment)'
    )
    
    parser.add_argument(
        '--azure-endpoint',
        type=str,
        help='Azure Document Intelligence endpoint for enhanced PDF processing'
    )
    
    parser.add_argument(
        '--use-python-api',
        action='store_true',
        help='Use Python API instead of CLI for enhanced features'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    input_path = Path(args.input).resolve()
    
    # Determine output paths
    output_dir, output_markdown_file, markdown_filename = determine_output_paths(args.output)
    
    # Validate input path
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)
    
    # Check for existing files and get confirmation
    images_dir = output_dir / "images"
    
    if output_markdown_file.exists() and not confirm_overwrite(output_markdown_file, args.yes):
        print("Operation cancelled.")
        sys.exit(1)
    
    if images_dir.exists() and not confirm_overwrite(images_dir, args.yes):
        print("Operation cancelled.")
        sys.exit(1)
    
    # Check optional dependencies
    if args.extract_images and not PYMUPDF_AVAILABLE:
        print("Warning: PyMuPDF not available. Manual image extraction disabled.")
        print("Install with: pip install PyMuPDF")
        args.extract_images = False
    
    if args.use_llm and not OPENAI_AVAILABLE:
        print("Warning: OpenAI package not available. LLM features disabled.")
        print("Install with: pip install openai")
        args.use_llm = False
    
    if args.use_llm and not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set. LLM features disabled.")
        args.use_llm = False
    
    # Check if markitdown is available (unless using Python API exclusively)
    markitdown_cmd = []
    cmd_description = ""
    
    if not args.use_python_api or args.azure_endpoint:
        print("Checking for markitdown availability...")
        markitdown_cmd, cmd_description = get_markitdown_command(args.yes)
        
        if not markitdown_cmd:
            print("Error: markitdown is not available")
            print("Please install markitdown using one of the following methods:")
            print("  pipx install markitdown[all]  (recommended)")
            print("  pip install markitdown[all]")
            print("  uv tool install markitdown")
            print("  Or install uv/uvx to use 'uvx markitdown'")
            sys.exit(1)
        
        print(f"✓ Will use: {cmd_description}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Find PDF files
    pdf_files = find_pdf_files(input_path)
    if not pdf_files:
        print(f"Error: No PDF files found in {input_path}")
        sys.exit(1)
    
    print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Create images directory if needed
    if args.extract_images:
        images_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert PDF files
    converted_files = []
    processing_info = {
        "Conversion Method": "Python API" if args.use_python_api else cmd_description,
        "Image Extraction": "PyMuPDF" if args.extract_images else "markitdown built-in",
        "LLM Enhancement": "Enabled" if args.use_llm else "Disabled",
        "Azure Integration": "Enabled" if args.azure_endpoint else "Disabled"
    }
    
    if len(pdf_files) > 1 and args.output.endswith('.md'):
        print("Warning: Multiple PDF files found, but output is a specific filename.")
        print("Only the first PDF file will be converted to the specified filename.")
        print("Other files will be skipped.")
        pdf_files = pdf_files[:1]
    
    for i, pdf_file in enumerate(pdf_files):
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_file.name}")
        print(f"{'='*60}")
        
        # Determine the final output file
        if len(pdf_files) == 1 or args.output.endswith('.md'):
            final_output_file = output_markdown_file
        else:
            # Multiple files with directory output - use original naming
            final_output_file = output_dir / f"{pdf_file.stem}.md"
        
        # Extract images manually if requested
        extracted_images = []
        if args.extract_images:
            file_images_dir = images_dir / pdf_file.stem if len(pdf_files) > 1 else images_dir
            file_images_dir.mkdir(parents=True, exist_ok=True)
            extracted_images = extract_images_with_pymupdf(pdf_file, file_images_dir)
        
        # Convert PDF to markdown
        markdown_content = None
        
        if args.use_python_api and not args.azure_endpoint:
            # Use Python API for enhanced features
            markdown_content = convert_pdf_with_python_api(
                pdf_file, output_dir, args.use_llm, args.azure_endpoint
            )
        
        if not markdown_content:
            # Fall back to CLI or use CLI for Azure
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                temp_converted_file = convert_pdf_to_markdown(
                    pdf_file, output_dir, temp_path, markitdown_cmd, 
                    args.use_llm, args.azure_endpoint
                )
                
                if temp_converted_file and temp_converted_file.exists():
                    with open(temp_converted_file, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
        
        if markdown_content:
            # Append extracted images if any
            if extracted_images:
                markdown_content = append_extracted_images(markdown_content, extracted_images)
            
            # Save final markdown file
            with open(final_output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            converted_files.append(final_output_file)
            print(f"✓ Created: {final_output_file.name}")
        else:
            print(f"✗ Failed to convert: {pdf_file.name}")
    
    # Create documentation
    create_readme(output_dir, converted_files, images_dir if args.extract_images else None, processing_info)
    
    # Summary
    print("\n" + "="*60)
    print("CONVERSION SUMMARY")
    print("="*60)
    print(f"Input path: {input_path}")
    print(f"Output directory: {output_dir}")
    print(f"PDF files found: {len(pdf_files)}")
    print(f"Successful conversions: {len(converted_files)}")
    
    if args.extract_images and images_dir.exists():
        image_count = len(list(images_dir.glob("**/*.png"))) + len(list(images_dir.glob("**/*.jpg")))
        print(f"Images extracted: {image_count}")
    
    print("\nFiles created:")
    for file_path in converted_files:
        print(f"  - {file_path.name}")
    
    if converted_files:
        print(f"\nSee {output_dir}/README.md for detailed information.")
        print("Conversion completed successfully!")
    else:
        print("\nNo files were successfully converted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
