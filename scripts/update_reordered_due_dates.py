from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
import re

def update_reordered_due_dates():
    """Update due dates based on new week order"""
    extracted_path = Path('extracted_course')
    
    # Due date schedule (Arizona time)
    start_date = datetime(2025, 9, 2, 20, 0)  # First Tuesday at 8 PM
    tlc_date = datetime(2025, 8, 28, 20, 0)   # Thursday at 8 PM
    final_date = datetime(2025, 12, 16, 20, 0)  # Final Tuesday at 8 PM
    
    # New week order mapping with due date sequence
    week_due_dates = {
        1: start_date,  # Week 1 - Sept 2
        2: start_date + timedelta(weeks=1),  # Week 2 - Sept 9
        3: start_date + timedelta(weeks=2),  # Week 3 - Sept 16
        4: start_date + timedelta(weeks=3),  # Week 4 - Sept 23
        5: start_date + timedelta(weeks=4),  # Week 5 - Sept 30 (was week 14)
        6: start_date + timedelta(weeks=5),  # Week 6 - Oct 7 (was week 5)
        7: start_date + timedelta(weeks=6),  # Week 7 - Oct 14 (was week 6)
        8: start_date + timedelta(weeks=7),  # Week 8 - Oct 21 (was week 7)
        9: start_date + timedelta(weeks=8),  # Week 9 - Oct 28 (was week 8)
        10: start_date + timedelta(weeks=9),  # Week 10 - Nov 4 (was week 9)
        11: start_date + timedelta(weeks=10),  # Week 11 - Nov 11 (was week 10)
        12: start_date + timedelta(weeks=11),  # Week 12 - Nov 18 (was week 11)
        13: start_date + timedelta(weeks=12),  # Week 13 - Nov 25 (was week 12)
        14: start_date + timedelta(weeks=13),  # Week 14 - Dec 2 (was week 13)
    }
    
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                if title_elem is not None:
                    title = title_elem.text
                    
                    if 'Technology Login Challenge' in title or 'TLC' in title:
                        due_date = tlc_date
                    elif 'Final Portfolio' in title:
                        due_date = final_date
                    else:
                        # Extract week number from title
                        week_match = re.search(r'Week (\d+):', title)
                        if week_match:
                            week_num = int(week_match.group(1))
                            due_date = week_due_dates.get(week_num, start_date)
                        else:
                            due_date = start_date
                    
                    # Update due date elements
                    due_at = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}due_at')
                    all_day_date = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}all_day_date')
                    
                    if due_at is not None:
                        due_at.text = due_date.strftime('%Y-%m-%dT%H:%M:%S')
                    if all_day_date is not None:
                        all_day_date.text = due_date.strftime('%Y-%m-%d')
                    
                    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
                    print(f"Updated: {title} -> {due_date.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    update_reordered_due_dates()