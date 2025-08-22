#!/usr/bin/env python3
"""
Comprehensive Image Analysis Report for AVC185 Course
Analyzes all image files and references in the course materials.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def find_all_images():
    """Find all physical image files in the course directories."""
    base_path = Path(r"F:\GCC canvas work\AVC185-course-management\AVC185")
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.tiff', '.tif']
    
    physical_images = []
    
    for ext in image_extensions:
        for img_file in base_path.glob(f"**/*{ext}"):
            physical_images.append({
                'path': str(img_file),
                'filename': img_file.name,
                'extension': ext,
                'size_bytes': img_file.stat().st_size if img_file.exists() else 0,
                'folder': str(img_file.parent.relative_to(base_path))
            })
    
    return physical_images

def extract_html_image_references():
    """Extract all image references from HTML files."""
    base_path = Path(r"F:\GCC canvas work\AVC185-course-management\AVC185")
    
    image_references = []
    
    # Find all HTML files
    html_files = list(base_path.glob("**/*.html"))
    
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Find img tags
            img_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            for src, alt in matches:
                # Check if it's an IMS-CC-FILEBASE reference
                if '$IMS-CC-FILEBASE$' in src:
                    # Extract the actual filename
                    filename_match = re.search(r'/([^/]+\.(png|jpg|jpeg|gif|webp|svg))[\?"]', src)
                    if filename_match:
                        filename = filename_match.group(1).replace('%20', ' ')
                        extension = filename_match.group(2).lower()
                    else:
                        filename = src.split('/')[-1].replace('%20', ' ')
                        extension = 'unknown'
                        if '.' in filename:
                            extension = filename.split('.')[-1].lower()
                
                    image_references.append({
                        'html_file': str(html_file.relative_to(base_path)),
                        'src': src,
                        'alt_text': alt,
                        'filename': filename,
                        'extension': extension,
                        'is_canvas_upload': True
                    })
                else:
                    # Direct file reference
                    filename = os.path.basename(src)
                    extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
                    
                    image_references.append({
                        'html_file': str(html_file.relative_to(base_path)),
                        'src': src,
                        'alt_text': alt,
                        'filename': filename,
                        'extension': extension,
                        'is_canvas_upload': False
                    })
                    
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    return image_references

def analyze_alt_text_quality(alt_text):
    """Analyze the quality of alt text."""
    if not alt_text or alt_text.strip() == "":
        return "Missing"
    
    alt_lower = alt_text.lower().strip()
    
    # Generic/inadequate alt text patterns
    generic_patterns = [
        r'^image$',
        r'^picture$',
        r'^photo$',
        r'^screenshot$',
        r'^img_\d+$',
        r'^image-[a-f0-9-]+$',
        r'^untitled$',
        r'^\d+$',
        r'^[a-f0-9-]+$'
    ]
    
    for pattern in generic_patterns:
        if re.match(pattern, alt_lower):
            return "Generic/Inadequate"
    
    # Short but potentially adequate
    if len(alt_text.strip()) < 10:
        return "Too Short"
    
    # Good descriptive alt text
    if len(alt_text.strip()) >= 10:
        return "Adequate"
    
    return "Needs Review"

def generate_report():
    """Generate comprehensive image analysis report."""
    print("=== AVC185 Course Image Analysis Report ===\n")
    
    # Find physical images
    print("1. PHYSICAL IMAGE FILES")
    print("=" * 50)
    
    physical_images = find_all_images()
    
    # Group by extension
    by_extension = defaultdict(list)
    for img in physical_images:
        by_extension[img['extension']].append(img)
    
    total_images = len(physical_images)
    print(f"Total physical image files found: {total_images}\n")
    
    for ext, images in sorted(by_extension.items()):
        print(f"{ext.upper()} files: {len(images)}")
        for img in sorted(images, key=lambda x: x['filename']):
            size_kb = img['size_bytes'] / 1024
            print(f"  - {img['filename']} ({size_kb:.1f} KB) - {img['folder']}")
        print()
    
    # Extract HTML references
    print("\n2. HTML IMAGE REFERENCES")
    print("=" * 50)
    
    html_refs = extract_html_image_references()
    
    print(f"Total image references in HTML: {len(html_refs)}\n")
    
    # Group by file and analyze
    canvas_uploads = [ref for ref in html_refs if ref['is_canvas_upload']]
    direct_refs = [ref for ref in html_refs if not ref['is_canvas_upload']]
    
    print(f"Canvas uploaded images (via $IMS-CC-FILEBASE$): {len(canvas_uploads)}")
    print(f"Direct file references: {len(direct_refs)}\n")
    
    # Analyze Canvas uploads
    if canvas_uploads:
        print("CANVAS UPLOADED IMAGES:")
        print("-" * 30)
        
        # Get unique images
        unique_canvas_images = {}
        for ref in canvas_uploads:
            key = ref['filename']
            if key not in unique_canvas_images:
                unique_canvas_images[key] = []
            unique_canvas_images[key].append(ref)
        
        for filename, refs in sorted(unique_canvas_images.items()):
            ref = refs[0]  # Use first reference for details
            alt_quality = analyze_alt_text_quality(ref['alt_text'])
            
            print(f"FILE: {filename} ({ref['extension'].upper()})")
            print(f"   Alt text: \"{ref['alt_text']}\"")
            print(f"   Quality: {alt_quality}")
            print(f"   Used in {len(refs)} file(s):")
            for r in refs:
                print(f"     - {r['html_file']}")
            print()
    
    # PNG files that need conversion
    print("\n3. PNG FILES REQUIRING JPEG CONVERSION")
    print("=" * 50)
    
    png_files = [img for img in physical_images if img['extension'] == '.png']
    png_refs = [ref for ref in canvas_uploads if ref['extension'] == 'png']
    
    print(f"Physical PNG files: {len(png_files)}")
    for png in png_files:
        print(f"  - {png['filename']} - {png['folder']}")
    
    print(f"\nCanvas PNG references: {len(png_refs)}")
    png_names = set()
    for ref in png_refs:
        if ref['filename'] not in png_names:
            png_names.add(ref['filename'])
            print(f"  - {ref['filename']}")
    
    print(f"\nTotal unique PNG files needing conversion: {len(png_files) + len(png_names)}")
    
    # Alt text analysis
    print("\n4. ALT TEXT QUALITY ANALYSIS")
    print("=" * 50)
    
    alt_quality_stats = defaultdict(int)
    problematic_alt_text = []
    
    for ref in html_refs:
        quality = analyze_alt_text_quality(ref['alt_text'])
        alt_quality_stats[quality] += 1
        
        if quality in ['Missing', 'Generic/Inadequate', 'Too Short']:
            problematic_alt_text.append({
                'filename': ref['filename'],
                'alt_text': ref['alt_text'],
                'quality': quality,
                'html_file': ref['html_file']
            })
    
    print("Alt text quality distribution:")
    for quality, count in sorted(alt_quality_stats.items()):
        print(f"  {quality}: {count}")
    
    if problematic_alt_text:
        print(f"\nImages with problematic alt text ({len(problematic_alt_text)}):")
        for item in problematic_alt_text:
            print(f"  - {item['filename']} - {item['quality']}")
            print(f"    Current: \"{item['alt_text']}\"")
            print(f"    File: {item['html_file']}")
            print()
    
    # Recommendations
    print("\n5. RECOMMENDATIONS")
    print("=" * 50)
    
    print("IMMEDIATE ACTIONS NEEDED:")
    print("1. Convert PNG to JPEG:")
    all_pngs = set()
    all_pngs.update([img['filename'] for img in png_files])
    all_pngs.update([ref['filename'] for ref in png_refs])
    
    for png_name in sorted(all_pngs):
        print(f"   - {png_name}")
    
    print(f"\n2. Improve alt text for {len(problematic_alt_text)} images")
    print("3. Ensure all images have descriptive, meaningful alt text")
    print("4. Consider file size optimization for large images")
    
    # File summary
    print(f"\nFILE SUMMARY:")
    print(f"- Total physical images: {total_images}")
    print(f"- Total HTML references: {len(html_refs)}")
    print(f"- PNG files to convert: {len(all_pngs)}")
    print(f"- Images needing alt text improvement: {len(problematic_alt_text)}")

if __name__ == "__main__":
    generate_report()