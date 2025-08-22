import json
from pathlib import Path
import shutil

def adjust_avc285_to_15():
    """Add one more assignment to make exactly 15 for AVC285"""
    
    assignments_path = Path('AVC285/assignments')
    
    # Check current assignments
    current_files = list(assignments_path.glob('*.html'))
    print(f"Current assignments: {len(current_files)}")
    
    if len(current_files) == 14:
        # Duplicate week 14 to create week 15 (VDM brushes advanced)
        week_14_file = assignments_path / 'week_14_sculpting_in_blender_using_vdm_brushes.html'
        week_15_file = assignments_path / 'week_15_advanced_vdm_techniques_and_final_portfolio.html'
        
        if week_14_file.exists():
            # Copy content
            content = week_14_file.read_text(encoding='utf-8')
            
            # Update title and content for week 15
            content = content.replace('Week 14:', 'Week 15:')
            content = content.replace('<title>Assignment: Week 14:', '<title>Assignment: Week 15:')
            
            # Update any redirect links to week 15
            content = content.replace('week14-lecture1', 'week15-lecture1')
            content = content.replace('week14-lecture2', 'week15-lecture2')
            
            week_15_file.write_text(content, encoding='utf-8')
            print(f"Created: {week_15_file.name}")
            
            # Update mapping
            with open('AVC285/assignment_mapping.json', 'r') as f:
                mapping = json.load(f)
            
            # Add week 15 entry based on week 14
            week_14_key = 'week_14_sculpting_in_blender_using_vdm_brushes'
            if week_14_key in mapping:
                week_15_entry = mapping[week_14_key].copy()
                week_15_entry['week_number'] = 15
                week_15_entry['title'] = 'Week 15: Advanced VDM Techniques and Final Portfolio'
                week_15_entry['original_title'] = 'Advanced VDM Techniques and Final Portfolio'
                mapping['week_15_advanced_vdm_techniques_and_final_portfolio'] = week_15_entry
            
            # Save updated mapping
            with open('AVC285/assignment_mapping.json', 'w') as f:
                json.dump(mapping, f, indent=2)
            
            print("Updated mapping with Week 15")
            print(f"Total assignments: {len(mapping)}")
        else:
            print("Week 14 file not found")
    else:
        print(f"Expected 14 assignments, found {len(current_files)}")

if __name__ == "__main__":
    adjust_avc285_to_15()