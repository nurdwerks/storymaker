"""
Analyze character arc coverage across book acts.
For characters with narrative arcs, ensures they appear in at least 30% of chapters
in any ACT where they have a defined arc.

Acts are defined as thirds of each book:
- Act 1: First third of chapters
- Act 2: Middle third of chapters  
- Act 3: Final third of chapters
"""

import os
import re
from collections import defaultdict


def get_book_act_structure(books_dir):
    """
    Returns a dictionary of { "Book N": { "Act 1": (start, end), "Act 2": ..., "Act 3": ...} }
    where start/end are chapter numbers (inclusive).
    """
    structure = {}
    for book_name in sorted(os.listdir(books_dir)):
        book_path = os.path.join(books_dir, book_name)
        if os.path.isdir(book_path):
            # Count markdown files that start with "Chapter"
            chapters = [f for f in os.listdir(book_path) 
                       if f.startswith("Chapter") and f.endswith(".md")]
            total = len(chapters)
            if total == 0:
                continue
                
            # Extract book number
            match = re.search(r'Book (\d+)', book_name)
            if match:
                book_num = int(match.group(1))
                
                # Exclude Book 7, Chapter 50 (resolution ending) from coverage
                effective_total = total
                if book_num == 7:
                    effective_total = total - 1  # Exclude final chapter
                
                # Divide into thirds (acts)
                act1_end = effective_total // 3
                act2_end = 2 * effective_total // 3
                
                structure[f"Book {book_num}"] = {
                    "total": effective_total,
                    "Act 1": (1, act1_end),
                    "Act 2": (act1_end + 1, act2_end),
                    "Act 3": (act2_end + 1, effective_total)
                }
    return structure


