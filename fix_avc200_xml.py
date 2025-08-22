import re
from pathlib import Path

def fix_avc200_xml_formatting():
    """Fix XML namespace formatting for AVC200 Canvas compatibility"""
    extracted_path = Path('AVC200/extracted_course')
    
    print("=== Fixing AVC200 XML Formatting ===")
    
    fixed_count = 0
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                content = xml_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix namespace formatting - Canvas expects specific format
                content = re.sub(
                    r'<ns0:assignment xmlns:ns0="http://canvas\.instructure\.com/xsd/cccv1p0"',
                    r'<assignment xmlns="http://canvas.instructure.com/xsd/cccv1p0"',
                    content
                )
                content = re.sub(r'</ns0:assignment>', r'</assignment>', content)
                content = re.sub(r'<ns0:([^>]+)>', r'<\1>', content)
                content = re.sub(r'</ns0:([^>]+)>', r'</\1>', content)
                
                if content != original_content:
                    xml_file.write_text(content, encoding='utf-8')
                    fixed_count += 1
                    print(f"  Fixed: {folder.name}")
    
    print(f"\n=== Fixed XML formatting in {fixed_count} assignments ===")

if __name__ == "__main__":
    fix_avc200_xml_formatting()