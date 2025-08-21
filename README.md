# Multi-Course Canvas Management Project

Canvas IMSCC course editing workflow for multiple courses: AVC185, AVC240, AVC200, AVC285.

## Project Structure

```
course-management/
├── README.md                    # This file
├── CLAUDE.md                   # Complete workflow documentation
├── scripts/                    # Python workflow scripts (shared)
├── AVC185/                     # 3D Modeling and Animation I
│   ├── assignments/            # Extracted assignment HTML files
│   ├── extracted_course/       # Extracted IMSCC content
│   ├── assignment_mapping.json # File mapping
│   ├── _config.yml             # GitHub Pages config
│   └── index.md                # Course index
├── AVC240/                     # Advanced Cinematography
│   ├── assignments/            # Extracted assignment HTML files
│   ├── extracted_course/       # Extracted IMSCC content
│   ├── assignment_mapping.json # File mapping
│   ├── _config.yml             # GitHub Pages config
│   └── index.md                # Course index
├── AVC200/                     # (Future course)
└── AVC285/                     # (Future course)
```

## Courses

### AVC185 - 3D Modeling and Animation I
- **Status**: Complete with updated lecture redirects (class=avc185)
- **Assignments**: 15 weekly assignments + TLC + Final Portfolio
- **Lecture Links**: Updated to use redirect format

### AVC240 - Advanced Cinematography  
- **Status**: Complete with updated lecture redirects (class=avc240)
- **Assignments**: 17 assignments covering camera theory, composition, lighting, motion
- **Lecture Links**: Updated to match week numbers (week1-lecture1, week1-lecture2, etc.)

## Key Features

- ✅ **Multi-course support** - Organized folder structure for multiple classes
- ✅ **Lecture redirect system** - Permanent YouTube redirect links by class and week
- ✅ **IMSCC workflow** - Extract, edit, rebuild workflow (preferred approach)
- ✅ **Week-matched links** - Lecture redirects match assignment week numbers
- ✅ **Canvas-compatible** - Proper XML formatting for successful imports

## Workflow Scripts

Located in `scripts/` folder (shared across all courses):

- `extract_imscc.py` - Extract IMSCC files
- `extract_assignments.py` - Extract assignments to editable HTML
- `update_due_dates.py` - Update assignment due dates
- `add_week_numbers.py` - Add week prefixes to assignments
- `replace_youtube_links.py` - Update YouTube redirect links
- `fix_xml_formatting.py` - Fix Canvas XML compatibility (CRITICAL)
- `repackage_imscc.py` - Create new IMSCC package

## Usage

### Complete Workflow Steps
1. **Extract IMSCC**: `python extract_imscc.py`
2. **Extract Assignments**: `python extract_assignments.py`
3. **Update Due Dates**: `python update_due_dates.py`
4. **Add Week Numbers**: `python add_week_numbers.py`
5. **Replace YouTube Links**: `python replace_youtube_links.py`
6. **Fix XML Formatting**: `python fix_xml_formatting.py` (CRITICAL)
7. **Repackage**: `python repackage_imscc.py`

### Course-Specific Customizations
When adapting for new courses:
- Update class code in YouTube redirect links
- Modify week patterns in assignment scripts
- Adjust due date schedules
- Update assignment group references if needed

## Lecture Redirect System

**Format**: `https://caseyfarina.github.io/lecture-redirects/?class={CLASS}&lecture=week{N}-lecture{X}`

**Examples**:
- `?class=avc185&lecture=week1-lecture1`
- `?class=avc240&lecture=week5-lecture2`

## Important Notes

- **Preferred Workflow**: IMSCC → parse → edit → rebuild IMSCC
- **GitHub Pages/iframe embedding**: Discontinued due to security and accessibility concerns
- **XML Formatting**: Always run `fix_xml_formatting.py` after XML modifications
- **Testing**: Test IMSCC imports in Canvas with backup courses before live deployment