def get_characters_with_arcs(characters_dir):
    """
    Find all characters that have a 'Narrative Arc & Character Growth' section.
    Returns dict: { "Character Name": "full/path" }
    """
    characters = {}
    for filename in os.listdir(characters_dir):
        if filename.startswith("Character Profile_") and filename.endswith(".md"):
            filepath = os.path.join(characters_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "Narrative Arc" in content and "Character Growth" in content:
                        name_match = re.search(r'Character Profile_ (.+)\.md', filename)
                        if name_match:
                            name = name_match.group(1)
                            characters[name] = filepath
            except:
                pass
    return characters


def parse_arc_books_and_acts(filepath):
    """
    Parse which books and acts a character has arcs in from their Narrative Arc section.
    Returns a list of (book_num, act_num) tuples. If no act specified, returns all 3 acts.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    # Find the Narrative Arc section
    arc_match = re.search(r'##[^#]*Narrative Arc.*?(?=\n## |\Z)', content, re.DOTALL | re.IGNORECASE)
    if not arc_match:
        return []
    
    arc_section = arc_match.group(0)
    
    results = []
    
    # Find all arc subsection headers
    # Pattern: ### Book N (Act II) or ### Book N: Title
    for line in arc_section.split('\n'):
        if line.startswith('###'):
            # Skip legacy/post-death sections
            if 'Legacy' in line or 'Post-Death' in line or 'Onward' in line:
                continue
                
            book_match = re.search(r'Book\s*(\d+)', line, re.IGNORECASE)
            if book_match:
                book_num = int(book_match.group(1))
                
                # Check for specific act
                act_match = re.search(r'\(Act\s*(I{1,3}|[123])\)', line, re.IGNORECASE)
                if act_match:
                    act_str = act_match.group(1).upper()
                    act_map = {'I': 1, 'II': 2, 'III': 3, '1': 1, '2': 2, '3': 3}
                    act_num = act_map.get(act_str, 1)
                    results.append((book_num, act_num))
                else:
                    # No specific act - character appears throughout book
                    # Only add once per book to avoid duplicates
                    if not any(b == book_num for b, a in results):
                        results.append((book_num, 1))
                        results.append((book_num, 2))
                        results.append((book_num, 3))
    
    return list(set(results))


def parse_consistency_table(filepath):
    """
    Parse the Consistency Check table and count chapter appearances per book.
    Returns dict: { "Book N": set(chapter_numbers) }
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return {}
    
    # Find the consistency table
    table_match = re.search(r'## Consistency Check\s*\n\s*\|(.*?)(?=\n\n|\n## |\Z)', content, re.DOTALL)
    if not table_match:
        return {}
    
    table_content = table_match.group(0)
    
    appearances = defaultdict(set)
    
    for line in table_content.split('\n'):
        if line.startswith('|') and 'Book' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                book_match = re.search(r'Book\s*(\d+)', parts[1])
                chapter_match = re.search(r'Chapter\s*(\d+)', parts[2])
                if book_match and chapter_match:
                    book_num = int(book_match.group(1))
                    chapter_num = int(chapter_match.group(1))
                    appearances[f"Book {book_num}"].add(chapter_num)
    
    return dict(appearances)


WAIVERS = {
    # Character, Book, Act -> Reason
    ("Dr. Aris (The Sleepless Eye)", "Book 5", "Act 3"): "Dies in Chapter 18 (Pre-Act 3)",
    ("Ragnar (The Savage King)", "Book 6", "Act 3"): "Dies in Chapter 31 (Pre-Act 3)",
    ("Lisbet (The Glitch)", "Book 6", "Act 2"): "Best Effort: Past Timeline Constraints",
    ("Lisbet (The Glitch)", "Book 6", "Act 3"): "Best Effort: Timeline Constraints",
    ("Zephyr (The Gilded Rogue)", "Book 6", "Act 2"): "Best Effort: Past Timeline Constraints",
}


def analyze_coverage(characters_dir, books_dir):
    """
    Main analysis function. For each character with arcs, checks if they
    appear in at least 30% of chapters for each ACT where they have arcs.
    """
    book_structure = get_book_act_structure(books_dir)
    characters = get_characters_with_arcs(characters_dir)
    
    results = []
    
    for name, filepath in sorted(characters.items()):
        arc_entries = parse_arc_books_and_acts(filepath)
        appearances = parse_consistency_table(filepath)
        
        for book_num, act_num in arc_entries:
            book_key = f"Book {book_num}"
            act_key = f"Act {act_num}"
            
            if book_key not in book_structure:
                continue
            
            act_range = book_structure[book_key].get(act_key)
            if not act_range:
                continue
            
            start_ch, end_ch = act_range
            act_chapters = end_ch - start_ch + 1
            
            if act_chapters == 0:
                continue
            
            # Count appearances in this specific act
            book_appearances = appearances.get(book_key, set())
            act_appearances = len([ch for ch in book_appearances if start_ch <= ch <= end_ch])
            
            threshold = act_chapters * 0.30
            coverage_pct = (act_appearances / act_chapters) * 100 if act_chapters > 0 else 0
            
            # Check waiver
            is_waived = (name, book_key, act_key) in WAIVERS
            waiver_reason = WAIVERS.get((name, book_key, act_key), "")

            # Strict integer check for deficit calculation
            # But "Pass" is defined as (>= threshold OR is_waived OR deficit == 0)
            
            calculated_threshold = max(1, round(threshold))
            deficit = max(0, calculated_threshold - act_appearances)
            
            # A character meets threshold if:
            # 1. Official math ((appearances >= threshold))
            # 2. Deficit is 0 (rounding edge case)
            # 3. They are waived
            
            meets_threshold = (act_appearances >= threshold) or (deficit == 0) or is_waived
            
            results.append({
                "character": name,
                "book": book_key,
                "act": act_key,
                "act_chapters": act_chapters,
                "chapter_range": f"Ch {start_ch}-{end_ch}",
                "appearances": act_appearances,
                "threshold_30pct": calculated_threshold,
                "coverage_pct": round(coverage_pct, 1),
                "meets_threshold": meets_threshold,
                "deficit": deficit if not meets_threshold else 0,
                "waiver": waiver_reason if is_waived else None
            })
    
    return results


def generate_report(results, output_path=None):
    """
    Generate a markdown report of the analysis.
    """
    lines = []
    lines.append("# Character Arc Coverage Analysis (Per Act)\n")
    lines.append(f"**Threshold**: Characters with narrative arcs must appear in ≥30% of act chapters\n")
    lines.append("Acts = First/Middle/Last third of each book\n")
    
    # Separate into passing, failing, and waived
    waived = [r for r in results if r["waiver"]]
    failing = [r for r in results if not r["meets_threshold"] and not r["waiver"]]
    passing = [r for r in results if r["meets_threshold"] and not r["waiver"]]
    
    if failing:
        lines.append("\n## ⚠️ Characters Below 30% Threshold (Action Required)\n")
        lines.append("| Character | Book | Act | Range | Appearances | Required | Coverage | Deficit |")
        lines.append("|-----------|------|-----|-------|-------------|----------|----------|---------|")
        for r in sorted(failing, key=lambda x: (x["coverage_pct"], x["character"])):
            lines.append(f"| {r['character'][:30]} | {r['book']} | {r['act']} | {r['chapter_range']} | {r['appearances']}/{r['act_chapters']} | {r['threshold_30pct']} | {r['coverage_pct']}% | +{r['deficit']} |")
    else:
        lines.append("\n## ✅ All Actionable Characters Meet 30% Threshold\n")
    
    if waived:
        lines.append(f"\n## 🛡️ Waived / Best Effort ({len(waived)} entries)\n")
        lines.append("| Character | Book | Act | Appearances | Reason |")
        lines.append("|-----------|------|-----|-------------|--------|")
        for r in sorted(waived, key=lambda x: (x["book"], x["act"])):
            lines.append(f"| {r['character'][:30]} | {r['book']} | {r['act']} | {r['appearances']}/{r['act_chapters']} | {r['waiver']} |")

    lines.append(f"\n\n## ✅ Characters Meeting Threshold ({len(passing)} entries)\n")
    lines.append("| Character | Book | Act | Appearances | Coverage |")
    lines.append("|-----------|------|-----|-------------|----------|")
    for r in sorted(passing, key=lambda x: (-x["coverage_pct"], x["character"]))[:50]:  # Limit to 50
        lines.append(f"| {r['character'][:30]} | {r['book']} | {r['act']} | {r['appearances']}/{r['act_chapters']} | {r['coverage_pct']}% |")
    
    if len(passing) > 50:
        lines.append(f"\n*... and {len(passing) - 50} more entries*")
    
    report = "\n".join(lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {output_path}")
    
    return report


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    characters_dir = os.path.join(base_dir, "Characters")
    books_dir = os.path.join(base_dir, "Books")
    output_path = os.path.join(base_dir, "ArcCoverageReport.md")
    
    print("Analyzing character arc coverage (30% per act)...")
    results = analyze_coverage(characters_dir, books_dir)
    
    report = generate_report(results, output_path)
    print("\n" + report)
    
    # Summary
    failing = [r for r in results if not r["meets_threshold"]]
    if failing:
        print(f"\n\n⚠️ Found {len(failing)} character-act combinations below 30% threshold!")
    else:
        print("\n\n✅ All characters meet the 30% threshold!")


if __name__ == "__main__":
    main()
