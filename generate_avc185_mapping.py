import json
from pathlib import Path
import re

def generate_avc185_mapping():
    """Generate assignment mapping for AVC185"""
    
    extracted_path = Path('AVC185/extracted_course')
    assignments_path = Path('AVC185/assignments')
    
    assignment_mapping = {}
    
    # Find assignment folders (cryptic identifiers)
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g') and len(folder.name) > 20:
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                # Parse title from XML
                content = xml_file.read_text(encoding='utf-8')
                title_match = re.search(r'<title>(.*?)</title>', content)
                if title_match:
                    title = title_match.group(1)
                    print(f"Found assignment: {title}")
                    
                    # Find matching HTML file in assignments folder
                    for html_file in assignments_path.glob('*.html'):
                        html_name = html_file.stem.lower()
                        title_lower = title.lower()
                        
                        # Try to match based on content similarity
                        if any(word in html_name for word in title_lower.split() if len(word) > 3):
                            # Create safe filename
                            safe_name = re.sub(r'[^\w\s-]', '', title.lower())
                            safe_name = re.sub(r'[-\s]+', '_', safe_name)
                            
                            # Find HTML file in folder
                            for original_html in folder.glob('*.html'):
                                assignment_mapping[safe_name] = {
                                    'original_folder': folder.name,
                                    'original_html': original_html.name,
                                    'title': title,
                                    'assignments_file': html_file.name
                                }
                                print(f"  Mapped to: {html_file.name}")
                                break
                            break
    
    # Save mapping
    with open('AVC185/assignment_mapping.json', 'w') as f:
        json.dump(assignment_mapping, f, indent=2)
    
    print(f"\nGenerated mapping for {len(assignment_mapping)} AVC185 assignments")

if __name__ == "__main__":
    generate_avc185_mapping()