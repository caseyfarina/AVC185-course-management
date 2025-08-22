import json
from pathlib import Path
import shutil
import re

def renumber_avc200():
    """Renumber remaining AVC200 assignments to fit 16-week semester"""
    
    assignments_path = Path('AVC200/assignments')
    
    # Get current files and sort them
    current_files = sorted([f for f in assignments_path.glob('*.html')])
    
    print("=== Current Remaining Files ===")
    for f in current_files:
        print(f"  {f.name}")
    
    # Define the new 16-week mapping
    # Keep the same order but renumber sequentially
    week_mapping = {
        'week_1_introduction_to_unity_animation_interactivity.html': 1,
        'week_5_expanding_interactivity_prototyping_a_rolling_ball_game.html': 2,
        'week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances.html': 3,
        'week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows.html': 4,
        'week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles.html': 5,
        'week_9_adding_a_start_screen_using_llms_for_unity_scripting.html': 6,
        'week_11_adding_a_collectable_or_key_mechanic_to_the_game.html': 7,
        'week_12_rolling_ball_game_final.html': 8,
        'week_13_introduction_to_the_epic_eco_system_and_unreal_engine.html': 9,
        'week_14_first_person_collection_in_unreal_engine.html': 10,
        'week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx.html': 11,
        'week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints.html': 12,
        'week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_.html': 13,
        'week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system.html': 14,
        'week_20_final_portfolio_requirements_25_of_the_course_grade.html': 15
    }
    
    # We need 16 weeks, so let's add a final submission week
    # We'll duplicate the final portfolio as weeks 15 and 16 (prep and final)
    week_mapping['week_20_final_portfolio_requirements_25_of_the_course_grade.html'] = 16
    
    print("\n=== Renumbering to 16-Week Structure ===")
    
    # Load current mapping
    with open('AVC200/assignment_mapping.json', 'r') as f:
        current_mapping = json.load(f)
    
    new_mapping = {}
    temp_files = []
    
    # First pass: create temporary files with new numbering
    for old_filename, new_week_num in week_mapping.items():
        old_file = assignments_path / old_filename
        
        if old_file.exists():
            # Create new filename
            old_parts = old_filename.replace('.html', '').split('_')
            base_name = '_'.join(old_parts[2:])  # Remove 'week_X_' prefix
            
            # Special handling for final portfolio weeks 15 and 16
            if new_week_num == 15:
                new_filename = f"week_15_{base_name}_preparation.html"
            elif new_week_num == 16:
                new_filename = f"week_16_{base_name}_final_submission.html"
            else:
                new_filename = f"week_{new_week_num}_{base_name}.html"
            
            temp_file = assignments_path / f"temp_{new_filename}"
            
            # Read and update content
            content = old_file.read_text(encoding='utf-8')
            
            # Update title in HTML
            content = re.sub(
                r'<title>Assignment: Week \d+:',
                f'<title>Assignment: Week {new_week_num}:',
                content
            )
            
            # Write to temp file
            temp_file.write_text(content, encoding='utf-8')
            temp_files.append((temp_file, new_filename, old_filename, new_week_num))
            
            print(f"Week {new_week_num}: {new_filename}")
    
    # Remove old files
    for old_filename in week_mapping.keys():
        old_file = assignments_path / old_filename
        if old_file.exists():
            old_file.unlink()
    
    # Rename temp files to final names and update mapping
    for temp_file, new_filename, old_filename, new_week_num in temp_files:
        final_file = assignments_path / new_filename
        temp_file.rename(final_file)
        
        # Find corresponding entry in current mapping and update
        old_key = old_filename.replace('.html', '')
        if old_key in current_mapping:
            info = current_mapping[old_key].copy()
            info['week_number'] = new_week_num
            
            # Update title
            original_title = info['original_title']
            info['title'] = f"Week {new_week_num}: {original_title}"
            
            # Special titles for final portfolio weeks
            if new_week_num == 15:
                info['title'] = f"Week 15: {original_title} - Preparation"
            elif new_week_num == 16:
                info['title'] = f"Week 16: {original_title} - Final Submission"
            
            new_key = new_filename.replace('.html', '')
            new_mapping[new_key] = info
    
    # Save new mapping
    with open('AVC200/assignment_mapping.json', 'w') as f:
        json.dump(new_mapping, f, indent=2)
    
    print(f"\n=== Successfully renumbered to {len(new_mapping)} assignments for 16-week semester ===")
    
    # Update redirect links for the new week numbers
    update_redirect_links(new_mapping)

def update_redirect_links(mapping):
    """Update YouTube redirect links to match new week numbers"""
    assignments_path = Path('AVC200/assignments')
    
    print("\n=== Updating Redirect Links for 16-Week Schedule ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        new_week_num = info['week_number']
        
        # Update redirect links to use new week number
        # Pattern: https://caseyfarina.github.io/lecture-redirects/?class=avc200&lecture=weekN-lectureX
        redirect_pattern = r'https://caseyfarina\.github\.io/lecture-redirects/\?class=avc200&lecture=week(\d+)-(lecture\d+)'
        
        def update_week_number(match):
            lecture_part = match.group(2)  # lecture1 or lecture2
            return f'https://caseyfarina.github.io/lecture-redirects/?class=avc200&lecture=week{new_week_num}-{lecture_part}'
        
        new_content = re.sub(redirect_pattern, update_week_number, content)
        
        if new_content != original_content:
            html_file.write_text(new_content, encoding='utf-8')
            print(f"  Updated redirect links in {html_file.name} to week {new_week_num}")

if __name__ == "__main__":
    renumber_avc200()