import json
from pathlib import Path
import re

def final_renumber_avc200():
    """Renumber AVC200 assignments for weeks 2-16 (15 total assignments)"""
    
    assignments_path = Path('AVC200/assignments')
    
    # Get current files and sort them
    current_files = sorted([f for f in assignments_path.glob('*.html')])
    
    print("=== Current Files (should be 15) ===")
    for f in current_files:
        print(f"  {f.name}")
    
    # Define the correct 15-assignment mapping for weeks 2-16
    # Week 1 has no assignment, assignments start at week 2
    week_mapping = {
        'week_1_introduction_to_unity_animation_interactivity.html': 2,  # Week 2
        'week_2_expanding_interactivity_prototyping_a_rolling_ball_game.html': 3,  # Week 3
        'week_3_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances.html': 4,  # Week 4
        'week_4_game_assets_substance_painter_substance_modeler_game_asset_workflows.html': 5,  # Week 5
        'week_5_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles.html': 6,  # Week 6
        'week_6_adding_a_start_screen_using_llms_for_unity_scripting.html': 7,  # Week 7
        'week_7_adding_a_collectable_or_key_mechanic_to_the_game.html': 8,  # Week 8
        'week_8_rolling_ball_game_final.html': 9,  # Week 9
        'week_9_introduction_to_the_epic_eco_system_and_unreal_engine.html': 10,  # Week 10
        'week_10_first_person_collection_in_unreal_engine.html': 11,  # Week 11
        'week_11_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx.html': 12,  # Week 12
        'week_12_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints.html': 13,  # Week 13
        'week_13_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_.html': 14,  # Week 14
        'week_14_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system.html': 15,  # Week 15
        'week_16_final_portfolio_requirements_25_of_the_course_grade_final_submission.html': 16  # Week 16
    }
    
    print(f"\n=== Renumbering {len(week_mapping)} assignments for weeks 2-16 ===")
    
    # Load current mapping
    with open('AVC200/assignment_mapping.json', 'r') as f:
        current_mapping = json.load(f)
    
    new_mapping = {}
    temp_files = []
    
    # First pass: create temporary files with new numbering
    for old_filename, new_week_num in week_mapping.items():
        old_file = assignments_path / old_filename
        
        if old_file.exists():
            # Create new filename based on week number
            old_parts = old_filename.replace('.html', '').split('_')
            base_name = '_'.join(old_parts[2:])  # Remove 'week_X_' prefix
            
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
            
            # Update redirect links to use new week number
            content = re.sub(
                r'week\d+-(lecture\d+)',
                f'week{new_week_num}-\\1',
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
        new_key = new_filename.replace('.html', '')
        
        # Create new mapping entry
        new_mapping[new_key] = {
            'original_folder': 'placeholder',  # Will be updated when copying back
            'original_html': 'placeholder.html',
            'title': f"Week {new_week_num}: Assignment Title",  # Will be updated
            'original_title': f"Assignment Title",
            'week_number': new_week_num
        }
    
    # Save new mapping
    with open('AVC200/assignment_mapping.json', 'w') as f:
        json.dump(new_mapping, f, indent=2)
    
    print(f"\n=== Successfully renumbered to {len(new_mapping)} assignments for weeks 2-16 ===")
    print("Week 1: No assignment (introduction week)")
    print("Weeks 2-16: 15 assignments total")

if __name__ == "__main__":
    final_renumber_avc200()