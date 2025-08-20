# AVC185 Course Management Project

Canvas IMSCC course editing workflow for AVC185 - 3D Modeling and Animation I (Fall 2025).

## Project Structure

```
AVC185_project/
├── README.md                    # This file
├── CLAUDE.md                   # Complete workflow documentation
├── updated_course_*.imscc      # Final corrected IMSCC file
├── assignments/                # Extracted assignment HTML files
├── extracted_course/           # Extracted IMSCC content
├── scripts/                    # Python workflow scripts
├── archive/                    # Original and intermediate IMSCC files
└── temp/                       # Temporary files (mapping, etc.)
```

## Quick Start

1. **Current Status**: All assignments have been reordered and corrected according to the proper sequence
2. **Latest IMSCC**: `updated_course_20250819_210609.imscc` - ready for Canvas import
3. **Documentation**: See `CLAUDE.md` for complete workflow and reusable scripts

## Assignment Order (Corrected)

1. Week 1: Introduction to Blender
2. Week 2: Bezier Curves
3. Week 3: Modifiers and Rendering
4. Week 4: Rendering, Compositing and Basic Remesh Workflow
5. Week 5: Materials, Hard Surface VS Sculpting workflow
6. Week 6: Introduction to Substance Painter
7. Week 7: Introduction to UV Unwrapping
8. Week 8: Modeling Foliage, UV details, Playground Showcase Video
9. Week 9: Modeling to Scale and UV Packing
10. Week 10: Substance Painter Techniques
11. Week 11: Lamp Revisions
12. Week 12: Kitchen: Kitchen Table and Chairs
13. Week 13: Kitchen: Modeling Silverware, and Antique Silverware
14. Week 14: Kitchen: Plates and Napkins

## Scripts Overview

- `extract_imscc.py` - Extract IMSCC files
- `extract_assignments.py` - Extract assignments to editable HTML
- `fix_correct_order.py` - Apply correct assignment sequence
- `fix_all_redirect_links.py` - Update YouTube redirect links
- `fix_xml_formatting.py` - Fix Canvas XML compatibility
- `repackage_imscc.py` - Create new IMSCC package

## Key Features Implemented

- ✅ Correct assignment week numbering
- ✅ Updated due dates (Tuesdays 8PM, TLC Thursday 8PM)
- ✅ YouTube redirect links with proper week numbers
- ✅ Canvas-compatible XML formatting
- ✅ File organization and cleanup

## Usage

For similar courses, copy `CLAUDE.md` to new projects as it contains the complete reusable workflow.

### Workflow Summary
1. Extract IMSCC: `python scripts/extract_imscc.py`
2. Extract assignments: `python scripts/extract_assignments.py`
3. Make edits to assignments and settings
4. Fix formatting: `python scripts/fix_xml_formatting.py`
5. Repackage: `python scripts/repackage_imscc.py`

## File References

Assignment HTML files reference resources using `$IMS-CC-FILEBASE$` tokens:
- Images: `$IMS-CC-FILEBASE$/Uploaded%20Media/image-xyz.png`
- PDFs: `$IMS-CC-FILEBASE$/Uploaded%20Media/syllabus.pdf`

These tokens are automatically resolved by Canvas during import.