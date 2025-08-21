#!/usr/bin/env python3
"""
Extract and display assignment due dates from IMSCC
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import json

def get_due_dates():
    """Extract due dates from all assignment settings"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    mapping_file = base_path / "assignment_mapping.json"
    
    # Load assignment mapping
    if not mapping_file.exists():
        print("Run extract_assignments.py first")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    assignments_with_dates = []
    
    for assignment_name, mapping_info in assignment_mapping.items():
        folder_path = extracted_path / mapping_info['original_folder']
        settings_file = folder_path / "assignment_settings.xml"
        
        if settings_file.exists():
            try:
                tree = ET.parse(settings_file)
                root = tree.getroot()
                
                # Extract data with namespace handling
                ns = {'cc': 'http://canvas.instructure.com/xsd/cccv1p0'}
                
                title = root.find('.//cc:title', ns)
                due_at = root.find('.//cc:due_at', ns) 
                all_day_date = root.find('.//cc:all_day_date', ns)
                points = root.find('.//cc:points_possible', ns)
                
                title_text = title.text if title is not None else assignment_name
                due_text = due_at.text if due_at is not None else None
                all_day_text = all_day_date.text if all_day_date is not None else None
                points_text = points.text if points is not None else "0"
                
                # Parse dates
                due_date = None
                if due_text:
                    try:
                        due_date = datetime.fromisoformat(due_text.replace('Z', '+00:00'))
                    except:
                        due_date = due_text
                
                all_day = None
                if all_day_text:
                    try:
                        all_day = datetime.fromisoformat(all_day_text).date()
                    except:
                        all_day = all_day_text
                
                assignments_with_dates.append({
                    'name': assignment_name,
                    'title': title_text,
                    'due_at': due_date,
                    'all_day_date': all_day,
                    'points': float(points_text) if points_text else 0,
                    'file': f"assignments/{assignment_name}.html"
                })
                
            except ET.ParseError as e:
                print(f"Error parsing {settings_file}: {e}")
    
    # Sort by due date
    assignments_with_dates.sort(key=lambda x: x['due_at'] or datetime.max)
    
    print("Assignment Due Dates")
    print("=" * 60)
    print()
    
    for i, assignment in enumerate(assignments_with_dates, 1):
        print(f"{i:2}. {assignment['title']}")
        
        if assignment['due_at']:
            if isinstance(assignment['due_at'], datetime):
                due_str = assignment['due_at'].strftime('%m/%d/%Y at %I:%M %p')
                day_str = assignment['due_at'].strftime('%A')
                print(f"    Due: {due_str} ({day_str})")
            else:
                print(f"    Due: {assignment['due_at']}")
        
        if assignment['all_day_date']:
            print(f"    All-day date: {assignment['all_day_date']}")
            
        print(f"    Points: {assignment['points']}")
        print(f"    File: {assignment['file']}")
        print()
    
    return assignments_with_dates

if __name__ == "__main__":
    get_due_dates()