
import re

line = "- **Key Event:** **Lady Corinne** sits on a floral armchair, looking like a queen exiled to a dollhouse."
content = line.replace("- **Key Event:**", "").strip()
print(f"Content: '{content}'")

terms = ["Corinne", "Lady Corinne", "The Porcelain Doll"]
found = False
for term in terms:
    pattern = r'\b' + re.escape(term) + r'\b'
    if re.search(pattern, content, re.IGNORECASE):
        print(f"MATCH: '{term}' with pattern '{pattern}'")
        found = True

if not found:
    print("NO MATCH FOUND")
