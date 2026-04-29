$base = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/'
$icons = @('zapier','notion','stripe','whatsapp','twilio','zendesk','calendly','mailchimp','activecampaign','intercom','pipedrive','airtable','make')

foreach ($name in $icons) {
    $url = $base + $name + '.svg'
    $out = $name + '.svg'
    try {
        Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing
        Write-Host "OK: $out"
    }
    catch {
        Write-Host "FAIL: $out - $($_.Exception.Message)"
    }
}
Write-Host "Done."
