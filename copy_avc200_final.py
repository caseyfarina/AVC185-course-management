from pathlib import Path
import shutil

def copy_avc200_final():
    """Copy final AVC200 assignments back to extracted_course"""
    
    # We need to manually map the new filenames to their original folders
    # Based on the original extraction, we can reconstruct the mapping
    
    assignments_path = Path('AVC200/assignments')
    extracted_path = Path('AVC200/extracted_course')
    
    # Get all assignment folders
    assignment_folders = [f for f in extracted_path.iterdir() if f.is_dir() and f.name.startswith('g') and len(f.name) > 20]
    
    print("=== Available assignment folders ===")
    for folder in assignment_folders:
        print(f"  {folder.name}")
    
    print(f"\n=== Current assignment files ===")
    assignment_files = list(assignments_path.glob('*.html'))
    for file in sorted(assignment_files):
        print(f"  {file.name}")
    
    print(f"\n=== Copying {len(assignment_files)} assignments back to extracted_course ===")
    
    # For now, let's just copy them to the first available folders
    # This is a simplified approach since the exact mapping was lost during renaming
    
    for i, assignment_file in enumerate(sorted(assignment_files)):
        if i < len(assignment_folders):
            target_folder = assignment_folders[i]
            
            # Find the HTML file in the target folder
            html_files = list(target_folder.glob('*.html'))
            if html_files:
                target_file = html_files[0]  # Use the first HTML file found
                
                # Copy the updated assignment
                shutil.copy2(assignment_file, target_file)
                print(f"  Copied {assignment_file.name} -> {target_folder.name}/{target_file.name}")
    
    print(f"\n=== AVC200 assignments copied back to extracted_course ===")

if __name__ == "__main__":
    copy_avc200_final()