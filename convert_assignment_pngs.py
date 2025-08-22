import re
from pathlib import Path

def convert_assignment_pngs():
    """Convert PNG references to JPEG in AVC185 assignment files"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    conversions_made = 0
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Find and replace PNG references with JPEG
        png_pattern = r'(\$IMS-CC-FILEBASE\$/Uploaded%20Media/[^"]*?)\.png'
        content = re.sub(png_pattern, r'\1.jpg', content, flags=re.IGNORECASE)
        
        # Also handle any direct PNG references
        png_pattern2 = r'(src="[^"]*?)\.png(")'
        content = re.sub(png_pattern2, r'\1.jpg\2', content, flags=re.IGNORECASE)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            conversions_made += 1
            print(f"Updated {html_file.name}")
    
    print(f"\nConverted PNG references to JPEG in {conversions_made} assignment files")
    
    # Also update extracted_course files
    extracted_conversions = 0
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Find and replace PNG references with JPEG
                png_pattern = r'(\$IMS-CC-FILEBASE\$/Uploaded%20Media/[^"]*?)\.png'
                content = re.sub(png_pattern, r'\1.jpg', content, flags=re.IGNORECASE)
                
                # Also handle any direct PNG references
                png_pattern2 = r'(src="[^"]*?)\.png(")'
                content = re.sub(png_pattern2, r'\1.jpg\2', content, flags=re.IGNORECASE)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    extracted_conversions += 1
                    print(f"Updated {html_file}")
    
    print(f"Updated {extracted_conversions} files in extracted_course")
    
    return conversions_made + extracted_conversions

if __name__ == "__main__":
    total_conversions = convert_assignment_pngs()
    print(f"\nTotal files updated: {total_conversions}")
    print("\nNOTE: This script only changes file extensions in HTML references.")
    print("The actual PNG to JPEG conversion must be done by Canvas when uploading.")
    print("When re-uploading to Canvas, convert PNG files to JPEG format before upload.")