import re
import sys

def count_words(text):
    return len(text.split())

def analyze_chapters(filepath, specific_chapters=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find chapter starts (### Chapter X)
    chapter_pattern = re.compile(r'^###\s+Chapter\s+(\d+[:.]?.*)$', re.MULTILINE)

    matches = list(chapter_pattern.finditer(content))

    results = []

    for i in range(len(matches)):
        start_index = matches[i].end()
        chapter_title = matches[i].group(1).strip()

        # Check if we only want specific chapters (by number or partial title)
        chapter_num_match = re.match(r'^(\d+)', chapter_title)
        chapter_num = int(chapter_num_match.group(1)) if chapter_num_match else -1

        if specific_chapters and chapter_num not in specific_chapters:
            continue

        # Determine end index
        if i < len(matches) - 1:
            end_index = matches[i+1].start()
        else:
            end_index = len(content)

        chapter_content = content[start_index:end_index]
        word_count = count_words(chapter_content)

        results.append({
            'title': chapter_title,
            'word_count': word_count,
            'status': 'PASS' if word_count >= 1000 else 'FAIL'
        })

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python count_chapters.py <filepath> [chapter_numbers...]")
        sys.exit(1)

    filepath = sys.argv[1]
    chapters = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None

    data = analyze_chapters(filepath, chapters)

    for ch in data:
        print(f"{ch['title']}: {ch['word_count']} words [{ch['status']}]")
