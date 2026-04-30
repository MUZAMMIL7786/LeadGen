Add-Type -AssemblyName System.Drawing

$paths = @("d:\github\LeadGen\assets\images\logo.png", "d:\github\LeadGen\favicon.png")

foreach ($path in $paths) {
    if (Test-Path $path) {
        $img = [System.Drawing.Bitmap]::FromFile($path)
        $newImg = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
        
        $minX = $img.Width
        $minY = $img.Height
        $maxX = 0
        $maxY = 0

        # Step 1: Make white/off-white background transparent and find bounds
        for ($y = 0; $y -lt $img.Height; $y++) {
            for ($x = 0; $x -lt $img.Width; $x++) {
                $color = $img.GetPixel($x, $y)
                
                # Check if it's NOT a background color (background is either transparent, white, or very light gray)
                $isBg = ($color.A -lt 20) -or ($color.R -gt 240 -and $color.G -gt 240 -and $color.B -gt 240)
                
                if (-not $isBg) {
                    # Keep original color
                    $newImg.SetPixel($x, $y, $color)
                    
                    # Update bounds
                    if ($x -lt $minX) { $minX = $x }
                    if ($x -gt $maxX) { $maxX = $x }
                    if ($y -lt $minY) { $minY = $y }
                    if ($y -gt $maxY) { $maxY = $y }
                } else {
                    # Set to transparent
                    $newImg.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
                }
            }
        }

        # Step 2: Crop to bounds
        $newWidth = $maxX - $minX + 1
        $newHeight = $maxY - $minY + 1

        if ($newWidth -gt 0 -and $newHeight -gt 0) {
            $rect = New-Object System.Drawing.Rectangle($minX, $minY, $newWidth, $newHeight)
            $cropped = $newImg.Clone($rect, $newImg.PixelFormat)
            
            $img.Dispose()
            $newImg.Dispose()
            
            $cropped.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
            $cropped.Dispose()
            Write-Host "Processed and cropped $path to ${newWidth}x${newHeight}"
        } else {
            $img.Dispose()
            $newImg.Dispose()
            Write-Host "Failed to find logo pixels in $path"
        }
    }
}
