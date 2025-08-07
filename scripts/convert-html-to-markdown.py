#!/usr/bin/env python3
"""
HTML to Markdown Converter with Image Organization

This script converts HTML files to Markdown using markitdown and properly organizes
associated images with corrected relative paths. The output is a clean markdown file
with all image references pointing to an organized 'images/' directory.

Usage:
    python convert-html-to-markdown.py -i /path/to/input/dir -o /path/to/output/dir
    python convert-html-to-markdown.py --input /path/to/input/dir --output /path/to/output/dir

Requirements:
    - markitdown must be available in system PATH, or uvx/uv available as fallback
    - Install with: pipx install markitdown (recommended) or pip install markitdown
    - Alternative: install uv and use 'uvx markitdown' (automatic installation)
    - Input directory should contain HTML file(s) and optionally an images subdirectory

Output:
    - Clean markdown files with corrected image paths
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
from pathlib import Path
from typing import List, Optional, Tuple


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
        markdown_filename = "converted.md"
        markdown_file = output_dir / markdown_filename
    
    return output_dir, markdown_file, markdown_filename


def find_html_files(input_dir: Path) -> List[Path]:
    """Find all HTML files in the input directory."""
    html_files = []
    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.html', '.htm']:
            html_files.append(file_path)
    return html_files


def find_image_directories(input_dir: Path) -> List[Path]:
    """Find subdirectories that likely contain images."""
    image_dirs = []
    for item in input_dir.iterdir():
        if item.is_dir():
            # Check if directory contains image files
            image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}
            has_images = any(
                file.suffix.lower() in image_extensions 
                for file in item.iterdir() 
                if file.is_file()
            )
            if has_images:
                image_dirs.append(item)
    return image_dirs


def copy_images(image_dirs: List[Path], output_dir: Path) -> Path:
    """Copy all images to output directory and return the images directory path."""
    images_output_dir = output_dir / "images"
    
    # Clean existing directory if it exists
    if images_output_dir.exists():
        shutil.rmtree(images_output_dir)
    
    images_output_dir.mkdir(parents=True, exist_ok=True)
    
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}
    copied_count = 0
    
    for image_dir in image_dirs:
        print(f"Copying images from: {image_dir}")
        for file_path in image_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                destination = images_output_dir / file_path.name
                # Handle duplicate filenames by adding a suffix
                counter = 1
                original_destination = destination
                while destination.exists():
                    stem = original_destination.stem
                    suffix = original_destination.suffix
                    destination = images_output_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.copy2(file_path, destination)
                copied_count += 1
                print(f"  Copied: {file_path.name} -> {destination.name}")
    
    print(f"Total images copied: {copied_count}")
    return images_output_dir


def convert_html_to_markdown(html_file: Path, output_dir: Path, temp_dir: Path, markitdown_cmd: List[str]) -> Optional[Path]:
    """Convert HTML file to Markdown using markitdown."""
    temp_output_file = temp_dir / f"{html_file.stem}_temp.md"
    
    try:
        print(f"Converting: {html_file.name}")
        command = markitdown_cmd + [str(html_file), '-o', str(temp_output_file)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"Successfully converted to temporary file")
            return temp_output_file
        else:
            print(f"Error converting {html_file.name}: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Timeout while converting {html_file.name}")
        return None
    except Exception as e:
        print(f"Unexpected error converting {html_file.name}: {e}")
        return None


def fix_image_paths(temp_markdown_file: Path, image_dirs: List[Path], output_markdown_file: Path) -> Path:
    """Fix image paths in the markdown file and save as final clean version."""
    print(f"Fixing image paths and creating final output")
    
    with open(temp_markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create patterns for each image directory
    patterns_replacements = []
    
    for image_dir in image_dirs:
        dir_name = image_dir.name
        # Pattern to match image references to this directory
        # Matches: ![alt](./dirname/filename) or ![alt](dirname/filename)
        pattern = rf'!\[([^\]]*)\]\(\.?/?{re.escape(dir_name)}/([^)]+)\)'
        replacement = r'![\1](images/\2)'
        patterns_replacements.append((pattern, replacement))
    
    # Apply all patterns
    original_content = content
    for pattern, replacement in patterns_replacements:
        content = re.sub(pattern, replacement, content)
    
    # Also handle direct file references if they exist
    # Pattern for direct image file references
    image_extensions = r'\.(png|jpg|jpeg|gif|svg|webp|bmp)'
    direct_pattern = rf'!\[([^\]]*)\]\(\.?/?([^/\)]+{image_extensions})\)'
    content = re.sub(direct_pattern, r'![\1](images/\2)', content, flags=re.IGNORECASE)
    
    # Count changes made
    changes_made = len(re.findall(r'!\[[^\]]*\]\(images/', content))
    print(f"Fixed {changes_made} image references")
    
    # Create final clean output file
    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created final output: {output_markdown_file.name}")
    return output_markdown_file


def create_readme(output_dir: Path, converted_files: List[Path], images_dir: Optional[Path]):
    """Create a README file explaining the conversion results."""
    readme_path = output_dir / "README.md"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# HTML to Markdown Conversion Results\n\n")
        f.write("This directory contains the results of HTML to Markdown conversion.\n\n")
        
        f.write("## Converted Files\n\n")
        for file_path in converted_files:
            f.write(f"- `{file_path.name}`\n")
        
        if images_dir and images_dir.exists():
            image_count = len(list(images_dir.glob("*")))
            f.write(f"\n## Images\n\n")
            f.write(f"- **Location**: `images/` directory\n")
            f.write(f"- **Count**: {image_count} files\n")
            f.write("- All image references in the markdown files have been updated to point to this directory\n")
        
        f.write("\n## Notes\n\n")
        f.write("- All markdown files have corrected image paths pointing to the `images/` directory\n")
        f.write("- Image paths use relative references for portability\n")
    
    print(f"Created documentation: {readme_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML files to Markdown with proper image organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i ./paper-source -o ./output
  %(prog)s -i ./paper-source -o ./my-paper.md
  %(prog)s --input /path/to/html/files --output /path/to/output/dir
  %(prog)s -i ./source -o ./result.md --yes
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Input directory containing HTML file(s) and image subdirectories'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output directory or markdown filename. If directory, creates "converted.md". If filename ending with .md, uses that name.'
    )
    
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Answer yes to all prompts (non-interactive mode)'
    )
    
    parser.add_argument(
        '--keep-original-images',
        action='store_true',
        help='Keep original image directory structure (do not reorganize)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    input_dir = Path(args.input).resolve()
    
    # Determine output paths
    output_dir, output_markdown_file, markdown_filename = determine_output_paths(args.output)
    
    # Validate input directory
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}")
        sys.exit(1)
    
    # Check for existing files and get confirmation
    images_dir = output_dir / "images"
    
    if output_markdown_file.exists() and not confirm_overwrite(output_markdown_file, args.yes):
        print("Operation cancelled.")
        sys.exit(1)
    
    if images_dir.exists() and not confirm_overwrite(images_dir, args.yes):
        print("Operation cancelled.")
        sys.exit(1)
    
    # Check if markitdown is available and determine command to use
    print("Checking for markitdown availability...")
    markitdown_cmd, cmd_description = get_markitdown_command(args.yes)
    
    if not markitdown_cmd:
        print("Error: markitdown is not available")
        print("Please install markitdown using one of the following methods:")
        print("  pipx install markitdown  (recommended)")
        print("  pip install markitdown")
        print("  uv tool install markitdown")
        print("  Or install uv/uvx to use 'uvx markitdown'")
        sys.exit(1)
    
    print(f"✓ Will use: {cmd_description}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Find HTML files
    html_files = find_html_files(input_dir)
    if not html_files:
        print(f"Error: No HTML files found in {input_dir}")
        sys.exit(1)
    
    print(f"Found {len(html_files)} HTML file(s):")
    for html_file in html_files:
        print(f"  - {html_file.name}")
    
    # Find image directories
    image_dirs = find_image_directories(input_dir)
    print(f"Found {len(image_dirs)} image director(ies):")
    for img_dir in image_dirs:
        print(f"  - {img_dir.name}")
    
    # Copy images if found and not keeping original structure
    images_output_dir = None
    if image_dirs and not args.keep_original_images:
        images_output_dir = copy_images(image_dirs, output_dir)
    
    # Convert HTML files using temporary directory
    converted_files = []
    
    if len(html_files) > 1 and args.output.endswith('.md'):
        print("Warning: Multiple HTML files found, but output is a specific filename.")
        print("Only the first HTML file will be converted to the specified filename.")
        print("Other files will be skipped.")
        html_files = html_files[:1]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for i, html_file in enumerate(html_files):
            temp_converted_file = convert_html_to_markdown(html_file, output_dir, temp_path, markitdown_cmd)
            if temp_converted_file:
                # Determine the final output file
                if len(html_files) == 1 or args.output.endswith('.md'):
                    final_output_file = output_markdown_file
                else:
                    # Multiple files with directory output - use original naming
                    final_output_file = output_dir / f"{html_file.stem}.md"
                
                # Fix image paths and create final clean output
                if image_dirs and not args.keep_original_images:
                    final_file = fix_image_paths(temp_converted_file, image_dirs, final_output_file)
                    converted_files.append(final_file)
                else:
                    # If no image processing needed, just copy to final location
                    shutil.copy2(temp_converted_file, final_output_file)
                    converted_files.append(final_output_file)
                    print(f"Created final output: {final_output_file.name}")
    
    # Create documentation
    create_readme(output_dir, converted_files, images_output_dir)
    
    # Summary
    print("\n" + "="*60)
    print("CONVERSION SUMMARY")
    print("="*60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"HTML files processed: {len(converted_files)}")
    print(f"Successful conversions: {len(converted_files)}")
    
    if images_output_dir:
        image_count = len(list(images_output_dir.glob("*")))
        print(f"Images organized: {image_count}")
    
    print("\nFiles created:")
    for file_path in converted_files:
        print(f"  - {file_path.name}")
    
    print(f"\nSee {output_dir}/README.md for detailed information.")
    print("Conversion completed successfully!")


if __name__ == "__main__":
    main()
