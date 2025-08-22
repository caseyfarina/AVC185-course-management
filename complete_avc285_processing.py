import re
from pathlib import Path
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import shutil

def update_avc285_youtube_links():
    """Replace YouTube links with AVC285 redirect links"""
    assignments_path = Path('AVC285/assignments')
    
    with open('AVC285/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    print("=== Updating AVC285 YouTube Links ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        week_num = info['week_number']
        
        print(f"\nProcessing: {html_file.name} (Week {week_num})")
        
        # Replace YouTube links (first two only per assignment)
        youtube_count = 0
        def replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                class_code = "avc285"
                lecture_num = youtube_count
                new_url = f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
                print(f"  Replaced YouTube link {youtube_count}: week{week_num}-lecture{lecture_num}")
                return f'<a href="{new_url}" target="_blank">{new_url}</a>'
            return match.group(0)
        
        # Pattern for YouTube links in anchor tags
        youtube_pattern = r'<a[^>]*href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>https://www\.youtube\.com/watch\?v=[^<]*</a>'
        new_content = re.sub(youtube_pattern, replacement_func, content)
        
        # Also handle direct YouTube URLs not in anchor tags
        if youtube_count < 2:
            def direct_url_replacement(match):
                nonlocal youtube_count
                youtube_count += 1
                if youtube_count <= 2:
                    class_code = "avc285"
                    lecture_num = youtube_count
                    new_url = f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
                    print(f"  Replaced direct YouTube URL {youtube_count}: week{week_num}-lecture{lecture_num}")
                    return f'<a href="{new_url}" target="_blank">{new_url}</a>'
                return match.group(0)
            
            # Pattern for direct YouTube URLs
            direct_youtube_pattern = r'https://www\.youtube\.com/watch\?v=[^\s<>"\)]+(?:\s|<|$)'
            new_content = re.sub(direct_youtube_pattern, direct_url_replacement, new_content)
        
        # Write back if changes were made
        if new_content != original_content:
            html_file.write_text(new_content, encoding='utf-8')
            print(f"  Updated {html_file.name}")
        else:
            print(f"  No YouTube links found in {html_file.name}")

def generate_avc285_alt_text():
    """Generate descriptive alt text for AVC285 images"""
    assignments_path = Path('AVC285/assignments')
    
    with open('AVC285/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    print("\n=== Generating AVC285 Alt Text ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        week_num = info['week_number']
        title = info['original_title']
        
        print(f"\nProcessing: {html_file.name} - {title}")
        
        # Generate context-aware alt text based on assignment content
        def generate_alt_text(title, week_num):
            title_lower = title.lower()
            
            if 'simulation' in title_lower and 'rigid' in title_lower:
                return "Rigid body physics simulation demonstration or interface"
            elif 'simulation' in title_lower and 'fracture' in title_lower:
                return "Fracture simulation and art direction example"
            elif 'simulation' in title_lower and 'cloth' in title_lower:
                return "Cloth simulation physics demonstration or workflow"
            elif 'twinmotion' in title_lower:
                return "TwinMotion interface or architectural visualization"
            elif 'substance painter' in title_lower:
                return "Substance Painter interface or texturing workflow"
            elif 'substance sampler' in title_lower:
                return "Substance Sampler material creation interface"
            elif 'photogrammetry' in title_lower:
                return "Photogrammetry scanning process or 3D reconstruction"
            elif 'sculpting' in title_lower and 'blender' in title_lower:
                return "Blender sculpting interface or digital sculpture example"
            elif 'vdm' in title_lower or 'brush' in title_lower:
                return "VDM brush techniques or displacement sculpting example"
            elif 'unreal' in title_lower:
                return "Unreal Engine interface or real-time rendering example"
            else:
                return "Course instructional image or 3D modeling tutorial"
        
        # Replace generic alt text with descriptive alt text
        alt_text = generate_alt_text(title, week_num)
        
        # Pattern to find images with generic alt text
        generic_patterns = [
            r'alt="[^"]*\.png"',
            r'alt="[^"]*\.jpg"',
            r'alt="[^"]*\.jpeg"',
            r'alt="image[^"]*"',
            r'alt="Image[^"]*"',
            r'alt=""',
            r'alt="[^"]{1,10}"'  # Very short alt text likely generic
        ]
        
        updated = False
        for pattern in generic_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, f'alt="{alt_text}"', content)
                updated = True
        
        # Write back if changes were made
        if updated and content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  Updated alt text: {alt_text}")
        else:
            print(f"  No generic alt text found or already descriptive")

def update_avc285_due_dates():
    """Update AVC285 assignment due dates to Tuesday schedule starting Sep 2"""
    extracted_path = Path('AVC285/extracted_course')
    
    # Due date schedule (Arizona time) - start September 2nd, 2025 at 8 PM
    start_date = datetime(2025, 9, 2, 20, 0)  # Tuesday September 2nd at 8 PM
    
    print(f"\n=== Updating AVC285 Due Dates ===")
    print(f"Start date: {start_date.strftime('%Y-%m-%d %H:%M')} (Arizona Time)")
    
    # Load mapping to get correct order
    with open('AVC285/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    # Create a mapping from original folder to week number
    folder_to_week = {}
    for safe_name, info in mapping.items():
        folder_to_week[info['original_folder']] = info['week_number']
    
    assignment_count = 0
    
    # Process all assignment folders in the extracted course
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists() and folder.name in folder_to_week:
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                    if title_elem is not None:
                        title = title_elem.text
                        
                        # Get week number from mapping
                        week_num = folder_to_week[folder.name]
                        due_date = start_date + timedelta(weeks=week_num - 1)
                        assignment_count += 1
                        
                        print(f"Week {week_num}: {title}")
                        print(f"  Due: {due_date.strftime('%Y-%m-%d %H:%M')}")
                        
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

def fix_avc285_xml_formatting():
    """Fix XML namespace formatting for AVC285 Canvas compatibility"""
    extracted_path = Path('AVC285/extracted_course')
    
    print("\n=== Fixing AVC285 XML Formatting ===")
    
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
    
    print(f"Fixed XML formatting in {fixed_count} assignments")

def copy_avc285_assignments_back():
    """Copy AVC285 assignments back to extracted_course"""
    assignments_path = Path('AVC285/assignments')
    extracted_path = Path('AVC285/extracted_course')
    
    with open('AVC285/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    print(f"\n=== Copying AVC285 Assignments Back ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        if html_file.exists():
            dest_folder = extracted_path / info['original_folder']
            dest_file = dest_folder / info['original_html']
            shutil.copy2(html_file, dest_file)
            print(f"  Copied {html_file.name}")

def create_avc285_github_pages():
    """Create GitHub Pages files for AVC285"""
    
    # Create _config.yml
    config_content = """theme: jekyll-theme-minimal
title: AVC285 Advanced 3D Modeling and Simulation
description: Assignment resources for AVC285 Advanced 3D Modeling and Simulation course at GCC"""
    
    config_file = Path('AVC285/_config.yml')
    config_file.write_text(config_content, encoding='utf-8')
    
    # Create index.md
    index_content = """# AVC285 Advanced 3D Modeling and Simulation

## Course Assignments

This repository contains assignment resources for AVC285 Advanced 3D Modeling and Simulation. The course runs for 16 weeks with 15 assignments (weeks 1-15). Week 16 is reserved for final presentations and course wrap-up. Assignments include lecture videos accessible through the redirect system.

### Week-by-Week Assignments

**Simulation Modeling Phase (Weeks 1-6)**
1. [Week 1: Simulation Modeling: Rigid Bodies](assignments/week_1_simulation_modeling_rigid_bodies.html)
2. [Week 2: Simulation Modeling: Fracture and Art Directing a Simulation](assignments/week_2_simulation_modeling_fracture_and_art_directing_a_simulation.html)
3. [Week 3: Simulation Modeling: Cloth and Spline](assignments/week_3_simulation_modeling_cloth_and_spline_.html)
4. [Week 4: Introduction to TwinMotion and Substance Painter: Transferring Assets](assignments/week_4_introduction_to_twinmotion_and_substance_painter_transferring_assets.html)
5. [Week 5: Simulation Modeling: Cloth: Pants and Shirts](assignments/week_5_simulation_modeling_cloth_pants_and_shirts.html)
6. [Week 6: Simulation Modeling: Soft Body Physics, Simulated Cloth workflow, Introduction to Unreal Engine](assignments/week_6_simulation_modeling_soft_body_physics_simulated_cloth_workflow_introduction_to_unreal_engine.html)

**Advanced Texturing Phase (Weeks 7-11)**
7. [Week 7: Substance Sampler: Creating your own Substances, Using them in Unreal Engine](assignments/week_7_substance_sampler_creating_your_own_substances_using_them_in_unreal_engine.html)
8. [Week 8: Photogrammetry: Scanning Reality, Sequences in Unreal Engine](assignments/week_8_photogrammetry_scanning_reality_sequences_in_unreal_engine.html)
9. [Week 9: Photogrammetry: Revisions](assignments/week_9_photogrammetry_revisions.html)
10. [Week 10: Substance Painter: Advanced Techniques](assignments/week_10_substance_painter_advanced_techniques.html)
11. [Week 11: Substance Painter: Advanced brush generation techniques](assignments/week_11_substance_painter_advanced_brush_generation_techniques.html)

**Advanced Sculpting Phase (Weeks 12-15)**
12. [Week 12: Introduction to Sculpting in Blender](assignments/week_12_introduction_to_sculpting_in_blender.html)
13. [Week 13: Hard Surface Sculpting in Blender, Advanced Mask Techniques in Substance Painter](assignments/week_13_hard_surface_sculpting_in_blender_advanced_mask_techniques_in_substance_painter.html)
14. [Week 14: Sculpting in Blender: Using VDM brushes](assignments/week_14_sculpting_in_blender_using_vdm_brushes.html)
15. [Week 15: Advanced VDM Techniques and Final Portfolio](assignments/week_15_advanced_vdm_techniques_and_final_portfolio.html)

**Week 16: Course Wrap-up** (No Assignment - Final Presentations)

## Features

- **Lecture Redirect System**: YouTube lecture links use the redirect system at `https://caseyfarina.github.io/lecture-redirects/` for easy maintenance
- **Standardized Headers**: All assignments use consistent H2 heading structure with bold formatting
- **Accessibility**: Images include descriptive alt text for screen readers
- **Week Organization**: Assignments for weeks 1-15 with week 16 reserved for final presentations

## Technical Notes

- Course focuses on advanced 3D modeling, simulation, and texturing techniques
- Assignments include Blender simulation, Substance suite workflows, and Unreal Engine integration
- Covers photogrammetry, VDM sculpting, and advanced material creation
- Course integrates multiple professional 3D software packages

## Course Structure

**Phase 1: Simulation Modeling** (Weeks 1-6)
- Rigid body and soft body physics
- Fracture and destruction simulations
- Cloth simulation and spline modeling
- TwinMotion architectural visualization
- Unreal Engine integration

**Phase 2: Advanced Texturing** (Weeks 7-11)
- Substance Sampler material creation
- Photogrammetry workflow and scanning
- Advanced Substance Painter techniques
- Custom brush generation and procedural texturing

**Phase 3: Advanced Sculpting** (Weeks 12-15)
- Digital sculpting in Blender
- Hard surface sculpting techniques
- VDM (Vector Displacement Map) workflows
- Advanced mask and detail techniques
- Final portfolio development

**Phase 4: Course Conclusion** (Week 16)
- Final presentations and course wrap-up
- Portfolio review and professional development
- No assignment due
"""
    
    index_file = Path('AVC285/index.md')
    index_file.write_text(index_content, encoding='utf-8')
    
    print(f"\n=== Created AVC285 GitHub Pages ===")

def complete_avc285_processing():
    """Run complete AVC285 processing workflow"""
    print("=== Starting Complete AVC285 Processing ===")
    
    # Step 1: Update YouTube links
    update_avc285_youtube_links()
    
    # Step 2: Standardize headers (reuse existing script)
    print("\n=== Standardizing AVC285 Headers ===")
    # This will be handled by the existing standardize_headers.py script
    
    # Step 3: Generate alt text
    generate_avc285_alt_text()
    
    # Step 4: Update due dates
    update_avc285_due_dates()
    
    # Step 5: Fix XML formatting
    fix_avc285_xml_formatting()
    
    # Step 6: Create GitHub Pages
    create_avc285_github_pages()
    
    # Step 7: Copy assignments back
    copy_avc285_assignments_back()
    
    print(f"\n=== AVC285 Complete Processing Finished ===")
    print("AVC285 is now ready for Canvas import with:")
    print("- 15 assignments for weeks 1-15")
    print("- Tuesday due dates starting September 2, 2025")
    print("- AVC285 redirect links")
    print("- Standardized formatting and accessibility")
    print("- XML formatting fixed for Canvas compatibility")

if __name__ == "__main__":
    complete_avc285_processing()