import shutil
import json
from pathlib import Path

def copy_assignments_back():
    """Copy updated assignments back to extracted_course folders"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Check if assignment mapping exists
    mapping_file = Path('AVC185/assignment_mapping.json')
    if not mapping_file.exists():
        print("No assignment mapping found. Looking for corresponding folders...")
        copy_by_name_matching()
        return
    
    # Load mapping
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)
    
    # Create reverse mapping from assignment titles to files
    title_to_file = {}
    for assignment_file in assignments_path.glob('*.html'):
        title_to_file[assignment_file.name] = assignment_file
    
    for safe_name, info in mapping.items():
        # Try multiple filename variations
        possible_names = [
            f"{safe_name}.html",
            info['title'] + ".html",
            # Handle Week X format
            info['title'].replace("Week ", "Week ").replace(":", " -") + ".html"
        ]
        
        html_file = None
        for name in possible_names:
            test_file = assignments_path / name
            if test_file.exists():
                html_file = test_file
                break
        
        if not html_file:
            # Try fuzzy matching
            for file_name, file_path in title_to_file.items():
                if fuzzy_match(safe_name, file_name) or fuzzy_match(info['title'], file_name):
                    html_file = file_path
                    break
        
        if html_file and html_file.exists():
            dest_folder = extracted_path / info['original_folder']
            dest_file = dest_folder / info['original_html']
            
            if dest_folder.exists():
                shutil.copy2(html_file, dest_file)
                print(f"Copied {html_file.name} -> {dest_file}")
            else:
                print(f"Warning: Destination folder {dest_folder} not found")
        else:
            print(f"Warning: No matching file found for {safe_name} / {info['title']}")

def fuzzy_match(term1, term2):
    """Simple fuzzy matching for assignment names"""
    term1_clean = term1.lower().replace(' ', '').replace('-', '').replace('_', '')
    term2_clean = term2.lower().replace(' ', '').replace('-', '').replace('_', '').replace('.html', '')
    
    # Check if most characters match
    common_chars = sum(1 for c in term1_clean if c in term2_clean)
    return common_chars >= min(len(term1_clean), len(term2_clean)) * 0.7

def copy_by_name_matching():
    """Copy assignments by matching names when no mapping exists"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    if not extracted_path.exists():
        print(f"Error: {extracted_path} does not exist")
        return
    
    # Find assignment folders
    for assignment_file in assignments_path.glob('*.html'):
        assignment_name = assignment_file.stem.lower()
        
        # Look for matching folder based on name patterns
        for folder in extracted_path.iterdir():
            if folder.is_dir() and folder.name.startswith('g'):
                # Check for HTML files in folder
                html_files = list(folder.glob('*.html'))
                if html_files:
                    # Use the first HTML file found
                    dest_file = html_files[0]
                    
                    # Check if this might be the right assignment by looking at content
                    try:
                        content = dest_file.read_text(encoding='utf-8')
                        if is_matching_assignment(assignment_name, content):
                            shutil.copy2(assignment_file, dest_file)
                            print(f"Copied {assignment_file.name} -> {dest_file}")
                            break
                    except Exception as e:
                        print(f"Error reading {dest_file}: {e}")
                        continue

def is_matching_assignment(assignment_name, content):
    """Check if assignment name matches content"""
    
    # Extract key terms from assignment name
    name_terms = assignment_name.replace('-', ' ').replace('_', ' ').split()
    
    # Look for matching terms in content (title or H1)
    content_lower = content.lower()
    
    # Count matching terms
    matches = 0
    for term in name_terms:
        if term in content_lower and len(term) > 2:  # Skip very short terms
            matches += 1
    
    # Consider it a match if we find most of the key terms
    return matches >= len(name_terms) * 0.6

if __name__ == "__main__":
    copy_assignments_back()
    print("Assignment copying completed!")