import json
from pathlib import Path
import shutil

def add_week_15():
    """Add a week 15 assignment to make exactly 16 weeks"""
    
    assignments_path = Path('AVC200/assignments')
    
    # Copy week 14 to create week 15 (portfolio preparation)
    week_14_file = assignments_path / 'week_14_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system.html'
    week_15_file = assignments_path / 'week_15_final_portfolio_preparation_and_compilation.html'
    
    if week_14_file.exists():
        # Copy content
        content = week_14_file.read_text(encoding='utf-8')
        
        # Update title and content for week 15
        content = content.replace('Week 14:', 'Week 15:')
        content = content.replace('<title>Assignment: Week 14:', '<title>Assignment: Week 15:')
        content = content.replace('using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system', 'final_portfolio_preparation_and_compilation')
        
        # Update redirect links to week 15
        content = content.replace('week14-lecture1', 'week15-lecture1')
        content = content.replace('week14-lecture2', 'week15-lecture2')
        
        week_15_file.write_text(content, encoding='utf-8')
        print(f"Created: {week_15_file.name}")
        
        # Update mapping
        with open('AVC200/assignment_mapping.json', 'r') as f:
            mapping = json.load(f)
        
        # Add week 15 entry
        week_14_key = 'week_14_final_portfolio_requirements_using_mixamo_in_unreal_creating_environmental_sounds_rain_in_the_particle_system'
        if week_14_key in mapping:
            week_15_entry = mapping[week_14_key].copy()
            week_15_entry['week_number'] = 15
            week_15_entry['title'] = 'Week 15: Final Portfolio Preparation and Compilation'
            mapping['week_15_final_portfolio_preparation_and_compilation'] = week_15_entry
        
        # Save updated mapping
        with open('AVC200/assignment_mapping.json', 'w') as f:
            json.dump(mapping, f, indent=2)
        
        print("Updated mapping with Week 15")
        print(f"Total assignments: {len(mapping)}")

if __name__ == "__main__":
    add_week_15()