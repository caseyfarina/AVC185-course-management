import os
import shutil
from pathlib import Path
import urllib.parse
import xml.etree.ElementTree as ET

def generate_github_pages_imscc():
    """Generate IMSCC with iframe assignments pointing to GitHub Pages"""
    
    # GitHub Pages URL (will be available after enabling Pages)
    github_user = "caseyfarina"
    github_repo = "AVC185-course-management"
    
    # GitHub Pages URL format
    base_url = f"https://{github_user.lower()}.github.io/{github_repo}/assignments/"
    
    # Copy existing extracted course as base
    output_dir = Path('github_pages_course')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree('extracted_course', output_dir)
    
    # Direct title-to-filename mapping
    title_mapping = {
        'Week 1: Introduction to Blender': 'Week 1 - Introduction to Blender.html',
        'Week 2: Bezier Curves: Creating 3D shapes from 2D Curves': 'Week 2 - Bezier Curves Creating 3D Shapes.html',
        'Week 3: Modifiers and Rendering: Constructing a scene from Multipart Objects': 'Week 3 - Modifiers and Rendering.html',
        'Week 4: Rendering, Compositing and Basic Remesh Workflow': 'Week 4 - Rendering Compositing and Remesh.html',
        'Week 5: Materials, Hard Surface VS Sculpting workflow': 'Week 5 - Materials Hard Surface vs Sculpting.html',
        'Week 6: Introduction to Substance Painter': 'Week 6 - Introduction to Substance Painter.html',
        'Week 7: Introduction to UV Unwrapping': 'Week 7 - Introduction to UV Unwrapping.html',
        'Week 8: Modeling Foliage, UV details, Playground Showcase Video': 'Week 8 - Modeling Foliage and UV Details.html',
        'Week 9: Modeling to Scale and UV Packing': 'Week 9 - Modeling to Scale and UV Packing.html',
        'Week 10: Substance Painter Techniques': 'Week 10 - Substance Painter Techniques.html',
        'Week 11: Lamp Revisions': 'Week 11 - Lamp Revisions.html',
        'Week 12: Kitchen Modeling: Kitchen Table and Chairs': 'Week 12 - Kitchen Table and Chairs.html',
        'Week 13: Kitchen: Modeling Silverware, and Antique Silverware': 'Week 13 - Kitchen Silverware.html',
        'Week 14: Kitchen: Plates and Napkins': 'Week 14 - Kitchen Plates and Napkins.html',
        'Final Portfolio Requirements 25% of the course grade': 'Week 15 - Final Portfolio.html',
        'Technology Login Challenge (TLC)': 'Technology Login Challenge TLC.html',
    }
    
    print(f"Converting assignments to GitHub Pages iframe format...")
    print(f"GitHub Pages URL: {base_url}")
    
    # Process each assignment folder
    for folder in output_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('g') and len(folder.name) > 20:
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                title = get_assignment_title(xml_file)
                if title:
                    clean_title = title.strip()
                    
                    # Find exact match or fuzzy match
                    github_filename = None
                    
                    if clean_title in title_mapping:
                        github_filename = title_mapping[clean_title]
                    else:
                        github_filename = fuzzy_match_title(clean_title, title_mapping)
                    
                    if github_filename:
                        # URL encode the filename for GitHub Pages
                        encoded_filename = urllib.parse.quote(github_filename)
                        github_pages_url = base_url + encoded_filename
                        
                        # Create iframe HTML content
                        iframe_html = create_github_pages_iframe_html(clean_title, github_pages_url)
                        
                        # Replace the HTML file content
                        html_files = list(folder.glob('*.html'))
                        if html_files:
                            html_files[0].write_text(iframe_html, encoding='utf-8')
                            print(f"[OK] {clean_title} -> {github_pages_url}")
                        else:
                            print(f"[WARNING] No HTML file found in {folder.name}")
                    else:
                        print(f"[WARNING] No mapping found for: '{clean_title}'")
    
    print(f"\nGitHub Pages course generated in: {output_dir}")
    print("Next: Enable GitHub Pages in repository settings, then create IMSCC package")

