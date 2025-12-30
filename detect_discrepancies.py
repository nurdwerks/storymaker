import os
import re

def analyze_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(file_path)
    character_name = filename.replace("Character Profile_ ", "").replace(".md", "")
    
    # 1. Check Metadata (Arc Coverage in Narrative Section)
    narrative_arc_pattern = re.compile(r'## VI\. Narrative Arc & Character Growth(.*?)(## VII|$)', re.DOTALL)
    narrative_match = narrative_arc_pattern.search(content)
    
    narrative_books = set()
    if narrative_match:
        narrative_text = narrative_match.group(1)
        # Look for headers like "### Book 1", "### Book 5", etc.
        book_headers = re.findall(r'### (Book \d+)', narrative_text)
        narrative_books = set(book_headers)

    # 2. Check Consistency Check Table
    consistency_pattern = re.compile(r'## Consistency Check(.*?)$', re.DOTALL)
    consistency_match = consistency_pattern.search(content)
    
    consistency_books = set()
    last_event_book = None
    last_event_chapter = None
    
    if consistency_match:
        table_text = consistency_match.group(1)
        # Look for rows starting with "| Book X"
        # Assuming format "| Book 1 | ..."
        rows = re.findall(r'\|\s*(Book \d+)\s*\|\s*(Chapter \d+)', table_text)
        for b, c in rows:
            consistency_books.add(b)
            last_event_book = b
            last_event_chapter = c

    # 3. Findings
    issues = []
    
    # Check for missing books (Arc mentions it, but no events found)
    for book in narrative_books:
        if book not in consistency_books:
            issues.append(f"Narrative describes {book}, but no events found in Consistency Check.")

    # Check for extra books (Consistency has it, but Narrative doesn't - less critical but interesting)
    # for book in consistency_books:
    #     if book not in narrative_books:
    #         issues.append(f"Consistency Check has events for {book}, but Narrative Arc does not mention it.")

    # Check for completely empty table
    if not consistency_books:
        issues.append("Consistency Check table is empty or missing.")

    return issues

def main():
    characters_dir = r"c:\Users\bryan\Documents\storymaker\Characters"
    findings_file = r"c:\Users\bryan\Documents\storymaker\Findings.md"
    
    all_issues = []
    
    for filename in os.listdir(characters_dir):
        if filename.endswith(".md"):
            path = os.path.join(characters_dir, filename)
            char_issues = analyze_profile(path)
            if char_issues:
                char_name = filename.replace("Character Profile_ ", "").replace(".md", "")
                for issue in char_issues:
                    all_issues.append(f"- **{char_name}**: {issue}")

    # Read existing findings to preserve them? 
    # The prompt says "Note any discrepancies in Findings.md. Only note discrepancies."
    # I should probably append or rewrite. I'll rewrite the specific section.
    
    # Write to a file
    with open("consistencies_report.txt", "w", encoding='utf-8') as f:
        if all_issues:
            f.write("# Detected Discrepancies\n\n")
            for issue in sorted(all_issues):
                f.write(f"{issue}\n")
        else:
            f.write("No structural discrepancies found.")
            
    print("Report generated at consistencies_report.txt")

if __name__ == "__main__":
    main()
