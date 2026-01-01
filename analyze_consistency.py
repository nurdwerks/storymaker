import json
import re

def parse_book_chapter(book_str, chapter_str):
    # Extract numbers
    book_num = 0
    match_b = re.search(r'\d+', book_str)
    if match_b:
        book_num = int(match_b.group())
        
    chapter_num = 0
    # Handle "Chapter 01", "Chapter 1", etc.
    match_c = re.search(r'\d+', chapter_str)
    if match_c:
        chapter_num = int(match_c.group())
        
    return book_num, chapter_num

def analyze_continuity(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    report = []
    
    for char_name, events in data.items():
        last_book = -1
        last_chapter = -1
        
        char_errors = []
        
        for i, event in enumerate(events):
            b_str = event.get("Book", "")
            c_str = event.get("Chapter", "")
            desc = event.get("Description", "")
            
            b_num, c_num = parse_book_chapter(b_str, c_str)
            
            if b_num < last_book:
                char_errors.append(f"Sequential Error: Book {b_num} (Chapter {c_num}) appears after Book {last_book}")
            elif b_num == last_book:
                if c_num < last_chapter:
                    char_errors.append(f"Sequential Error: Chapter {c_num} appears after Chapter {last_chapter} in Book {b_num}")
            
            last_book = b_num
            last_chapter = c_num
            
            # Check for generic nonsense or placeholders
            if "description" in desc.lower() and len(desc) < 20:
                 char_errors.append(f"Potential Placeholder: '{desc}'")

        if char_errors:
            report.append(f"### {char_name}")
            for err in char_errors:
                report.append(f"- {err}")
            report.append("")
            
    if not report:
        report.append("No sequential errors detected.")
        
    return "\n".join(report)

if __name__ == "__main__":
    report = analyze_continuity("consistency_summary.json")
    print(report)
    
    with open("consistency_report.md", "w", encoding='utf-8') as f:
        f.write("# Consistency Analysis Report\n\n")
        f.write(report)