def get_assignment_title(xml_file):
    """Extract assignment title from XML file"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
        if title_elem is not None:
            return title_elem.text
    except Exception as e:
        print(f"Error reading {xml_file}: {e}")
    return None

def fuzzy_match_title(title, title_mapping):
    """Find best match for title using fuzzy matching"""
    title_lower = title.lower()
    
    # Check for week numbers first
    for week_num in range(1, 16):
        if f'week {week_num}:' in title_lower:
            for mapped_title, filename in title_mapping.items():
                if f'week {week_num}:' in mapped_title.lower():
                    return filename
    
    # Check for specific keywords
    if 'final portfolio' in title_lower:
        return title_mapping.get('Final Portfolio Requirements 25% of the course grade')
    elif 'technology login challenge' in title_lower or 'tlc' in title_lower:
        return title_mapping.get('Technology Login Challenge (TLC)')
    
    # Keyword-based matching
    keyword_matches = {
        'introduction.*blender': 'Week 1 - Introduction to Blender.html',
        'bezier.*curves': 'Week 2 - Bezier Curves Creating 3D Shapes.html',
        'modifiers.*rendering': 'Week 3 - Modifiers and Rendering.html',
        'rendering.*compositing': 'Week 4 - Rendering Compositing and Remesh.html',
        'materials.*hard.*surface': 'Week 5 - Materials Hard Surface vs Sculpting.html',
        'introduction.*substance.*painter': 'Week 6 - Introduction to Substance Painter.html',
        'introduction.*uv.*unwrapping': 'Week 7 - Introduction to UV Unwrapping.html',
        'modeling.*foliage': 'Week 8 - Modeling Foliage and UV Details.html',
        'modeling.*scale': 'Week 9 - Modeling to Scale and UV Packing.html',
        'substance.*painter.*techniques': 'Week 10 - Substance Painter Techniques.html',
        'lamp.*revisions': 'Week 11 - Lamp Revisions.html',
        'kitchen.*table': 'Week 12 - Kitchen Table and Chairs.html',
        'kitchen.*silverware': 'Week 13 - Kitchen Silverware.html',
        'kitchen.*plates': 'Week 14 - Kitchen Plates and Napkins.html',
    }
    
    import re
    for pattern, filename in keyword_matches.items():
        if re.search(pattern, title_lower):
            return filename
    
    return None

def create_github_pages_iframe_html(assignment_title, github_pages_url):
    """Create HTML content with iframe pointing to GitHub Pages"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Assignment: {assignment_title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 1.2em;
            font-weight: 600;
        }}
        .header p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .iframe-container {{
            position: relative;
            width: 100%;
            height: calc(100vh - 80px);
            min-height: 600px;
            background: white;
            border-radius: 8px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }}
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #666;
            text-align: center;
        }}
        .loading::after {{
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #667eea;
            border-radius: 50%;
            border-top: 3px solid transparent;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .fallback {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            z-index: 100;
        }}
        .fallback a {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.85em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }}
        .fallback a:hover {{
            background: #5a6fd8;
            transform: translateY(-1px);
        }}
        @media (max-width: 768px) {{
            .iframe-container {{
                margin: 5px;
                height: calc(100vh - 90px);
                border-radius: 0;
            }}
            .header {{
                padding: 10px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{assignment_title}</h1>
        <p>Live content from GitHub • AVC185 Fall 2025</p>
    </div>
    
    <div class="iframe-container">
        <div class="loading" id="loading">Loading assignment content</div>
        <iframe src="{github_pages_url}" 
                title="{assignment_title}"
                onload="document.getElementById('loading').style.display='none';"
                onerror="document.getElementById('loading').innerHTML='Failed to load content. Try the direct link below.';">
        </iframe>
        <div class="fallback">
            <a href="{github_pages_url}" target="_blank">Open Direct</a>
        </div>
    </div>
    
    <script>
        // Auto-adjust iframe height
        function adjustLayout() {{
            const container = document.querySelector('.iframe-container');
            const header = document.querySelector('.header');
            if (container && header) {{
                const headerHeight = header.offsetHeight;
                container.style.height = `calc(100vh - ${{headerHeight + 20}}px)`;
            }}
        }}
        
        window.addEventListener('resize', adjustLayout);
        window.addEventListener('load', adjustLayout);
        
        // Hide loading after timeout
        setTimeout(() => {{
            const loading = document.getElementById('loading');
            if (loading && loading.style.display !== 'none') {{
                loading.innerHTML = 'Content is taking longer than expected. <br><a href="{github_pages_url}" target="_blank" style="color: #667eea;">Click here to open directly</a>';
            }}
        }}, 10000);
    </script>
</body>
</html>'''

if __name__ == "__main__":
    generate_github_pages_imscc()