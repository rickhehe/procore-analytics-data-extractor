#!powershell

# Setup script for Procore Analytics Extractor
Write-Host "Setting up Procore Analytics Extractor..." -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created. Please edit it with your configuration." -ForegroundColor Yellow
}

# Check if any .share files exist in config directory
$share_files = Get-ChildItem -Path "config" -Filter "*.share" -Exclude "*.example"
if ($share_files.Count -eq 0) {
    Write-Host "Creating Delta Sharing profile from template..."
    $profile_name = Read-Host "Enter a name for your Delta Sharing profile (e.g., 'production', 'dev')"
    if ([string]::IsNullOrWhiteSpace($profile_name)) {
        $profile_name = "my_profile"
    }
    
    $target_file = "config/$profile_name.share"
    Copy-Item "config/delta_sharing_profile.share.example" $target_file
    Write-Host "Created $target_file. Please edit it with your actual credentials." -ForegroundColor Yellow
    
    # Update .env to point to the new file
    $env_content = Get-Content ".env"
    $env_content = $env_content -replace "CONFIG_PATH=.*", "CONFIG_PATH=$target_file"
    $env_content | Set-Content ".env"
    Write-Host "✓ Updated .env to use $target_file"
}

Write-Host ""
Write-Host "Setup complete! Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit your .share file with actual Delta Sharing credentials"
Write-Host "2. Run: $ .\script\run.ps1"
