# Canvas IMSCC Course Editing Workflow

## Overview
IMSCC (IMS Common Cartridge) is Canvas's course export format - essentially a ZIP file with XML metadata and HTML content files. This document outlines the complete workflow for editing Canvas courses via IMSCC files.

**Preferred Workflow**: The IMSCC → parse → edit → rebuild IMSCC workflow is the recommended approach for course content management. Previous experiments with GitHub Pages hosting and iframe embedding were discontinued due to security and accessibility concerns.

## Key Technical Concepts

### IMSCC Structure
- `.imscc` files are ZIP archives that can be extracted by renaming to `.zip`
- Contains XML metadata files and HTML content organized in folders
- Assignment folders use cryptic identifiers (e.g., `ga45c0a38ed19157066c2b34c30e682af`)
- Each assignment has `assignment_settings.xml` and HTML content files

### Critical XML Namespace Requirements
**IMPORTANT**: Canvas expects specific XML namespace formatting in assignment_settings.xml:
```xml
<assignment xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
```

Python's ElementTree changes this to `ns0:` prefixed format which breaks Canvas import. Always run XML formatting fix after ElementTree operations.

### Lecture Redirect Link System
Use permanent redirect links for YouTube lecture videos:
- Pattern: `https://caseyfarina.github.io/lecture-redirects/?class={CLASS}&lecture=week{N}-lecture{X}`
- Each week typically has 2 lectures (lecture1, lecture2)
- Final week uses `week15-lecture1` format (not "final-lecture1")
- Example: `https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=week1-lecture1`

## Complete Workflow Scripts

### 1. Extract IMSCC (`extract_imscc.py`)
```python
import shutil
import zipfile
import os
from pathlib import Path

def extract_imscc():
    """Extract IMSCC by copying to ZIP format first"""
    imscc_files = list(Path('.').glob('*.imscc'))
    if not imscc_files:
        print("No IMSCC files found")
        return
    
    imscc_file = imscc_files[0]
    zip_file = imscc_file.with_suffix('.zip')
    
    # Copy to zip format
    shutil.copy2(imscc_file, zip_file)
    
    # Extract
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('extracted_course')
    
    print(f"Extracted to extracted_course/")
    os.remove(zip_file)  # Clean up temp zip file

if __name__ == "__main__":
    extract_imscc()
```

### 2. Extract Assignments (`extract_assignments.py`)
```python
import json
from pathlib import Path
import shutil
import re

def extract_assignments():
    """Extract assignments to organized structure"""
    extracted_path = Path('extracted_course')
    assignments_path = Path('assignments')
    assignments_path.mkdir(exist_ok=True)
    
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
                    # Create safe filename
                    safe_name = re.sub(r'[^\w\s-]', '', title.lower())
                    safe_name = re.sub(r'[-\s]+', '_', safe_name)
                    
                    # Copy HTML files
                    for html_file in folder.glob('*.html'):
                        dest_file = assignments_path / f"{safe_name}.html"
                        shutil.copy2(html_file, dest_file)
                        
                        assignment_mapping[safe_name] = {
                            'original_folder': folder.name,
                            'original_html': html_file.name,
                            'title': title
                        }
                        break
    
    # Save mapping
    with open('assignment_mapping.json', 'w') as f:
        json.dump(assignment_mapping, f, indent=2)
    
    print(f"Extracted {len(assignment_mapping)} assignments")

if __name__ == "__main__":
    extract_assignments()
```

### 3. Update Due Dates (`update_due_dates.py`)
```python
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
import json

def update_due_dates():
    """Update assignment due dates"""
    extracted_path = Path('extracted_course')
    
    # Due date schedule (Arizona time)
    start_date = datetime(2025, 9, 2, 20, 0)  # First Tuesday at 8 PM
    tlc_date = datetime(2025, 8, 28, 20, 0)   # Thursday at 8 PM
    final_date = datetime(2025, 12, 16, 20, 0)  # Final Tuesday at 8 PM
    
    assignment_count = 0
    
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
                        # Regular assignment - Tuesdays starting Sept 2
                        due_date = start_date + timedelta(weeks=assignment_count)
                        assignment_count += 1
                    
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
    update_due_dates()
```

### 4. Add Week Numbers (`add_week_numbers.py`)
```python
from pathlib import Path
import xml.etree.ElementTree as ET
import re

def add_week_numbers():
    """Add Week N: prefixes to assignments 1-14"""
    extracted_path = Path('extracted_course')
    
    # Assignment patterns to week mapping
    week_patterns = [
        (r'introduction.*blender', 1),
        (r'bezier.*curves', 2),
        (r'uv.*unwrapping', 3),
        (r'modeling.*scale', 4),
        (r'materials.*hard.*surface', 5),
        (r'kitchen.*modeling.*table', 6),
        (r'kitchen.*plates', 7),
        (r'kitchen.*modeling.*silverware', 8),
        (r'modifiers.*rendering', 9),
        (r'substance.*painter.*techniques', 10),
        (r'introduction.*substance.*painter', 11),
        (r'lamp.*revisions', 12),
        (r'modeling.*foliage', 13),
        (r'rendering.*compositing', 14)
    ]
    
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                if title_elem is not None:
                    title = title_elem.text.lower()
                    
                    # Skip TLC and Final Portfolio
                    if 'technology login challenge' in title or 'final portfolio' in title:
                        continue
                    
                    # Find matching week
                    for pattern, week_num in week_patterns:
                        if re.search(pattern, title):
                            new_title = f"Week {week_num}: {title_elem.text}"
                            title_elem.text = new_title
                            tree.write(xml_file, encoding='utf-8', xml_declaration=True)
                            print(f"Updated: {new_title}")
                            break

if __name__ == "__main__":
    add_week_numbers()
```

