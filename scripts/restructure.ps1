# Create professional folder structure
$root = "d:\github\LeadGen"

# Create folders
$folders = @(
    "assets\icons\integrations",
    "assets\images",
    "assets\fonts",
    "scripts"
)
foreach ($f in $folders) {
    New-Item -ItemType Directory -Path "$root\$f" -Force | Out-Null
    Write-Host "Created: $f"
}

# Move all integration SVG icons
$svgIcons = @(
    "activecampaign.svg","airtable.svg","calendly.svg","googleanalytics.svg",
    "googlecalendar.svg","googlemeet.svg","hubspot.svg","intercom.svg",
    "mailchimp.svg","make.svg","microsoftteams.svg","notion.svg",
    "outlook.svg","pipedrive.svg","salesforce.svg","slack.svg",
    "stripe.svg","twilio.svg","whatsapp.svg","zapier.svg","zendesk.svg"
)
foreach ($svg in $svgIcons) {
    $src = "$root\$svg"
    if (Test-Path $src) {
        Move-Item $src "$root\assets\icons\integrations\$svg" -Force
        Write-Host "Moved icon: $svg"
    }
}

# Move founder image
if (Test-Path "$root\founder.png") {
    Move-Item "$root\founder.png" "$root\assets\images\founder.png" -Force
    Write-Host "Moved: founder.png"
}

# Move scripts
foreach ($script in @("download_svgs.ps1","download_missing.ps1")) {
    if (Test-Path "$root\$script") {
        Move-Item "$root\$script" "$root\scripts\$script" -Force
        Write-Host "Moved script: $script"
    }
}

Write-Host "`nDone. New structure:"
Get-ChildItem $root -Recurse -Exclude ".git" | Where-Object { $_.FullName -notlike "*\.git*" } | ForEach-Object {
    $rel = $_.FullName.Replace($root + "\", "")
    $prefix = if ($_.PSIsContainer) { "[DIR] " } else { "[FILE]" }
    Write-Host "  $prefix $rel"
}
