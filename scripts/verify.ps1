Write-Host "=== FINAL REPO STRUCTURE ===" -ForegroundColor Cyan
Get-ChildItem "d:\github\LeadGen" -Recurse | Where-Object { $_.FullName -notlike "*\.git\*" } | Sort-Object FullName | ForEach-Object {
    $rel = $_.FullName.Replace("d:\github\LeadGen\", "")
    $depth = ($rel.Split("\").Count - 1)
    $indent = "    " * $depth
    $icon = if ($_.PSIsContainer) { "[DIR] " } else { "     " }
    Write-Host ($indent + $icon + $_.Name)
}

Write-Host ""
Write-Host "=== PATH VALIDATION ===" -ForegroundColor Cyan

$iconCount = (Select-String -Path "d:\github\LeadGen\index.html" -Pattern "assets/icons/integrations" | Measure-Object).Count
Write-Host "Integration icon references in HTML: $iconCount"

$rootSvgs = Get-ChildItem "d:\github\LeadGen\*.svg" -ErrorAction SilentlyContinue
if ($rootSvgs) {
    Write-Host "WARNING: Bare SVGs still in root!" -ForegroundColor Yellow
    $rootSvgs | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Yellow }
} else {
    Write-Host "Root clean — no loose SVGs in root" -ForegroundColor Green
}

$icons = @('hubspot','slack','microsoftteams','salesforce','googlecalendar','zapier',
           'notion','stripe','whatsapp','twilio','zendesk','calendly','mailchimp',
           'activecampaign','intercom','pipedrive','airtable','make')
$missing = 0
foreach ($icon in $icons) {
    $path = "d:\github\LeadGen\assets\icons\integrations\$icon.svg"
    if (-not (Test-Path $path)) {
        Write-Host "MISSING: $icon.svg" -ForegroundColor Red
        $missing++
    }
}
if ($missing -eq 0) {
    Write-Host "All 18 integration SVGs present: OK" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Cyan