### 5. Replace YouTube Links (`replace_youtube_links.py`)
```python
import re
from pathlib import Path
import json

def replace_youtube_links():
    """Replace YouTube links with redirect links"""
    assignments_path = Path('assignments')
    
    with open('assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    # Week number patterns
    week_patterns = [
        (r'week.*1', 1), (r'introduction.*blender', 1),
        (r'week.*2', 2), (r'bezier.*curves', 2),
        (r'week.*3', 3), (r'uv.*unwrapping', 3),
        # ... continue pattern for all weeks
        (r'final.*portfolio', 15)
    ]
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        # Determine week number
        week_num = 1
        filename_lower = html_file.stem.lower()
        for pattern, num in week_patterns:
            if re.search(pattern, filename_lower):
                week_num = num
                break
        
        # Replace YouTube links (first two only)
        youtube_count = 0
        def replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                class_code = "avc185"  # Adjust per course
                lecture_num = youtube_count
                return f'<a href="https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}" target="_blank">https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}</a>'
            return match.group(0)
        
        # Pattern for YouTube links
        youtube_pattern = r'<a[^>]*href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>https://www\.youtube\.com/watch\?v=[^<]*</a>'
        new_content = re.sub(youtube_pattern, replacement_func, content)
        
        if new_content != content:
            html_file.write_text(new_content, encoding='utf-8')
            print(f"Updated {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    replace_youtube_links()
```

### 6. XML Formatting Fix (`fix_xml_formatting.py`)
```python
import re
from pathlib import Path

def fix_xml_formatting():
    """Fix XML namespace formatting for Canvas compatibility"""
    extracted_path = Path('extracted_course')
    
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                content = xml_file.read_text(encoding='utf-8')
                
                # Fix namespace formatting
                content = re.sub(
                    r'<ns0:assignment xmlns:ns0="http://canvas\.instructure\.com/xsd/cccv1p0"',
                    r'<assignment xmlns="http://canvas.instructure.com/xsd/cccv1p0"',
                    content
                )
                content = re.sub(r'</ns0:assignment>', r'</assignment>', content)
                content = re.sub(r'<ns0:([^>]+)>', r'<\1>', content)
                content = re.sub(r'</ns0:([^>]+)>', r'</\1>', content)
                
                xml_file.write_text(content, encoding='utf-8')

if __name__ == "__main__":
    fix_xml_formatting()
```

### 7. Repackage IMSCC (`repackage_imscc.py`)
```python
import zipfile
import json
from pathlib import Path
import shutil
from datetime import datetime

def repackage_imscc():
    """Create new IMSCC package"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'updated_course_{timestamp}.imscc'
    
    # Copy assignments back
    assignments_path = Path('assignments')
    extracted_path = Path('extracted_course')
    
    if Path('assignment_mapping.json').exists():
        with open('assignment_mapping.json', 'r') as f:
            mapping = json.load(f)
        
        for safe_name, info in mapping.items():
            html_file = assignments_path / f"{safe_name}.html"
            if html_file.exists():
                dest_folder = extracted_path / info['original_folder']
                dest_file = dest_folder / info['original_html']
                shutil.copy2(html_file, dest_file)
            else:
                print(f"Warning: {html_file.name} not found in assignments folder")
    
    # Create IMSCC package
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in extracted_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(extracted_path)
                zipf.write(file_path, arcname)
    
    size_mb = Path(output_file).stat().st_size / (1024 * 1024)
    print(f"IMSCC package created: {output_file}")
    print(f"Size: {size_mb:.1f} MB")

if __name__ == "__main__":
    repackage_imscc()
```

## Complete Workflow Steps

1. **Extract IMSCC**: `python extract_imscc.py`
2. **Extract Assignments**: `python extract_assignments.py`
3. **Update Due Dates**: `python update_due_dates.py`
4. **Add Week Numbers**: `python add_week_numbers.py`
5. **Replace YouTube Links**: `python replace_youtube_links.py`
6. **Fix XML Formatting**: `python fix_xml_formatting.py` (CRITICAL)
7. **Repackage**: `python repackage_imscc.py`

## Common Issues & Solutions

### Missing Assignments After Import
- **Cause**: XML namespace formatting incompatibility
- **Solution**: Always run `fix_xml_formatting.py` after any XML modifications

### Encoding Issues
- Use UTF-8 encoding for all file operations
- Replace Unicode symbols with ASCII in console output

### File Reference Tokens
- Preserve `$IMS-CC-FILEBASE$` tokens in HTML for Canvas resource linking
- Don't modify these during content updates

## Course-Specific Customizations

When adapting for other courses:
- Update class code in YouTube redirect links
- Modify week patterns in `add_week_numbers.py`
- Adjust due date schedules in `update_due_dates.py`
- Update assignment group references if needed

## Testing
Always test IMSCC imports in Canvas with a backup course before deploying to live courses.