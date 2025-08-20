#!/usr/bin/env python3
"""
Rename assignment HTML files to match assignment titles
"""

import os
import json
from pathlib import Path

def rename_assignment_files():
    """Rename assignment HTML files to descriptive names"""
    
    base_path = Path(__file__).parent
    assignments_path = base_path / "assignments"
    mapping_file = base_path / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    # Assignment order for proper numbering
    assignment_order = [
        ("week_1_introduction_to_blender", "Week 1 - Introduction to Blender"),
        ("week_2_bezier_curves_creating_3d_shapes_from_2d_curves", "Week 2 - Bezier Curves Creating 3D Shapes"),
        ("modifiers_and_rendering_constructing_a_scene_from_multipart_objects", "Week 3 - Modifiers and Rendering"),
        ("rendering_compositing_and_basic_remesh_workflow", "Week 4 - Rendering Compositing and Remesh"),
        ("introduction_to_substance_painter", "Week 5 - Introduction to Substance Painter"),
        ("introduction_to_uv_unwrapping", "Week 6 - Introduction to UV Unwrapping"),
        ("modeling_foliage_uv_details_playground_showcase_video", "Week 7 - Modeling Foliage and UV Details"),
        ("modeling_to_scale_and_uv_packing", "Week 8 - Modeling to Scale and UV Packing"),
        ("substance_painter_techniques", "Week 9 - Substance Painter Techniques"),
        ("lamp_revisions", "Week 10 - Lamp Revisions"),
        ("kitchen_modeling_kitchen_table_and_chairs", "Week 11 - Kitchen Table and Chairs"),
        ("kitchen_modeling_silverware_and_antique_silverware", "Week 12 - Kitchen Silverware"),
        ("kitchen_plates_and_napkins", "Week 13 - Kitchen Plates and Napkins"),
        ("materials_hard_surface_vs_sculpting_workflow", "Week 14 - Materials Hard Surface vs Sculpting"),
        ("final_portfolio_requirements_25_percent_of_the_course_grade", "Week 15 - Final Portfolio"),
        ("week_1_technology_login_challenge_3", "Technology Login Challenge (TLC)")
    ]
    
    renamed_count = 0
    
    for old_name, new_title in assignment_order:
        if old_name in assignment_mapping:
            old_file = assignments_path / f"{old_name}.html"
            
            # Create clean filename from title
            clean_title = new_title.replace("(", "").replace(")", "").replace(":", "").replace("/", " or ")
            clean_title = " ".join(clean_title.split())  # Remove extra spaces
            new_file = assignments_path / f"{clean_title}.html"
            
            if old_file.exists():
                try:
                    old_file.rename(new_file)
                    print(f"Renamed: {old_name}.html -> {clean_title}.html")
                    renamed_count += 1
                except Exception as e:
                    print(f"Error renaming {old_name}: {e}")
            else:
                print(f"File not found: {old_name}.html")
    
    print(f"\nRenamed {renamed_count} assignment files")
    print("\nNew filenames:")
    print("-" * 60)
    
    for file in sorted(assignments_path.glob("*.html")):
        print(f"  {file.name}")

if __name__ == "__main__":
    rename_assignment_files()