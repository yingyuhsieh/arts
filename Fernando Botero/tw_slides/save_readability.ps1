$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$records = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'readability_edits.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$targetDir = Join-Path $PSScriptRoot 'update'
$backupDir = Join-Path $PSScriptRoot 'before_readability_20260907'
[IO.Directory]::CreateDirectory($backupDir) | Out-Null
foreach ($item in $records) {
    $suffix = '_slide_{0:D4}.png' -f [int]$item.id
    $target = @(Get-ChildItem -LiteralPath $targetDir -File | Where-Object { $_.Name.EndsWith($suffix) })
    if ($target.Count -ne 1) { throw "Expected one target for $suffix" }
    $backup = Join-Path $backupDir $target[0].Name
    if (-not (Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $target[0].FullName -Destination $backup }
    Copy-Item -LiteralPath $item.source -Destination $target[0].FullName -Force
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $sourceHash = [BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($item.source)))
        $targetHash = [BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($target[0].FullName)))
        if ($sourceHash -ne $targetHash) { throw 'Copy verification failed' }
    } finally { $sha.Dispose() }
    $savedImage = [Drawing.Image]::FromFile($target[0].FullName)
    try {
        if ($savedImage.Width -lt 1280 -or $savedImage.Height -lt 720) { throw 'Unexpected resolution' }
        Write-Output "Verified slide $($item.id): $($savedImage.Width)x$($savedImage.Height)"
    } finally { $savedImage.Dispose() }
}
