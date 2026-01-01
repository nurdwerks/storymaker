import os
import re
import json

def extract_consistency_tables(characters_dir):
    consistency_data = {}
    
    # Regex to find the Consistency Check header
    header_pattern = re.compile(r'## Consistency Check')
    # Regex to capture table rows (starting with |)
    table_row_pattern = re.compile(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|')
    
    for filename in os.listdir(characters_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(characters_dir, filename)
        character_name = filename.replace("Character Profile_", "").replace(".md", "").strip()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        capture_mode = False
        events = []
        
        for line in lines:
            if header_pattern.search(line):
                capture_mode = True
                continue
            
            if capture_mode:
                # Stop if we hit the next header
                if line.startswith("## ") and "Consistency Check" not in line:
                    break
                
                # Check for table row
                if line.strip().startswith("|") and not line.strip().startswith("|---"):
                    match = table_row_pattern.search(line)
                    if match:
                        cols = [c.strip() for c in match.groups()]
                        # Skip header row if caught (checked by contents usually, or skip first if needed)
                        if cols[0].lower() == "book": 
                            continue
                            
                        events.append({
                            "Book": cols[0],
                            "Chapter": cols[1],
                            "Type": cols[2],
                            "Description": cols[3]
                        })
        
        if events:
            consistency_data[character_name] = events

    return consistency_data

if __name__ == "__main__":
    characters_dir = "c:\\Users\\bryan\\Documents\\storymaker\\Characters"
    data = extract_consistency_tables(characters_dir)
    
    # Sort characters alphabetically
    sorted_chars = sorted(data.keys())
    
    output_path = "consistency_summary.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Extracted consistency data for {len(data)} characters to {output_path}")
