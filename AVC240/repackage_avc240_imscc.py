import zipfile
from pathlib import Path
from datetime import datetime

def repackage_imscc():
    """Create new AVC240 IMSCC package"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'AVC240_AVCCCP_compliant_{timestamp}.imscc'
    
    extracted_path = Path('extracted_course')
    
    # Create IMSCC package
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in extracted_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(extracted_path)
                zipf.write(file_path, arcname)
    
    size_mb = Path(output_file).stat().st_size / (1024 * 1024)
    print(f"AVC240 IMSCC package created: {output_file}")
    print(f"Size: {size_mb:.1f} MB")

if __name__ == "__main__":
    repackage_imscc()