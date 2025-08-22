import shutil
from pathlib import Path

def manual_copy_assignments():
    """Manually copy assignments to correct extracted course folders"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Manual mapping based on the assignment mapping JSON structure
    manual_mapping = {
        'Week 1 - Introduction to Blender.html': 'g36450a0839599fd7909acf76c13b40b0/week-1-introduction-to-blender.html',
        'Week 2 - Bezier Curves Creating 3D Shapes.html': 'g8220ab6adee6ec8f84bf9f6012f57f26/week-2-bezier-curves-creating-3d-shapes-from-2d-curves.html',
        'Week 3 - Modifiers and Rendering.html': 'g6b72bfaf2319de56b62847c8baf810f2/modifiers-and-rendering-constructing-a-scene-from-multipart-objects.html',
        'Week 4 - Rendering Compositing and Remesh.html': 'g20f59e25f3fa3656d818e757af72613e/rendering-compositing-and-basic-remesh-workflow.html',
        'Week 5 - Materials Hard Surface vs Sculpting.html': 'ged670864b6f6dbe659f5d703882cb069/materials-hard-surface-vs-sculpting-workflow.html',
        'Week 6 - Introduction to Substance Painter.html': 'gf996147eab481787e5c4f5626a295d61/introduction-to-substance-painter.html',
        'Week 7 - Introduction to UV Unwrapping.html': 'g17408bb11ac5ff71e18579d04bfb57d8/introduction-to-uv-unwrapping.html',
        'Week 8 - Modeling Foliage and UV Details.html': 'g8407165939ff80ce73f7945689263009/modeling-foliage-uv-details-playground-showcase-video.html',
        'Week 9 - Modeling to Scale and UV Packing.html': 'g189401cb9fa253cbe434a381802a6596/modeling-to-scale-and-uv-packing.html',
        'Week 10 - Substance Painter Techniques.html': 'g410b9f6fbc39e616a90ed53576e640dd/substance-painter-techniques.html',
        'Week 11 - Lamp Revisions.html': 'gdcd12c342fa682a3f61b3fe296bb137f/lamp-revisions.html',
        'Week 12 - Kitchen Table and Chairs.html': 'g515785273d32271ea7c08468191b15c6/kitchen-modeling-kitchen-table-and-chairs.html',
        'Week 13 - Kitchen Silverware.html': 'gd9f812b003cb8f2a4c56a849d0a7f958/kitchen-modeling-silverware-and-antique-silverware.html',
        'Week 14 - Kitchen Plates and Napkins.html': 'gaae5c0e89b19779012112987a61f4773/kitchen-plates-and-napkins.html',
        'Week 15 - Final Portfolio.html': 'ga45c0a38ed19157066c2b34c30e682af/final-portfolio-requirements-25-percent-of-the-course-grade.html',
        'Technology Login Challenge TLC.html': 'gd948913ca32ac0d123c2119940756c91/week-1-technology-login-challenge-3.html'
    }
    
    for assignment_file, dest_path in manual_mapping.items():
        source_file = assignments_path / assignment_file
        dest_file = extracted_path / dest_path
        
        if source_file.exists() and dest_file.parent.exists():
            shutil.copy2(source_file, dest_file)
            print(f"Copied {assignment_file} -> {dest_path}")
        else:
            if not source_file.exists():
                print(f"Warning: Source file {assignment_file} not found")
            if not dest_file.parent.exists():
                print(f"Warning: Destination folder {dest_file.parent} not found")

if __name__ == "__main__":
    manual_copy_assignments()
    print("Manual assignment copying completed!")