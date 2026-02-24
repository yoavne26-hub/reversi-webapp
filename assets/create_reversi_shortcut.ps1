param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$IconPath
)

$ErrorActionPreference = "Stop"

$desktopCandidates = @(
    [Environment]::GetFolderPath("Desktop"),
    (Join-Path $env:USERPROFILE "Desktop"),
    (Join-Path $env:USERPROFILE "OneDrive\Desktop")
) | Select-Object -Unique

$desktop = $desktopCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $desktop) {
    throw "Desktop folder not found."
}

$target = Join-Path $ProjectRoot "Play Reversi.bat"
if (-not (Test-Path $target)) {
    throw "Launcher not found: $target"
}

$shortcutPath = Join-Path $desktop "Play Reversi.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $ProjectRoot
$shortcut.Description = "Play Reversi (starts server and opens browser)"

if (Test-Path $IconPath) {
    $shortcut.IconLocation = $IconPath
} else {
    $shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,220"
}

$shortcut.Save()
Write-Host "Desktop shortcut created/updated:" $shortcutPath

