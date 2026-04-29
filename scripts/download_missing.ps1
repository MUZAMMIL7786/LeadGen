$base = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/'

# Twilio alternative
try { Invoke-WebRequest -Uri ($base+'twilio.svg') -OutFile 'twilio.svg' -UseBasicParsing; Write-Host 'OK: twilio' }
catch {
    # Try with full brand name
    try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/twilio.svg' -OutFile 'twilio.svg' -UseBasicParsing; Write-Host 'OK: twilio master' }
    catch { Write-Host "FAIL twilio: $($_.Exception.Message)" }
}

# ActiveCampaign - try different casing
try { Invoke-WebRequest -Uri ($base+'activecampaign.svg') -OutFile 'activecampaign.svg' -UseBasicParsing; Write-Host 'OK: activecampaign' }
catch {
    # Inline SVG fallback for ActiveCampaign
    Set-Content 'activecampaign.svg' '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#356AE6"><path d="M0 12.028c0-6.628 5.373-12 12-12 6.628 0 12 5.372 12 12 0 6.627-5.372 12-12 12-6.627 0-12-5.373-12-12zm11.32 4.662l5.783-9.324H5.01l1.787 2.88h5.197l-2.91 4.69 2.236 1.754z"/></svg>'
    Write-Host 'OK: activecampaign (fallback)'
}

# Pipedrive
try { Invoke-WebRequest -Uri ($base+'pipedrive.svg') -OutFile 'pipedrive.svg' -UseBasicParsing; Write-Host 'OK: pipedrive' }
catch {
    Set-Content 'pipedrive.svg' '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#017737"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 5.143c2.838 0 4.571 1.838 4.571 4.571 0 2.572-1.733 4.572-4.285 4.572-.429 0-.858-.072-1.215-.215v4.786H8.5V5.5c1.071-.215 2.214-.357 3.5-.357zm-.286 2.071c-.357 0-.786.072-1.143.143v4.858c.357.143.714.215 1.072.215 1.5 0 2.285-1.072 2.285-2.643 0-1.5-.785-2.573-2.214-2.573z"/></svg>'
    Write-Host 'OK: pipedrive (fallback)'
}

# Also download a couple more useful ones
@('googleanalytics','googlemeet','microsoftoutlook') | ForEach-Object {
    $n = $_
    try { 
        Invoke-WebRequest -Uri ($base+$n+'.svg') -OutFile ($n+'.svg') -UseBasicParsing
        Write-Host "OK: $n"
    }
    catch { Write-Host "FAIL: $n" }
}

Write-Host "Done."
