from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

def update_avc200_due_dates():
    """Update AVC200 assignment due dates to match other courses"""
    extracted_path = Path('AVC200/extracted_course')
    
    # Due date schedule (Arizona time) - start September 2nd, 2025 at 8 PM
    start_date = datetime(2025, 9, 2, 20, 0)  # Tuesday September 2nd at 8 PM
    
    print(f"=== Updating AVC200 Due Dates ===")
    print(f"Start date: {start_date.strftime('%Y-%m-%d %H:%M')} (Arizona Time)")
    
    assignment_count = 0
    
    # Process all assignment folders
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                    if title_elem is not None:
                        title = title_elem.text
                        
                        # Calculate due date (assignment_count starts at 0 for week 1)
                        due_date = start_date + timedelta(weeks=assignment_count)
                        assignment_count += 1
                        
                        print(f"Assignment {assignment_count}: {title}")
                        print(f"  Due: {due_date.strftime('%Y-%m-%d %H:%M')} (Week {assignment_count})")
                        
                        # Update due date elements
                        due_at = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}due_at')
                        all_day_date = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}all_day_date')
                        
                        if due_at is not None:
                            due_at.text = due_date.strftime('%Y-%m-%dT%H:%M:%S')
                        if all_day_date is not None:
                            all_day_date.text = due_date.strftime('%Y-%m-%d')
                        
                        # Save the updated XML
                        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
                        
                except ET.ParseError as e:
                    print(f"Error parsing XML in {folder.name}: {e}")
                except Exception as e:
                    print(f"Error processing {folder.name}: {e}")
    
    print(f"\n=== Updated {assignment_count} assignments ===")
    print("Due date schedule:")
    for i in range(assignment_count):
        week_date = start_date + timedelta(weeks=i)
        print(f"  Week {i+1}: {week_date.strftime('%A, %B %d, %Y at %I:%M %p')}")

if __name__ == "__main__":
    update_avc200_due_dates()