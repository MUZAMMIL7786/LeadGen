Add-Type -AssemblyName System.Drawing

$sourcePath = "d:\github\LeadGen\favicon.png"
$destPath192 = "d:\github\LeadGen\favicon-192x192.png"
$destPath32 = "d:\github\LeadGen\favicon-32x32.png"

if (Test-Path $sourcePath) {
    $img = [System.Drawing.Bitmap]::FromFile($sourcePath)
    
    # Create 192x192 (multiple of 48px as required by Google)
    $bmp192 = New-Object System.Drawing.Bitmap(192, 192)
    $g192 = [System.Drawing.Graphics]::FromImage($bmp192)
    $g192.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g192.DrawImage($img, 0, 0, 192, 192)
    $bmp192.Save($destPath192, [System.Drawing.Imaging.ImageFormat]::Png)
    $g192.Dispose()
    $bmp192.Dispose()
    
    # Create 32x32 (standard)
    $bmp32 = New-Object System.Drawing.Bitmap(32, 32)
    $g32 = [System.Drawing.Graphics]::FromImage($bmp32)
    $g32.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g32.DrawImage($img, 0, 0, 32, 32)
    $bmp32.Save($destPath32, [System.Drawing.Imaging.ImageFormat]::Png)
    $g32.Dispose()
    $bmp32.Dispose()

    $img.Dispose()
    Write-Host "Created resized favicons for Google!"
}
