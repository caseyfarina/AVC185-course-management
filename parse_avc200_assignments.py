import json
from pathlib import Path
import shutil
import re
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_avc200_assignments():
    """Parse AVC200 assignments and order by due date"""
    extracted_path = Path('AVC200/extracted_course')
    assignments_path = Path('AVC200/assignments')
    assignments_path.mkdir(exist_ok=True)
    
    assignment_data = []
    assignment_mapping = {}
    
    print("=== Parsing AVC200 Assignments ===")
    
    # Find assignment folders (cryptic identifiers)
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g') and len(folder.name) > 20:
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Parse assignment details
                    title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                    due_at_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}due_at')
                    workflow_state_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}workflow_state')
                    
                    if title_elem is not None:
                        title = title_elem.text
                        due_date = due_at_elem.text if due_at_elem is not None else None
                        workflow_state = workflow_state_elem.text if workflow_state_elem is not None else 'unpublished'
                        
                        # Only process published assignments
                        if workflow_state == 'published':
                            # Parse due date
                            due_datetime = None
                            if due_date:
                                try:
                                    due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                                except:
                                    due_datetime = None
                            
                            # Find HTML files in assignment folder
                            html_files = list(folder.glob('*.html'))
                            if html_files:
                                html_file = html_files[0]
                                
                                assignment_data.append({
                                    'title': title,
                                    'due_date': due_date,
                                    'due_datetime': due_datetime,
                                    'workflow_state': workflow_state,
                                    'folder': folder.name,
                                    'html_file': html_file.name
                                })
                                
                                # Clean title for display
                                clean_title = title.encode('ascii', 'replace').decode('ascii')
                                print(f"Found: {clean_title}")
                                if due_datetime:
                                    print(f"  Due: {due_datetime.strftime('%Y-%m-%d %H:%M')}")
                                else:
                                    print(f"  Due: No due date")
                
                except ET.ParseError as e:
                    print(f"Error parsing XML in {folder.name}: {e}")
                except Exception as e:
                    print(f"Error processing {folder.name}: {e}")
    
    # Sort assignments by due date (None dates go to end)
    assignment_data.sort(key=lambda x: x['due_datetime'] if x['due_datetime'] else datetime.max)
    
    print(f"\n=== Assignment Order by Due Date ===")
    for i, assignment in enumerate(assignment_data, 1):
        clean_title = assignment['title'].encode('ascii', 'replace').decode('ascii')
        print(f"Week {i}: {clean_title}")
        if assignment['due_datetime']:
            print(f"  Due: {assignment['due_datetime'].strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"  Due: No due date")
    
    # Extract HTML files to assignments folder with week numbers
    for i, assignment in enumerate(assignment_data, 1):
        # Create safe filename
        original_title = assignment['title']
        safe_name = re.sub(r'[^\w\s-]', '', original_title.lower())
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        safe_name = f"week_{i}_{safe_name}"
        
        # Copy HTML file
        source_folder = extracted_path / assignment['folder']
        source_html = source_folder / assignment['html_file']
        dest_html = assignments_path / f"{safe_name}.html"
        
        if source_html.exists():
            shutil.copy2(source_html, dest_html)
            print(f"Extracted: {dest_html.name}")
            
            assignment_mapping[safe_name] = {
                'original_folder': assignment['folder'],
                'original_html': assignment['html_file'],
                'title': f"Week {i}: {original_title}",
                'original_title': original_title,
                'due_date': assignment['due_date'],
                'week_number': i
            }
    
    # Save mapping
    with open('AVC200/assignment_mapping.json', 'w') as f:
        json.dump(assignment_mapping, f, indent=2)
    
    print(f"\nExtracted {len(assignment_mapping)} published AVC200 assignments")
    return assignment_data

if __name__ == "__main__":
    parse_avc200_assignments()