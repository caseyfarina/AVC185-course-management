#!/usr/bin/env python3
"""
Update Final Portfolio YouTube links with redirect links
"""

from pathlib import Path

def update_final_portfolio():
    """Update Final Portfolio YouTube links"""
    
    final_portfolio_file = Path(__file__).parent / "assignments" / "final_portfolio_requirements_25_percent_of_the_course_grade.html"
    
    if not final_portfolio_file.exists():
        print("Final portfolio file not found")
        return
    
    # Read the file
    with open(final_portfolio_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace YouTube links
    content = content.replace(
        'href="https://www.youtube.com/watch?v=tHIopRvd5qY"',
        'href="https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture1"'
    )
    
    content = content.replace(
        'https://www.youtube.com/watch?v=tHIopRvd5qY</a>',
        'https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture1</a>'
    )
    
    content = content.replace(
        'href="https://www.youtube.com/watch?v=f4toulfEQ3o"',
        'href="https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture2"'
    )
    
    content = content.replace(
        'https://www.youtube.com/watch?v=f4toulfEQ3o</a>',
        'https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture2</a>'
    )
    
    # Write back to file
    with open(final_portfolio_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Final Portfolio YouTube links updated successfully")
    print("Updated links:")
    print("  - https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture1")
    print("  - https://caseyfarina.github.io/lecture-redirects/?class=avc185&lecture=final-lecture2")

if __name__ == "__main__":
    update_final_portfolio()