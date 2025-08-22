import json
from pathlib import Path
import shutil
import re

def restructure_avc200():
    """Remove specified assignments and renumber remaining ones to 16 weeks"""
    
    assignments_path = Path('AVC200/assignments')
    
    # Load current mapping
    with open('AVC200/assignment_mapping.json', 'r') as f:
        current_mapping = json.load(f)
    
    # Assignments to remove
    remove_assignments = [
        'week_2_class_video_introduction_',
        'week_3_will_my_home_computer_work_for_this_class', 
        'week_4_technology_login_challenge_3',
        'week_10_play_tester_feedback',
        'week_19_play_tester_feedback_unreal'
    ]
    
    print("=== Removing Non-Assignment Files ===")
    
    # Remove unwanted assignments
    for assignment_name in remove_assignments:
        html_file = assignments_path / f"{assignment_name}.html"
        if html_file.exists():
            html_file.unlink()
            print(f"Removed: {html_file.name}")
        
        # Remove from mapping
        if assignment_name in current_mapping:
            del current_mapping[assignment_name]
            print(f"Removed from mapping: {assignment_name}")
    
    # Create new mapping for 16 weeks
    print("\n=== Creating 16-Week Structure ===")
    
    # Define the new 16-week order
    remaining_assignments = [
        ('week_1_introduction_to_unity_animation_interactivity', 1),
        ('week_5_expanding_interactivity_prototyping_a_rolling_ball_game', 2),
        ('week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances', 3),
        ('week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows', 4),
        ('week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles', 5),
        ('week_9_adding_a_start_screen_using_llms_for_unity_scripting', 6),
        ('week_11_adding_a_collectable_or_key_mechanic_to_the_game', 7),
        ('week_12_rolling_ball_game_final', 8),
        ('week_13_introduction_to_the_epic_eco_system_and_unreal_engine', 9),
        ('week_14_first_person_collection_in_unreal_engine', 10),
        ('week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx', 11),
        ('week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints', 12),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 13),
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 14),
        ('week_20_final_portfolio_requirements_25_of_the_course_grade', 15)
    ]
    
    # Note: We'll make week 15 and 16 both portfolio-related
    remaining_assignments.append(('week_20_final_portfolio_requirements_25_of_the_course_grade', 16))
    
    # Remove the duplicate
    remaining_assignments = remaining_assignments[:-1]
    remaining_assignments.append(('week_20_final_portfolio_requirements_25_of_the_course_grade', 16))
    
    # Actually, let's just make it 15 weeks with the final portfolio
    remaining_assignments = [
        ('week_1_introduction_to_unity_animation_interactivity', 1),
        ('week_5_expanding_interactivity_prototyping_a_rolling_ball_game', 2),
        ('week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances', 3),
        ('week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows', 4),
        ('week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles', 5),
        ('week_9_adding_a_start_screen_using_llms_for_unity_scripting', 6),
        ('week_11_adding_a_collectable_or_key_mechanic_to_the_game', 7),
        ('week_12_rolling_ball_game_final', 8),
        ('week_13_introduction_to_the_epic_eco_system_and_unreal_engine', 9),
        ('week_14_first_person_collection_in_unreal_engine', 10),
        ('week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx', 11),
        ('week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints', 12),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 13),
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 14),
        ('week_20_final_portfolio_requirements_25_of_the_course_grade', 15)
    ]
    
    # Actually we need 16, let's split the portfolio into prep and final
    remaining_assignments = [
        ('week_1_introduction_to_unity_animation_interactivity', 1),
        ('week_5_expanding_interactivity_prototyping_a_rolling_ball_game', 2),
        ('week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances', 3),
        ('week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows', 4),
        ('week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles', 5),
        ('week_9_adding_a_start_screen_using_llms_for_unity_scripting', 6),
        ('week_11_adding_a_collectable_or_key_mechanic_to_the_game', 7),
        ('week_12_rolling_ball_game_final', 8),
        ('week_13_introduction_to_the_epic_eco_system_and_unreal_engine', 9),
        ('week_14_first_person_collection_in_unreal_engine', 10),
        ('week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx', 11),
        ('week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints', 12),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 13),
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 14),
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 15),  # Portfolio prep
        ('week_20_final_portfolio_requirements_25_of_the_course_grade', 16)  # Final portfolio
    ]
    
    # Remove duplicate - let's be more thoughtful
    remaining_assignments = [
        ('week_1_introduction_to_unity_animation_interactivity', 1),
        ('week_5_expanding_interactivity_prototyping_a_rolling_ball_game', 2),
        ('week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances', 3),
        ('week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows', 4),
        ('week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles', 5),
        ('week_9_adding_a_start_screen_using_llms_for_unity_scripting', 6),
        ('week_11_adding_a_collectable_or_key_mechanic_to_the_game', 7),
        ('week_12_rolling_ball_game_final', 8),
        ('week_13_introduction_to_the_epic_eco_system_and_unreal_engine', 9),
        ('week_14_first_person_collection_in_unreal_engine', 10),
        ('week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx', 11),
        ('week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints', 12),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 13),
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 14),
        ('week_20_final_portfolio_requirements_25_of_the_course_grade', 15)
    ]
    
    # We need exactly 16 - let's add one more practical assignment by splitting one
    remaining_assignments = [
        ('week_1_introduction_to_unity_animation_interactivity', 1),
        ('week_5_expanding_interactivity_prototyping_a_rolling_ball_game', 2),
        ('week_6_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances', 3),
        ('week_7_game_assets_substance_painter_substance_modeler_game_asset_workflows', 4),
        ('week_8_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles', 5),
        ('week_9_adding_a_start_screen_using_llms_for_unity_scripting', 6),
        ('week_11_adding_a_collectable_or_key_mechanic_to_the_game', 7),
        ('week_12_rolling_ball_game_final', 8),
        ('week_13_introduction_to_the_epic_eco_system_and_unreal_engine', 9),
        ('week_14_first_person_collection_in_unreal_engine', 10),
        ('week_15_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx', 11),
        ('week_16_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints', 12),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 13),
        ('week_17_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_', 14),  # Part 2
        ('week_18_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 15),
        ('week_20_final_portfolio_requirements_25_of_the_course_grade', 16)
    ]
    
    new_mapping = {}
    
    # Rename files and update mapping
    for old_name, new_week in remaining_assignments:
        old_file = assignments_path / f"{old_name}.html"
        
        if old_file.exists():
            # Create new filename
            base_name = old_name.replace(f"week_{old_name.split('_')[1]}_", "")
            new_name = f"week_{new_week}_{base_name}"
            new_file = assignments_path / f"{new_name}.html"
            
            # Handle potential duplicates for week 14 (building game part 2)
            if new_week == 14 and 'building_the_game' in new_name and new_file.exists():
                new_name = f"week_14_building_the_game_in_unreal_part_2"
                new_file = assignments_path / f"{new_name}.html"
            
            # Read content and update week references in titles
            if old_file.exists():
                content = old_file.read_text(encoding='utf-8')
                
                # Update title tags and headers to reflect new week number
                if old_name in current_mapping:
                    old_title = current_mapping[old_name]['title']
                    new_title = re.sub(r'^Week \d+:', f'Week {new_week}:', old_title)
                    
                    # Update title in HTML content
                    content = re.sub(r'<title>Assignment: Week \d+:', f'<title>Assignment: Week {new_week}:', content)
                
                # Write to new file
                new_file.write_text(content, encoding='utf-8')
                
                # Update mapping
                if old_name in current_mapping:
                    current_mapping[old_name]['title'] = f"Week {new_week}: " + current_mapping[old_name]['original_title']
                    current_mapping[old_name]['week_number'] = new_week
                    new_mapping[new_name] = current_mapping[old_name]
                
                # Remove old file if different name
                if old_file != new_file:
                    old_file.unlink()
                
                print(f"Week {new_week}: {new_name}")
    
    # Save updated mapping
    with open('AVC200/assignment_mapping.json', 'w') as f:
        json.dump(new_mapping, f, indent=2)
    
    print(f"\n=== Restructured to {len(new_mapping)} assignments for 16-week semester ===")

if __name__ == "__main__":
    restructure_avc200()