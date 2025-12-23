
$booksDir = "c:\Users\bryan\Documents\storymaker\Books"
Write-Host "Checking directory: $booksDir"
if (Test-Path $booksDir) {
    Write-Host "Directory exists."
}
else {
    Write-Host "Directory NOT found."
}

$files = Get-ChildItem -Path $booksDir -Filter "Book*.md" | Sort-Object Name
Write-Host "Found $($files.Count) files."

$report = [ordered]@{}

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content -Path $file.FullName -Raw
    
    # regex to find chapters: ### Chapter <number>: <title>
    $matches = [regex]::Matches($content, '(?m)^###\s+Chapter\s+(.*)$')
    Write-Host "  Found $($matches.Count) chapters."
    
    $chapters = @()
    
    for ($i = 0; $i -lt $matches.Count; $i++) {
        $match = $matches[$i]
        $title = $match.Groups[1].Value.Trim()
        $startIndex = $match.Index + $match.Length
        
        if ($i -lt $matches.Count - 1) {
            $endIndex = $matches[$i + 1].Index
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
    
    $report[$file.Name] = $chapters
}

$json = $report | ConvertTo-Json -Depth 5
Write-Host "JSON Output Start:"
Write-Output $json
Write-Host "JSON Output End"
