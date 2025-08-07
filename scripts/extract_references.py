import re
import os

def format_authors(author_line):
    authors = author_line.strip().replace(', et al.', '').split(', ')
    formatted_authors = []
    for author in authors:
        parts = author.split()
        if len(parts) > 1:
            # Take first initial of all but last name part
            initials = ''.join([p[0] + '.' for p in parts[:-1]])
            formatted_authors.append(f"{initials} {parts[-1]}")
        else:
            formatted_authors.append(author)
    return ", ".join(formatted_authors)

def parse_and_format_references(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the references section
    references_section = re.search(r'## References\n\n(.*?)(?=\n## Appendix A|\Z)', content, re.DOTALL)
    if not references_section:
        print("References section not found.")
        return

    references_text = references_section.group(1)
    
    # Split into individual reference blocks
    reference_blocks = re.split(r'\n\s*\*\s+', references_text)
    
    formatted_references = []
    for i, block in enumerate(reference_blocks):
        if not block.strip():
            continue

        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        # Skip header line like "Babuschkin et al. (2010)↑"
        if '↑' in lines[0]:
            lines = lines[1:]

        # Join lines to handle multiline titles or publication info
        full_text = " ".join(lines)

        # Simple extraction based on common patterns. This is heuristic.
        authors = ""
        title = ""
        publication = ""
        year = ""

        # Extract year from the header of the block
        year_match = re.search(r'\((\d{4})\)', block.split('\n')[0])
        if year_match:
            year = year_match.group(1)

        # First line is usually authors
        authors = lines[0].rstrip('.')
        
        # The rest is title and publication info
        remaining_text = " ".join(lines[1:])
        
        # Find title (often in quotes or the first sentence ending with a period)
        title_match = re.search(r'([A-Z].*?[\.|\?])\s*(In\s|\*|URL|http|$)', remaining_text)
        if title_match:
            title = title_match.group(1).strip()
            pub_start_index = remaining_text.find(title) + len(title)
            publication = remaining_text[pub_start_index:].strip()
        else: # fallback
            title = lines[1]
            publication = " ".join(lines[2:])

        # Clean up publication info
        publication = re.sub(r'\[.*?\]\(.*?\)', '', publication) # remove markdown links
        publication = publication.replace('URL ', '').strip()
        
        # Format into IEEE style
        # [i] A. Author, "Title," Publication, Year.
        f_authors = format_authors(authors)
        ieee_ref = f'[{i}] {f_authors}, "{title}," {publication}, {year}.'
        
        # Post-processing to clean up common issues
        ieee_ref = ieee_ref.replace('.,', ',')
        ieee_ref = re.sub(r'\s+', ' ', ieee_ref).strip()

        formatted_references.append(ieee_ref)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# References in IEEE Format\n\n")
        for ref in formatted_references:
            f.write(f"{ref}\n\n")

if __name__ == "__main__":
    # Correctly specify relative paths
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(workspace_dir, 'papers', 'genie-generative-interactive-environments-2024', 'paper.md')
    output_path = os.path.join(workspace_dir, 'papers', 'references.md')
    
    parse_and_format_references(input_path, output_path)
    print(f"References extracted and saved to {output_path}")