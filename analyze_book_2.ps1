# Analyze word counts for Book 2

$bookPath = "c:\Users\bryan\Documents\storymaker\Books\Book 2_ The Cipher of Sins (Original Terms).md"
$content = Get-Content $bookPath -Raw

# Split by chapter headers
$chapters = $content -split '(?=### Chapter \d+:)'

$results = @()
foreach ($chapter in $chapters) {
    if ($chapter -match '### Chapter (\d+): (.+)') {
        $chapterNum = $Matches[1]
        $chapterTitle = $Matches[2].Trim()
        $wordCount = ($chapter -split '\s+' | Where-Object { $_ }).Count
        $results += [PSCustomObject]@{
            title           = "$chapterNum`: $chapterTitle"
            needs_expansion = $wordCount -lt 1000
            word_count      = $wordCount
        }
    }
}

$results | ConvertTo-Json
