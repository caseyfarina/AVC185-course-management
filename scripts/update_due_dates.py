#!/usr/bin/env python3
"""
Update assignment due dates according to new schedule:
- Technology Login Challenge: Thursday Aug 28, 2025 at 8 PM Arizona time
- All other assignments: Tuesdays at 8 PM Arizona time starting Sept 2, 2025
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timedelta
import json

def update_due_dates():
    """Update all assignment due dates according to new schedule"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    mapping_file = base_path / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found. Run extract_assignments.py first.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    # Define new schedule
    # Start date: Tuesday September 2, 2025 at 8 PM Arizona time
    start_date = datetime(2025, 9, 2, 20, 0, 0)  # Sept 2, 2025, 8:00 PM
    
    # Special case: Technology Login Challenge - Thursday Aug 28, 2025 at 8 PM
    tech_challenge_date = datetime(2025, 8, 28, 20, 0, 0)  # Aug 28, 2025, 8:00 PM
    
    # Assignment order (based on content analysis)
    assignment_order = [
        "week_1_introduction_to_blender",
        "week_2_bezier_curves_creating_3d_shapes_from_2d_curves", 
        "modifiers_and_rendering_constructing_a_scene_from_multipart_objects",
        "rendering_compositing_and_basic_remesh_workflow",
        "introduction_to_substance_painter",
        "introduction_to_uv_unwrapping",
        "modeling_foliage_uv_details_playground_showcase_video", 
        "modeling_to_scale_and_uv_packing",
        "substance_painter_techniques",
        "lamp_revisions",
        "kitchen_modeling_kitchen_table_and_chairs",
        "kitchen_modeling_silverware_and_antique_silverware",
        "kitchen_plates_and_napkins",
        "materials_hard_surface_vs_sculpting_workflow",
        "final_portfolio_requirements_25_percent_of_the_course_grade"
    ]
    
    updates_made = 0
    
    for assignment_name, mapping_info in assignment_mapping.items():
        folder_path = extracted_path / mapping_info['original_folder']
        settings_file = folder_path / "assignment_settings.xml"
        
        if not settings_file.exists():
            print(f"Warning: {settings_file} not found")
            continue
        
        try:
            tree = ET.parse(settings_file)
            root = tree.getroot()
            
            # Find due_at and all_day_date elements
            ns = {'cc': 'http://canvas.instructure.com/xsd/cccv1p0'}
            due_at_elem = root.find('.//cc:due_at', ns)
            all_day_elem = root.find('.//cc:all_day_date', ns)
            
            if due_at_elem is None:
                print(f"Warning: No due_at element found in {assignment_name}")
                continue
            
            # Determine new due date
            if assignment_name == "week_1_technology_login_challenge_3":
                new_due_date = tech_challenge_date
                print(f"Special: {assignment_name} -> Thursday Aug 28, 8 PM")
            else:
                # Find position in ordered list
                if assignment_name in assignment_order:
                    week_offset = assignment_order.index(assignment_name)
                    new_due_date = start_date + timedelta(weeks=week_offset)
                    print(f"Regular: {assignment_name} -> Tuesday {new_due_date.strftime('%b %d')}, 8 PM")
                else:
                    print(f"Warning: {assignment_name} not found in assignment order")
                    continue
            
            # Format dates for Canvas (Arizona time is UTC-7, but we'll use local time as specified)
            due_at_str = new_due_date.strftime("%Y-%m-%dT%H:%M:%S")
            all_day_str = new_due_date.strftime("%Y-%m-%d")
            
            # Update XML elements
            due_at_elem.text = due_at_str
            if all_day_elem is not None:
                all_day_elem.text = all_day_str
            
            # Write back to file
            tree.write(settings_file, encoding='UTF-8', xml_declaration=True)
            updates_made += 1
            
        except Exception as e:
            print(f"Error updating {assignment_name}: {e}")
    
    print(f"\nUpdated {updates_made} assignment due dates")
    print("\nNew Schedule:")
    print("=" * 50)
    print("Technology Login Challenge: Thursday Aug 28, 2025 at 8 PM")
    print("All other assignments: Tuesdays at 8 PM starting Sept 2, 2025")
    print("\nRun 'python show_due_dates.py' to verify changes")

if __name__ == "__main__":
    update_due_dates()