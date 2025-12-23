param (
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)

$InputFile = Resolve-Path $InputFile
$Dir = Split-Path $InputFile -Parent
$Name = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
$OutputFile = Join-Path $Dir "$Name.md"
$TempPath = Join-Path $Env:TEMP ([System.Guid]::NewGuid().ToString())

Write-Host "Converting '$InputFile' to '$OutputFile'..."

try {
    # Create temp directory
    New-Item -ItemType Directory -Force -Path $TempPath | Out-Null

    # Copy and rename docx to zip
    $ZipFile = Join-Path $TempPath "content.zip"
    Copy-Item $InputFile $ZipFile

    # Unzip
    Expand-Archive -Path $ZipFile -DestinationPath $TempPath -Force

    # Read Document XML
    $XmlPath = Join-Path $TempPath "word\document.xml"
    if (-not (Test-Path $XmlPath)) {
        throw "Could not find word/document.xml in the docx file."
    }

    # Force UTF-8 when reading the XML content to avoid mojibake
    [xml]$xml = Get-Content $XmlPath -Encoding UTF8

    # Setup Namespace Manager
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

    # Extract Paragraphs
    $paragraphs = $xml.SelectNodes("//w:p", $ns)
    
    $mdLines = @()

    foreach ($p in $paragraphs) {
        $pText = ""
        
        # --- 1. Determine Paragraph Style (Header / List) ---
        $prefix = ""
        
        # Check for Headers (Heading1, Heading2...)
        $style = $p.SelectSingleNode("w:pPr/w:pStyle", $ns)
        if ($style) {
            $val = $style.Attributes["w:val"].Value
            if ($val -match "Heading(\d)") {
                $level = $matches[1]
                $prefix = "#" * [int]$level + " "
            }
        }

        # Check for Lists (Numbering)
        $num = $p.SelectSingleNode("w:pPr/w:numPr", $ns)
        if ($num) {
            # Indentation level
            $ilvlNode = $num.SelectSingleNode("w:ilvl", $ns)
            $ilvl = if ($ilvlNode) { [int]$ilvlNode.Attributes["w:val"].Value } else { 0 }
            
            # Markdown list indentation (2 spaces per level)
            $indent = "  " * $ilvl
            $prefix = "$indent- " # Using unordered list for simplicity as mapping numbers is complex
        }

        # --- 2. Process Runs (Bold / Italic) ---
        # We need to track state to handle adjacent runs correctly
        $isBold = $false
        $isItalic = $false
        
        $runs = $p.SelectNodes("w:r", $ns)
        
        foreach ($r in $runs) {
            # Run Properties
            $rPr = $r.SelectSingleNode("w:rPr", $ns)
            
            # Check Bold
            $rBold = $false
            if ($rPr -and $rPr.SelectSingleNode("w:b", $ns)) {
                # w:b can be present without value (true), or w:val="0" (false)
                $val = $rPr.SelectSingleNode("w:b", $ns).Attributes["w:val"]
                if (-not $val -or $val.Value -ne "0") { $rBold = $true }
            }

            # Check Italic
            $rItalic = $false
            if ($rPr -and $rPr.SelectSingleNode("w:i", $ns)) {
                $val = $rPr.SelectSingleNode("w:i", $ns).Attributes["w:val"]
                if (-not $val -or $val.Value -ne "0") { $rItalic = $true }
            }

            # Get Text
            $tNode = $r.SelectSingleNode("w:t", $ns)
            if (-not $tNode) { continue }
            $text = $tNode.InnerText

            # Skip empty runs if they don't change formatting significantly, 
            # but sometimes they hold spaces.
            if ([string]::IsNullOrEmpty($text)) { continue }

            # --- State Transitions ---
            
            # Close Bold if ending
            if ($isBold -and -not $rBold) { $pText += "**"; $isBold = $false }
            # Close Italic if ending
            if ($isItalic -and -not $rItalic) { $pText += "*"; $isItalic = $false }
            
            # Open Italic if starting
            if ($rItalic -and -not $isItalic) { $pText += "*"; $isItalic = $true }
            # Open Bold if starting
            if ($rBold -and -not $isBold) { $pText += "**"; $isBold = $true }
            
            $pText += $text
        }

        # Close any lingering tags at end of paragraph
        if ($isItalic) { $pText += "*" }
        if ($isBold) { $pText += "**" }

        # Assemble Line
        if (-not [string]::IsNullOrWhiteSpace($pText)) {
            $mdLines += "$prefix$pText"
            # Add blank line after blocks for standard MD spacing
            $mdLines += "" 
        }
    }

    # Save to Markdown file
    $mdLines | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "Conversion complete: $OutputFile"

}
catch {
    Write-Error "An error occurred: $_"
}
finally {
    # Cleanup
    if (Test-Path $TempPath) {
        Remove-Item -Path $TempPath -Recurse -Force
    }
}
