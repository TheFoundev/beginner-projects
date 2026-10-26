# Project 15 - Snapshot your cyber lab VM
#
# Take a named snapshot of your VirtualBox VM so you can rewind after an
# experiment. Snapshots are local and do not affect any other machine.
#
# Run:
#   powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1
#   powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -List
#   powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -SnapshotName "before-lab-02"
#
# Safety:
#   This only talks to VirtualBox on your computer. It does not touch the
#   network or any real system.

[CmdletBinding()]
param(
    [string]$VmName = "CyberStarterLab",
    [string]$SnapshotName = "clean-install",
    [string]$Description = "Clean Ubuntu install for safe cybersecurity practice",
    [switch]$List,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Find-VBoxManage {
    $candidates = @(
        "$env:ProgramFiles\Oracle\VirtualBox\VBoxManage.exe",
        "${env:ProgramFiles(x86)}\Oracle\VirtualBox\VBoxManage.exe",
        "VBoxManage.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) { return (Resolve-Path $candidate).Path }
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) { return $command.Source }
    }
    return $null
}

$VBoxManage = Find-VBoxManage
if (-not $VBoxManage) {
    if ($DryRun) {
        $VBoxManage = "VBoxManage"
    } else {
        throw "VirtualBox was not found. Install it from https://www.virtualbox.org/ first."
    }
}

if ($List) {
    Write-Host "Snapshots for '$VmName':" -ForegroundColor Cyan
    if ($DryRun) {
        Write-Host "  > VBoxManage snapshot `"$VmName`" list" -ForegroundColor DarkGray
    } else {
        & $VBoxManage snapshot $VmName list
        if ($LASTEXITCODE -ne 0) {
            throw "Could not list snapshots. Is the VM named '$VmName'?"
        }
    }
    return
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CYBER STARTER LAB - SNAPSHOT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "VM       : $VmName"
Write-Host "Snapshot : $SnapshotName"
Write-Host ""

$command = @(
    "snapshot", $VmName, "take", $SnapshotName,
    "--description", $Description
)
$display = "VBoxManage " + ($command -join " ")
Write-Host "  > $display" -ForegroundColor DarkGray

if (-not $DryRun) {
    $output = & $VBoxManage @command 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Snapshot failed with exit code $LASTEXITCODE. Output: $output"
    }
    $output | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
}

Write-Host ""
Write-Host "Snapshot complete." -ForegroundColor Green
Write-Host ""
Write-Host "If an experiment goes wrong later, restore with:" -ForegroundColor Cyan
Write-Host "  VBoxManage snapshot `"$VmName`" restore `"$SnapshotName`""
Write-Host ""
Write-Host "Tips:" -ForegroundColor Yellow
Write-Host "  - Shut the VM down cleanly before taking a snapshot."
Write-Host "  - Keep at most a few snapshots; they consume disk space."
Write-Host "  - Name snapshots after the lesson, for example 'before-lab-02'."
Write-Host "  - A snapshot is not a backup of your whole computer."
