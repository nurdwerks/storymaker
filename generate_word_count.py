import os
import urllib.parse

def count_words_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple word count: split by whitespace
            words = content.split()
            return len(words)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

def generate_report(base_dir):
    books_dir = os.path.join(base_dir, "Books")
    report_lines = []
    report_lines.append("# Chapter Word Count Report")
    report_lines.append("")
    report_lines.append("| Book | Chapter | Word Count | Status |")
    report_lines.append("|---|---|---|---|")

    total_words = 0
    
    # Walk through the Books directory
    if not os.path.exists(books_dir):
        print(f"Books directory not found: {books_dir}")
        return

    # sort books to ensure order
    book_folders = sorted([d for d in os.listdir(books_dir) if os.path.isdir(os.path.join(books_dir, d))])

    all_chapters = []

    for book_folder in book_folders:
        book_path = os.path.join(books_dir, book_folder)
        chapter_files = sorted([f for f in os.listdir(book_path) if f.endswith(".md")])
        
        for chapter_file in chapter_files:
             file_path = os.path.join(book_path, chapter_file)
             count = count_words_in_file(file_path)
             total_words += count
             
             # Status check (arbitrary threshold of 100 words for empty files)
             status = "Pass" if count > 100 else "Incomplete"
             
             all_chapters.append({
                 "book": book_folder,
                 "chapter": chapter_file,
                 "count": count,
                 "status": status
             })

    # Sort chapters by word count (shortest to longest)
    all_chapters.sort(key=lambda x: x['count'])

    for ch in all_chapters:
        # Create relative path for the link
        rel_path = f"Books/{ch['book']}/{ch['chapter']}"
        # Encode path to handle spaces
        encoded_path = urllib.parse.quote(rel_path)
        link = f"[{ch['chapter']}]({encoded_path})"
        report_lines.append(f"| {ch['book']} | {link} | {ch['count']} | {ch['status']} |")

    report_lines.append("")
    report_lines.append(f"**Total Word Count:** {total_words}")

    output_file = os.path.join(base_dir, "ChapterWordCount.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    
    print(f"Report generated at: {output_file}")

if __name__ == "__main__":
    # Base directory is where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    generate_report(base_dir)
