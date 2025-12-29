import os
import re

def get_character_profiles(characters_dir):
    """
    Scans the characters directory and returns a dictionary of:
    { "Character Name": { "path": "full/path", "short_names": ["Name"] } }
    """
    profiles = {}
    for filename in os.listdir(characters_dir):
        if filename.endswith(".md"):
            path = os.path.join(characters_dir, filename)
            
            # Simple heuristic for name: Filename without "Character Profile_ " and extension
            # But the content might be better. Let's rely on filenames for keys but refine search terms.
            
            # Example: "Character Profile_ Angelica Ward.md" -> "Angelica Ward"
            name_part = filename.replace("Character Profile_ ", "").replace(".md", "")
            
            # Clean up modifiers like "(The Time-Eater)" for the primary key, but keep them for search?
            # Actually, "Angelica Ward" is a good search term. "Angelica" is also good.
            # "Prelate Vane" -> "Vane"
            
            # Let's derive search terms.
            search_terms = [name_part] # Full name from filename
            
            # Remove parentheses content for a cleaner name to search
            clean_name = re.sub(r'\s*\(.*?\)', '', name_part).strip()
            if clean_name != name_part:
                search_terms.append(clean_name)
                
            # Add all parts as potential search terms (filtered later)
            parts = clean_name.split()
            search_terms.extend(parts)
            
            # Special cases? "The Entity" -> "Entity"?
            # (handled by splitting and filtering "The")

            # Deduplicate and filter short terms that might be too common (like "The")
            STOP_WORDS = {
                "the", "dr", "mr", "mrs", "ms", "lady", "lord", "sir", "madame", "master", 
                "sister", "brother", "father", "mother", "uncle", "aunt", 
                "captain", "lieutenant", "general", "major", "private", "sergeant", "corporal", 
                "chief", "officer", "agent", "detective", "inspector", "professor", "doctor",
                "little", "old", "big", "young"
            }
            
            final_terms = set()
            for term in search_terms:
                term_clean = term.lower().replace(".", "")
                if len(term) > 2 and term_clean not in STOP_WORDS:
                    final_terms.add(term)
            
            profiles[name_part] = {
                "path": path,
                "search_terms": list(final_terms),
                "events": []
            }
    return profiles

def scan_chapters(books_dir, profiles):
    """
    Iterates through all books and chapters, finding events for each character.
    """
    # Sort books to keep order
    books = sorted([b for b in os.listdir(books_dir) if b.startswith("Book ")])
    
    for book in books:
        book_path = os.path.join(books_dir, book)
        if not os.path.isdir(book_path):
            continue
            
        # Get book name "Book X"
        book_name = book.split(" - ")[0]
        
        # Robustly handle different naming conventions for chapters if necessary
        # But mostly rely on os.listdir
        
        chapters = sorted([c for c in os.listdir(book_path) if c.startswith("Chapter") and c.endswith(".md")])
        
        for chapter in chapters:
            chapter_path = os.path.join(book_path, chapter)
            
            # Get chapter number "Chapter XX"
            chapter_num_match = re.search(r'Chapter[ _](\d+)', chapter)
            chapter_num = f"Chapter {chapter_num_match.group(1)}" if chapter_num_match else "Chapter ??"
            
            try:
                content_str = read_file_robust(chapter_path)
                lines = content_str.splitlines()
            except Exception as e:
                print(f"Skipping {chapter}: {e}")
                continue
                
            for line in lines:
                line = line.strip()
                event_type = None
                content = None
                
                if line.startswith("- **Key Event:**"):
                    event_type = "Key Event"
                    content = line.replace("- **Key Event:**", "").strip()
                elif line.startswith("- _Character Defining Moment:_"):
                    event_type = "Moment"
                    content = line.replace("- _Character Defining Moment:_ ", "").strip()
                
                if event_type and content:
                    # Check which characters are mentioned in this content
                    for char_name, profile_data in profiles.items():
                        found = False
                        for term in profile_data['search_terms']:
                            # Case insensitive search
                            if re.search(r'\b' + re.escape(term) + r'\b', content, re.IGNORECASE):
                                found = True
                                break
                        
                        if found:
                            profile_data['events'].append({
                                "book": book_name,
                                "chapter": chapter_num,
                                "type": event_type,
                                "content": content
                            })

def read_file_robust(path):
    encodings = ['utf-8', 'cp1252', 'latin-1']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Could not decode {path} with any supported encoding.")

def update_profiles(profiles):
    """
    Writes the consistency check table to the character profile files.
    """
    for char_name, data in profiles.items():
        if not data['events']:
            continue
            
        path = data['path']
        print(f"Updating {char_name}...")
        
        # Build the new section
        new_section = ["\n## Consistency Check\n\n"]
        new_section.append("| Book | Chapter | Type | Event Description |\n")
        new_section.append("|---|---|---|---|\n")
        
        for event in data['events']:
            # Escape pipes in content to avoid breaking table
            safe_content = event['content'].replace("|", r"\|")
            new_section.append(f"| {event['book']} | {event['chapter']} | {event['type']} | {safe_content} |\n")
        
        try:
            content = read_file_robust(path)
        except Exception as e:
            print(f"Error reading {path}: {e}")
            continue
            
        # Remove existing Consistency Check section if present
        if "## Consistency Check" in content:
            # truncate content before this section
            content = content.split("## Consistency Check")[0].strip()
            
        # Append new section
        final_content = content + "\n" + "".join(new_section)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(final_content)
        except Exception as e:
            print(f"Error writing {path}: {e}")

def main():
    base_dir = r"c:\Users\bryan\Documents\storymaker"
    chars_dir = os.path.join(base_dir, "Characters")
    books_dir = os.path.join(base_dir, "Books")
    
    print("Scanning Profiles...")
    profiles = get_character_profiles(chars_dir)
    
    print("Scanning Chapters...")
    scan_chapters(books_dir, profiles)
    
    print("Updating Profiles...")
    update_profiles(profiles)
    
    print("Done!")

if __name__ == "__main__":
    main()
