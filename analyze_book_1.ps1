$file = "c:\Users\bryan\Documents\storymaker\Books\Book 1_ The Iron Selection (Original Terms).md"
$content = Get-Content -Path $file -Raw
    
# regex to find chapters: ### Chapter <number>: <title>
$foundChapters = [regex]::Matches($content, '(?m)^###\s+Chapter\s+(.*)$')

$chapters = @()

for ($i = 0; $i -lt $foundChapters.Count; $i++) {
    $match = $foundChapters[$i]
    $title = $match.Groups[1].Value.Trim()
    $startIndex = $match.Index + $match.Length
    
    if ($i -lt $foundChapters.Count - 1) {
        $endIndex = $foundChapters[$i + 1].Index
    }
    else {
        $endIndex = $content.Length
    }
    
    $chapterContent = $content.Substring($startIndex, $endIndex - $startIndex)
    
    # Simple word count
    $wordCount = ($chapterContent -split '\s+').Count
    
    $chapters += @{
        title           = $title
        word_count      = $wordCount
        needs_expansion = $wordCount -lt 1000
    }
}

$chapters | ConvertTo-Json -Depth 5
