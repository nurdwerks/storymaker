import os

# Paths
BASE_DIR = r"c:\Users\bryan\Documents\storymaker"
BOOKS_DIR = os.path.join(BASE_DIR, "Books")
FULL_DIR = os.path.join(BASE_DIR, "Full")
TRACKER_FILE = os.path.join(FULL_DIR, "Progress_Tracker.md")
TARGET_WORD_COUNT = 5500

def get_word_count(file_path):
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content.split())
    except Exception:
        return 0

def main():
    if not os.path.exists(BOOKS_DIR):
        print(f"Books directory not found: {BOOKS_DIR}")
        return

    # Data structure to hold stats
    project_stats = {
        "total_chapters": 0,
        "completed_chapters": 0,
        "total_words": 0,
        "books": {}
    }

    # Collect Data
    # Walk through the SOURCE (Books) directory to know what chapters should exist
    # But look in the TARGET (Full) directory for the word counts
    books = [d for d in os.listdir(BOOKS_DIR) if os.path.isdir(os.path.join(BOOKS_DIR, d)) and d.startswith("Book ")]
    books.sort()

    table_rows = []

    for book in books:
        book_source_path = os.path.join(BOOKS_DIR, book)
        book_target_path = os.path.join(FULL_DIR, book)
        
        # Initialize book stats
        if book not in project_stats["books"]:
            project_stats["books"][book] = {"chapters": 0, "completed": 0, "words": 0}
            
        chapters = [f for f in os.listdir(book_source_path) if f.endswith(".md")]
        chapters.sort()
        
        for chapter in chapters:
            project_stats["total_chapters"] += 1
            project_stats["books"][book]["chapters"] += 1
            
            # Check target file in Full/
            target_chapter_path = os.path.join(book_target_path, chapter)
            word_count = get_word_count(target_chapter_path)
            
            project_stats["total_words"] += word_count
            project_stats["books"][book]["words"] += word_count
            
            status = "Pending"
            if word_count > 0:
                status = "In Progress"
            if word_count >= TARGET_WORD_COUNT:
                status = "Completed"
                project_stats["completed_chapters"] += 1
                project_stats["books"][book]["completed"] += 1
            
            # Add to table rows
            # Clean up chapter name for display (remove .md)
            chapter_name = chapter.replace(".md", "")
            table_rows.append(f"| {book} | {chapter_name} | {word_count} | {status} |")

    # Generate Markdown Content
    md_content = []
    
    # 1. Title & Overall Stats
    md_content.append("# Project Progress Tracker")
    md_content.append("")
    md_content.append("## **Project Overview**")
    progress_percentage = (project_stats["completed_chapters"] / project_stats["total_chapters"] * 100) if project_stats["total_chapters"] > 0 else 0
    md_content.append(f"- **Total Chapters**: {project_stats['total_chapters']}")
    md_content.append(f"- **Completed Chapters**: {project_stats['completed_chapters']} ({progress_percentage:.1f}%)")
    md_content.append(f"- **Total Word Count**: {project_stats['total_words']:,}")
    md_content.append("")
    
    # 2. Book Breakdown Table
    md_content.append("## **Book Breakdown**")
    md_content.append("| Book | Chapters | Completed | Total Words | Progress |")
    md_content.append("|---|---|---|---|---|")
    
    for book in books:
        stats = project_stats["books"][book]
        bk_progress = (stats["completed"] / stats["chapters"] * 100) if stats["chapters"] > 0 else 0
        md_content.append(f"| {book} | {stats['chapters']} | {stats['completed']} | {stats['words']:,} | {bk_progress:.1f}% |")
    
    md_content.append("")
    
    # 3. Detailed Chapter Table
    md_content.append("## **Detailed Chapter Status**")
    md_content.append("| Book Name | Chapter | Word Count | Status |")
    md_content.append("|---|---|---|---|")
    md_content.extend(table_rows)
    
    # Write to file
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    
    print(f"Successfully updated {TRACKER_FILE}")

if __name__ == "__main__":
    main()
