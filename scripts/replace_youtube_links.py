#!/usr/bin/env python3
"""
Replace YouTube links in assignments with permanent redirect links
Format: https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=weekN-lecture1
"""

import re
from pathlib import Path
import json

def replace_youtube_links():
    """Replace YouTube links with permanent redirect links in all assignments"""
    
    base_path = Path(__file__).parent
    assignments_path = base_path / "assignments"
    mapping_file = base_path / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found. Run extract_assignments.py first.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    # Assignment order for week numbering (same as previous)
    assignment_order = [
        "week_1_introduction_to_blender",  # Week 1
        "week_2_bezier_curves_creating_3d_shapes_from_2d_curves",  # Week 2
        "modifiers_and_rendering_constructing_a_scene_from_multipart_objects",  # Week 3
        "rendering_compositing_and_basic_remesh_workflow",  # Week 4
        "introduction_to_substance_painter",  # Week 5
        "introduction_to_uv_unwrapping",  # Week 6
        "modeling_foliage_uv_details_playground_showcase_video",  # Week 7
        "modeling_to_scale_and_uv_packing",  # Week 8
        "substance_painter_techniques",  # Week 9
        "lamp_revisions",  # Week 10
        "kitchen_modeling_kitchen_table_and_chairs",  # Week 11
        "kitchen_modeling_silverware_and_antique_silverware",  # Week 12
        "kitchen_plates_and_napkins",  # Week 13
        "materials_hard_surface_vs_sculpting_workflow"  # Week 14
    ]
    
    # Special assignments (TLC and Final Portfolio) - also check for YouTube links
    special_assignments = [
        "week_1_technology_login_challenge_3",  # TLC
        "final_portfolio_requirements_25_percent_of_the_course_grade"  # Final Portfolio
    ]
    
    updates_made = 0
    
    # Process regular weekly assignments
    for assignment_name in assignment_order:
        if assignment_name not in assignment_mapping:
            print(f"Warning: {assignment_name} not found in mapping")
            continue
        
        week_num = assignment_order.index(assignment_name) + 1
        assignment_file = assignments_path / f"{assignment_name}.html"
        
        if not assignment_file.exists():
            print(f"Warning: {assignment_file} not found")
            continue
        
        # Read the file
        try:
            with open(assignment_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pattern to match YouTube links
            youtube_pattern = r'<a href="https://(?:www\.)?youtube\.com/(?:watch\?v=|live/)([^"]*)"[^>]*>([^<]*)</a>'
            
            # Find all YouTube links
            youtube_matches = re.findall(youtube_pattern, content)
            
            if len(youtube_matches) >= 2:
                # Replace first two YouTube links with redirect links
                lecture1_url = f"https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=week{week_num}-lecture1"
                lecture2_url = f"https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=week{week_num}-lecture2"
                
                # Replace first YouTube link
                first_match = youtube_matches[0]
                old_link1 = f'<a href="https://www.youtube.com/{first_match[0]}" target="_blank">{first_match[1]}</a>'
                if old_link1 not in content:
                    # Try alternative format
                    old_link1 = f'<a href="https://youtube.com/{first_match[0]}" target="_blank">{first_match[1]}</a>'
                
                new_link1 = f'<a href="{lecture1_url}" target="_blank">{lecture1_url}</a>'
                
                # Replace second YouTube link
                second_match = youtube_matches[1]
                old_link2 = f'<a href="https://www.youtube.com/{second_match[0]}" target="_blank">{second_match[1]}</a>'
                if old_link2 not in content:
                    # Try alternative format
                    old_link2 = f'<a href="https://youtube.com/{second_match[0]}" target="_blank">{second_match[1]}</a>'
                
                new_link2 = f'<a href="{lecture2_url}" target="_blank">{lecture2_url}</a>'
                
                # Perform replacements using regex for more flexible matching
                # Replace first two YouTube links only
                youtube_count = 0
                
                def replacement_func(match):
                    nonlocal youtube_count
                    youtube_count += 1
                    if youtube_count <= 2:  # Only replace first two
                        return f'<a href="https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=week{week_num}-lecture{youtube_count}" target="_blank">https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=week{week_num}-lecture{youtube_count}</a>'
                    else:
                        return match.group(0)  # Keep original for subsequent matches
                
                updated_content = re.sub(youtube_pattern, replacement_func, content)
                
                # Write back to file
                with open(assignment_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Week {week_num:2}: Updated {len(youtube_matches)} YouTube links -> redirect links")
                updates_made += 1
            else:
                print(f"Week {week_num:2}: Found {len(youtube_matches)} YouTube links (expected 2)")
        
        except Exception as e:
            print(f"Error processing {assignment_name}: {e}")
    
    # Process special assignments (TLC and Final Portfolio)
    for assignment_name in special_assignments:
        if assignment_name not in assignment_mapping:
            continue
        
        assignment_file = assignments_path / f"{assignment_name}.html"
        
        if not assignment_file.exists():
            continue
        
        try:
            with open(assignment_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for YouTube links
            youtube_matches = re.findall(youtube_pattern, content)
            
            if youtube_matches:
                print(f"Special assignment {assignment_name}: Found {len(youtube_matches)} YouTube links (review manually)")
            else:
                print(f"Special assignment {assignment_name}: No YouTube links found")
        
        except Exception as e:
            print(f"Error checking {assignment_name}: {e}")
    
    print(f"\nUpdated {updates_made} assignments with redirect links")
    print("\nRedirect link format:")
    print("Lecture 1: https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=weekN-lecture1")
    print("Lecture 2: https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=weekN-lecture2")

if __name__ == "__main__":
    replace_youtube_links()