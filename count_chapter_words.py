
import os
import re
import json

def count_words(text):
    return len(text.split())

def analyze_book(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by Chapter headers (### Chapter X)
    # Regex to find chapter starts
    chapter_pattern = re.compile(r'^###\s+Chapter\s+(\d+[:.]?.*)$', re.MULTILINE)
    
    matches = list(chapter_pattern.finditer(content))
    
    chapters = []
    
    for i in range(len(matches)):
        start_index = matches[i].end()
        chapter_title = matches[i].group(1).strip()
        
        # Determine end index
        if i < len(matches) - 1:
            end_index = matches[i+1].start()
        else:
            end_index = len(content)
            
        chapter_content = content[start_index:end_index]
        word_count = count_words(chapter_content)
        
        chapters.append({
            'title': chapter_title,
            'word_count': word_count,
            'needs_expansion': word_count < 1000
        })
        
    return chapters

def main():
    books_dir = r"c:\Users\bryan\Documents\storymaker\Books"
    files = [f for f in os.listdir(books_dir) if f.startswith("Book") and f.endswith(".md")]
    files.sort()
    
    report = {}
    
    for file in files:
        filepath = os.path.join(books_dir, file)
        chapters = analyze_book(filepath)
        report[file] = chapters
        
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
