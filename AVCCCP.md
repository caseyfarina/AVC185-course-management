# AVC Course Compliance Protocol (AVCCCP)

## Overview
The AVC Course Compliance Protocol (AVCCCP) is a standardized workflow for processing Canvas IMSCC course files to achieve complete accessibility compliance and content standardization. This protocol ensures YuJa Panorama accessibility compliance, proper course competency mapping, and consistent formatting across all course materials.

## Protocol Steps

### Phase 1: Course Extraction and Organization
1. **Extract IMSCC files** - Convert and extract course content
2. **Extract assignments** - Organize assignments into readable structure
3. **Create assignment mapping** - Track file relationships for repackaging

### Phase 2: Content Structure and Dating
4. **Update due dates** - Apply course-specific scheduling
5. **Add week numbers** - Standardize assignment naming with "Week N:" prefixes
6. **Replace YouTube links** - Convert to permanent redirect links

### Phase 3: Accessibility Compliance
7. **Fix heading structure** - Implement H1 title + H2 sections for YuJa compliance
8. **Add course competencies** - Map assignments to institutional learning objectives
9. **Convert PNG to JPEG** - Optimize images for faster loading
10. **Audit and improve alt text** - Ensure descriptive, non-generic image descriptions

### Phase 4: Content Standardization
11. **Standardize text formatting** - Apply 12pt font while preserving intentional styling
12. **Resize images** - Standardize to 200px height maintaining aspect ratios
13. **Add project objectives** - Generate meaningful objectives for empty sections

### Phase 5: Technical Finalization
14. **Fix XML formatting** - Critical step for Canvas compatibility
15. **Repackage IMSCC** - Create final course package

### Phase 6: Quality Assurance
16. **Run unit check** - Verify all compliance points achieved

## AVCCCP Unit Check Criteria

### ✅ Accessibility Compliance
- [ ] All assignments have proper H1 title + H2 section structure
- [ ] No H3 or other heading levels present
- [ ] All images have descriptive, non-generic alt text
- [ ] All hyperlinks have descriptive link text (not generic "click here")

### ✅ Content Standards
- [ ] All assignments have course competencies matching MCCCD mapping
- [ ] All Project Objective sections contain meaningful objectives
- [ ] YouTube links converted to permanent redirect format
- [ ] Week numbers added to assignments 1-14 (not TLC or Final Portfolio)

### ✅ Technical Standards
- [ ] All text standardized to 12pt font size
- [ ] All images converted from PNG to JPEG format
- [ ] All images resized to 200px height with maintained aspect ratios
- [ ] XML namespace formatting compatible with Canvas

### ✅ File Organization
- [ ] Assignment mapping JSON created and maintained
- [ ] Files properly copied between assignments and extracted_course folders
- [ ] IMSCC package successfully created with timestamp

## Course-Specific Customizations

When applying AVCCCP to different courses, customize:
- **Class code** in YouTube redirect links (avc185, avc240, etc.)
- **Week patterns** for assignment naming in `add_week_numbers.py`
- **Due date schedules** based on course calendar
- **Course competencies** using appropriate MCCCD mapping file

## Critical Success Factors

1. **Always run XML formatting fix** - Canvas import will fail without proper namespace formatting
2. **Preserve file tokens** - Maintain `$IMS-CC-FILEBASE$` references for Canvas compatibility
3. **Use UTF-8 encoding** - Prevent encoding issues across all operations
4. **Test systematically** - Run unit check to verify all criteria before deployment

## Protocol Execution Scripts

The AVCCCP relies on the following standardized scripts (adapted per course):
- `extract_imscc.py`
- `extract_assignments.py`
- `update_due_dates.py`
- `add_week_numbers.py`
- `replace_youtube_links.py`
- `fix_heading_structure.py`
- `add_course_competencies.py`
- `convert_png_to_jpeg.py`
- `audit_alt_text.py`
- `standardize_formatting.py`
- `resize_images.py`
- `add_project_objectives.py`
- `fix_xml_formatting.py`
- `repackage_imscc.py`
- `unit_check.py`

## Quality Assurance
Always test IMSCC imports in Canvas with a backup course before deploying to live courses.