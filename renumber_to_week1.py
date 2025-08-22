import re
from pathlib import Path
import json

def renumber_to_week1():
    """Renumber AVC200 assignments to start at Week 1 (weeks 1-15)"""
    
    assignments_path = Path('AVC200/assignments')
    
    # Get current files and sort them
    current_files = sorted([f for f in assignments_path.glob('*.html')])
    
    print("=== Current Files (Weeks 2-16) ===")
    for f in current_files:
        print(f"  {f.name}")
    
    print(f"\n=== Renumbering to Weeks 1-15 ===")
    
    # Create mapping from current week numbers (2-16) to new week numbers (1-15)
    week_mapping = {}
    temp_files = []
    
    for file in current_files:
        # Extract current week number from filename
        match = re.search(r'week_(\d+)_(.+)\.html', file.name)
        if match:
            current_week = int(match.group(1))
            base_name = match.group(2)
            new_week = current_week - 1  # Shift down by 1
            
            new_filename = f"week_{new_week}_{base_name}.html"
            temp_filename = f"temp_{new_filename}"
            
            # Read content and update
            content = file.read_text(encoding='utf-8')
            
            # Update title in HTML
            content = re.sub(
                rf'<title>Assignment: Week {current_week}:',
                f'<title>Assignment: Week {new_week}:',
                content
            )
            
            # Update redirect links to use new week number
            content = re.sub(
                rf'week{current_week}-(lecture\d+)',
                f'week{new_week}-\\1',
                content
            )
            
            # Write to temp file
            temp_file = assignments_path / temp_filename
            temp_file.write_text(content, encoding='utf-8')
            temp_files.append((temp_file, new_filename, file))
            
            print(f"Week {current_week} -> Week {new_week}: {new_filename}")
    
    # Remove original files
    for file in current_files:
        file.unlink()
    
    # Rename temp files to final names
    for temp_file, new_filename, original_file in temp_files:
        final_file = assignments_path / new_filename
        temp_file.rename(final_file)
    
    # Update mapping file
    new_mapping = {}
    for i in range(1, 16):  # Weeks 1-15
        key = f"week_{i}_placeholder"  # Placeholder keys
        new_mapping[key] = {
            'original_folder': 'placeholder',
            'original_html': 'placeholder.html',
            'title': f"Week {i}: Assignment Title",
            'original_title': f"Assignment Title",
            'week_number': i
        }
    
    with open('AVC200/assignment_mapping.json', 'w') as f:
        json.dump(new_mapping, f, indent=2)
    
    print(f"\n=== Successfully renumbered to 15 assignments for weeks 1-15 ===")
    print("Weeks 1-15: 15 assignments total")
    
    # Update GitHub Pages
    update_github_pages()

def update_github_pages():
    """Update GitHub Pages index for weeks 1-15"""
    
    index_file = Path('AVC200/index.md')
    
    new_content = """# AVC200 Game Design and Development

## Course Assignments

This repository contains assignment resources for AVC200 Game Design and Development. The course runs for 16 weeks with 15 assignments (weeks 1-15). Week 16 is reserved for final presentations and course wrap-up. Assignments include lecture videos accessible through the redirect system.

### Week-by-Week Assignments

**Unity Development Phase (Weeks 1-8)**
1. [Week 1: Introduction to Unity: Animation & Interactivity](assignments/week_1_introduction_to_unity_animation_interactivity.html)
2. [Week 2: Expanding Interactivity: Prototyping a rolling ball game](assignments/week_2_expanding_interactivity_prototyping_a_rolling_ball_game.html)
3. [Week 3: Game Assets: Modeling in Blender, Lighting, Prefabs, and editing Substances](assignments/week_3_game_assets_modeling_in_blender_lighting_prefabs_and_editing_substances.html)
4. [Week 4: Game Assets: Substance Painter, Substance Modeler, Game Asset Workflows](assignments/week_4_game_assets_substance_painter_substance_modeler_game_asset_workflows.html)
5. [Week 5: Sound Design, Animation, Primitives in Substance Modeler, Compiling the Game, and VFX (shaders and particles)](assignments/week_5_sound_design_animation_primitives_in_substance_modeler_compiling_the_game_and_vfx_shaders_and_particles.html)
6. [Week 6: Adding a start screen, Using LLM's for Unity Scripting](assignments/week_6_adding_a_start_screen_using_llms_for_unity_scripting.html)
7. [Week 7: Adding a Collectable or Key Mechanic to the Game](assignments/week_7_adding_a_collectable_or_key_mechanic_to_the_game.html)
8. [Week 8: Rolling Ball Game Final](assignments/week_8_rolling_ball_game_final.html)

**Unreal Engine Phase (Weeks 9-14)**
9. [Week 9: Introduction to the Epic Eco-System and Unreal Engine](assignments/week_9_introduction_to_the_epic_eco_system_and_unreal_engine.html)
10. [Week 10: First person collection in Unreal Engine](assignments/week_10_first_person_collection_in_unreal_engine.html)
11. [Week 11: Authoring Assets for Unreal Engine, creating animation in Shaders, and triggering Particle and Sound FX](assignments/week_11_authoring_assets_for_unreal_engine_creating_animation_in_shaders_and_triggering_particle_and_sound_fx.html)
12. [Week 12: Programming the Collection Count in Blueprints, Creating doors in Blueprints](assignments/week_12_programming_the_collection_count_in_blueprints_creating_doors_in_blueprints.html)
13. [Week 13: Building the game in Unreal, Recording gameplay, Adding Messages and Sound FX](assignments/week_13_building_the_game_in_unreal_recording_gameplay_adding_messages_and_sound_fx_.html)
14. [Week 14: Final Portfolio Requirements: Using Mixamo in Unreal, Creating environmental sounds, Rain in the Particle System](assignments/week_14_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system.html)

**Final Portfolio**
15. [Week 15: Final Portfolio Requirements: 25% of the course grade](assignments/week_15_final_portfolio_requirements_25_of_the_course_grade_final_submission.html)

**Week 16: Course Wrap-up** (No Assignment - Final Presentations)

## Features

- **Lecture Redirect System**: YouTube lecture links use the redirect system at `https://caseyfarina.github.io/lecture-redirects/` for easy maintenance
- **Standardized Headers**: All assignments use consistent H2 heading structure with bold formatting
- **Accessibility**: Images include descriptive alt text for screen readers
- **Week Organization**: Assignments for weeks 1-15 with week 16 reserved for final presentations

## Technical Notes

- Course uses both Unity (weeks 1-8) and Unreal Engine (weeks 9-14)
- Assignments include game development workflows, asset creation, and programming concepts
- Final portfolio represents 25% of course grade
- Course integrates 3D modeling (Blender), texturing (Substance suite), and game engines

## Course Structure

**Phase 1: Unity Foundation** (Weeks 1-8)
- Unity interface and basic animation
- Asset creation workflows with Blender and Substance
- Game mechanics implementation
- Audio integration and visual effects
- Rolling ball game completion

**Phase 2: Unreal Engine** (Weeks 9-14)  
- Epic ecosystem and Unreal Engine introduction
- Blueprint visual scripting
- Advanced game mechanics and level design
- Asset optimization for real-time rendering
- Advanced portfolio development

**Phase 3: Final Portfolio** (Week 15)
- Project compilation and final submission
- Professional portfolio presentation

**Phase 4: Course Conclusion** (Week 16)
- Final presentations and course wrap-up
- No assignment due
"""
    
    index_file.write_text(new_content, encoding='utf-8')
    print("\n=== Updated GitHub Pages index for weeks 1-15 ===")

if __name__ == "__main__":
    renumber_to_week1()