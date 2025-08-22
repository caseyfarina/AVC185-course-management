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
                original_content = content
                
                # Fix namespace formatting
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
                    print(f"Fixed XML formatting: {xml_file}")

if __name__ == "__main__":
    fix_xml_formatting()