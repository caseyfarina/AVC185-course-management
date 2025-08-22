import shutil
import zipfile
import os
from pathlib import Path

def extract_avc200():
    """Extract AVC200 IMSCC file"""
    # Find the AVC200 IMSCC file
    imscc_files = list(Path('.').glob('*avc200*.imscc'))
    if not imscc_files:
        print("No AVC200 IMSCC files found")
        return
    
    imscc_file = imscc_files[0]
    print(f"Found IMSCC file: {imscc_file.name}")
    
    zip_file = Path('AVC200') / 'temp_extract.zip'
    extract_path = Path('AVC200') / 'extracted_course'
    
    # Copy to zip format
    shutil.copy2(imscc_file, zip_file)
    
    # Extract
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    print(f"Extracted AVC200 to {extract_path}/")
    os.remove(zip_file)  # Clean up temp zip file

if __name__ == "__main__":
    extract_avc200()