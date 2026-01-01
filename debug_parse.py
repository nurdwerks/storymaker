
import re
import os

filepath = r"c:\Users\bryan\Documents\storymaker\Characters\Character Profile_ Lady Corinne (The Porcelain Doll).md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

table_match = re.search(r'## Consistency Check\s*\n\s*\|(.*?)(?=\n\n|\n## |\Z)', content, re.DOTALL)

if not table_match:
    print("No table found")
    exit()

table_content = table_match.group(0)
print(f"Table content length: {len(table_content)}")

books = {}

for line in table_content.split('\n'):
    if line.startswith('|') and 'Book' in line:
        parts = [p.strip() for p in line.split('|')]
        # print(f"Processing: {parts[1]} - {parts[2]}")
        if len(parts) >= 3:
            book_match = re.search(r'Book\s*(\d+)', parts[1])
            chapter_match = re.search(r'Chapter\s*(\d+)', parts[2])
            if book_match and chapter_match:
                book_num = int(book_match.group(1))
                chapter_num = int(chapter_match.group(1))
                if book_num == 6:
                    print(f"Found Ch {chapter_num}")
                    
