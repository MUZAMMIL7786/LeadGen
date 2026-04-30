Add-Type -AssemblyName System.Drawing

$paths = @("d:\github\LeadGen\assets\images\logo.png", "d:\github\LeadGen\favicon.png")

foreach ($path in $paths) {
    if (Test-Path $path) {
        $img = [System.Drawing.Bitmap]::FromFile($path)
        
        $minX = $img.Width
        $minY = $img.Height
        $maxX = 0
        $maxY = 0

        # Find the bounding box of non-transparent pixels
        for ($y = 0; $y -lt $img.Height; $y++) {
            for ($x = 0; $x -lt $img.Width; $x++) {
                $color = $img.GetPixel($x, $y)
                if ($color.A -gt 10) { # Threshold to ignore almost transparent pixels
                    if ($x -lt $minX) { $minX = $x }
                    if ($x -gt $maxX) { $maxX = $x }
                    if ($y -lt $minY) { $minY = $y }
                    if ($y -gt $maxY) { $maxY = $y }
                }
            }
        }

        # Calculate new dimensions
        $newWidth = $maxX - $minX + 1
        $newHeight = $maxY - $minY + 1

        if ($newWidth -gt 0 -and $newHeight -gt 0) {
            $rect = New-Object System.Drawing.Rectangle($minX, $minY, $newWidth, $newHeight)
            $cropped = $img.Clone($rect, $img.PixelFormat)
            
            $img.Dispose()
            
            $cropped.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
            $cropped.Dispose()
            Write-Host "Cropped $path to ${newWidth}x${newHeight}"
        } else {
            $img.Dispose()
            Write-Host "No non-transparent pixels found in $path"
        }
    }
}
