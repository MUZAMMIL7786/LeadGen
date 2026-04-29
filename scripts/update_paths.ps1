# Update all asset paths in index.html to match the new folder structure
$file = 'd:\github\LeadGen\index.html'
$content = Get-Content $file -Raw -Encoding UTF8

# Update founder image path
$content = $content -replace '"founder\.png"', '"assets/images/founder.png"'

# Update all integration SVG icon paths
$icons = @(
    'activecampaign','airtable','calendly','googleanalytics','googlecalendar',
    'googlemeet','hubspot','intercom','mailchimp','make','microsoftteams',
    'notion','outlook','pipedrive','salesforce','slack','stripe','twilio',
    'whatsapp','zapier','zendesk'
)
foreach ($icon in $icons) {
    $content = $content -replace ('"' + $icon + '\.svg"'), ('"assets/icons/integrations/' + $icon + '.svg"')
}

Set-Content $file $content -Encoding UTF8
Write-Host "All paths updated successfully."

# Verify a few key replacements
$sample = (Select-String -Path $file -Pattern 'assets/icons/integrations' | Measure-Object).Count
Write-Host "Found $sample references to assets/icons/integrations in index.html"
$img = (Select-String -Path $file -Pattern 'assets/images/founder' | Measure-Object).Count
Write-Host "Found $img references to assets/images/founder.png in index.html"
