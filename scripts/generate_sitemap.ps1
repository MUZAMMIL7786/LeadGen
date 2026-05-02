param (
    [string]$BaseUrl = "https://www.wakilz.com"
)

# Go to the root of the LeadGen directory (parent of the scripts folder)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

# Get all HTML files in the root directory, excluding any that contain "-old"
$HtmlFiles = Get-ChildItem -Path $RootDir -Filter "*.html" | Where-Object { $_.Name -notmatch "-old" }

$Xml = "<?xml version=`"1.0`" encoding=`"UTF-8`"?>`n"
$Xml += "<urlset xmlns=`"http://www.sitemaps.org/schemas/sitemap/0.9`">`n"

foreach ($File in $HtmlFiles) {
    # If the file is index.html, map it to the root path
    $UrlPath = if ($File.Name -eq "index.html") { "/" } else { "/$($File.Name)" }
    
    # Format the last modified date in W3C Datetime format (ISO 8601)
    $LastMod = $File.LastWriteTime.ToString("yyyy-MM-ddTHH:mm:sszzz")
    
    $Xml += "  <url>`n"
    $Xml += "    <loc>$BaseUrl$UrlPath</loc>`n"
    $Xml += "    <lastmod>$LastMod</lastmod>`n"
    $Xml += "  </url>`n"
}

$Xml += "</urlset>"

$SitemapPath = Join-Path -Path $RootDir -ChildPath "sitemap.xml"

# Write the file with UTF-8 encoding (no BOM)
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllText($SitemapPath, $Xml, $Utf8NoBomEncoding)

Write-Host "Successfully generated sitemap.xml at $SitemapPath" -ForegroundColor Green
Write-Host "Included $($HtmlFiles.Count) HTML files." -ForegroundColor Cyan
