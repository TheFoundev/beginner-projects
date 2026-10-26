# Project 15 - Build a Cyber Playground: Your First Safe Virtual Machine
#
# Creates an isolated Ubuntu VM with VirtualBox, a NAT network, optional
# host-only networking, and a safe snapshot workflow.
#
# Run a preview first (no changes):
#   powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 -DryRun
#
# Create the VM:
#   powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 `
#       -IsoPath "C:\ISOs\ubuntu-24.04-desktop-amd64.iso"
#
# Safety:
#   This script only creates a local virtual machine. It does not attack
#   anything or change your host firewall.

[CmdletBinding()]
param(
    [string]$VmName = "CyberStarterLab",
    [string]$IsoPath = "",
    [int]$MemoryMB = 4096,
    [int]$Cpus = 2,
    [int]$DiskMB = 25600,
    [string]$VmFolder = "$env:USERPROFILE\VirtualBox VMs",
    [switch]$HostOnly,
    [switch]$Start,
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

function Invoke-VBox {
    param([string[]]$CommandArgs)
    $display = "VBoxManage " + ($CommandArgs -join " ")
    Write-Host "  > $display" -ForegroundColor DarkGray
    if ($DryRun) { return }
    $output = & $script:VBoxManage @CommandArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "VBoxManage failed with exit code $LASTEXITCODE. Output: $output"
    }
    $output | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
}

if ($MemoryMB -lt 2048 -or $MemoryMB -gt 16384) {
    throw "MemoryMB must be between 2048 and 16384."
}
if ($Cpus -lt 1 -or $Cpus -gt 8) {
    throw "Cpus must be between 1 and 8."
}
if ($DiskMB -lt 10240 -or $DiskMB -gt 200000) {
    throw "DiskMB must be between 10240 and 200000."
}

$VBoxManage = Find-VBoxManage
if (-not $VBoxManage) {
    if (-not $DryRun) {
        throw @"
VirtualBox was not found. Install it from https://www.virtualbox.org/ and run
this script again. On Windows, the default path is:
  C:\Program Files\Oracle\VirtualBox\VBoxManage.exe
"@
    }
    $VBoxManage = "VBoxManage"
}
$script:VBoxManage = $VBoxManage

if (-not $DryRun) {
    if (-not $IsoPath) {
        throw "IsoPath is required unless you use -DryRun. Download an Ubuntu Desktop ISO first."
    }
    if (-not (Test-Path $IsoPath)) {
        throw "ISO not found: $IsoPath"
    }
    $IsoPath = (Resolve-Path $IsoPath).Path
} else {
    if (-not $IsoPath) { $IsoPath = "C:\path\to\ubuntu-24.04-desktop-amd64.iso" }
    Write-Host "DRY RUN: no VM will be created." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CYBER STARTER LAB - VM SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "VM name    : $VmName"
Write-Host "Memory     : $MemoryMB MB"
Write-Host "CPUs       : $Cpus"
Write-Host "Disk       : $DiskMB MB"
Write-Host "ISO        : $IsoPath"
Write-Host "VM folder  : $VmFolder"
Write-Host "Host-only  : $HostOnly"
Write-Host "Start      : $Start"
Write-Host ""

if (-not $DryRun) {
    $existing = & $VBoxManage list vms 2>$null
    if ($existing -match [regex]::Escape("`"$VmName`"")) {
        throw "A VM named '$VmName' already exists. Choose another -VmName or remove it manually in VirtualBox."
    }
}

$machineFolder = Join-Path $VmFolder $VmName
$diskPath = Join-Path $machineFolder "$VmName.vdi"
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $machineFolder | Out-Null
}

Write-Host "[1/6] Creating the VM shell..." -ForegroundColor Green
Invoke-VBox @("createvm", "--name", $VmName, "--ostype", "Ubuntu_64", "--basefolder", $VmFolder, "--register")

Write-Host "[2/6] Setting safer defaults..." -ForegroundColor Green
Invoke-VBox @(
    "modifyvm", $VmName,
    "--memory", "$MemoryMB",
    "--cpus", "$Cpus",
    "--vram", "128",
    "--graphicscontroller", "vmsvga",
    "--audio", "none",
    "--usb", "off",
    "--clipboard", "disabled",
    "--draganddrop", "disabled",
    "--nic1", "nat",
    "--ioapic", "on",
    "--rtcuseutc", "on"
)

Write-Host "[3/6] Creating the virtual disk..." -ForegroundColor Green
Invoke-VBox @("createmedium", "disk", "--filename", $diskPath, "--size", "$DiskMB", "--format", "VDI")

Write-Host "[4/6] Attaching storage..." -ForegroundColor Green
Invoke-VBox @("storagectl", $VmName, "--name", "SATA", "--add", "sata", "--controller", "IntelAhci", "--portcount", "2")
Invoke-VBox @("storageattach", $VmName, "--storagectl", "SATA", "--port", "0", "--device", "0", "--type", "hdd", "--medium", $diskPath)
Invoke-VBox @("storageattach", $VmName, "--storagectl", "SATA", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", $IsoPath)
Invoke-VBox @("modifyvm", $VmName, "--boot1", "dvd", "--boot2", "disk", "--boot3", "none", "--boot4", "none")

if ($HostOnly) {
    Write-Host "[5/6] Adding an isolated host-only network..." -ForegroundColor Green
    if ($DryRun) {
        Invoke-VBox @("hostonlyif", "create")
        Invoke-VBox @("modifyvm", $VmName, "--nic2", "hostonly", "--hostonlyadapter2", "VirtualBox Host-Only Ethernet Adapter")
    } else {
        $hostOnlyOutput = & $VBoxManage hostonlyif create 2>&1
        $match = [regex]::Match(($hostOnlyOutput -join " "), "Interface '([^']+)'")
        if (-not $match.Success) {
            throw "Could not create a host-only adapter. Output: $hostOnlyOutput"
        }
        $adapterName = $match.Groups[1].Value
        Write-Host "    Created host-only adapter: $adapterName" -ForegroundColor DarkGray
        Invoke-VBox @("modifyvm", $VmName, "--nic2", "hostonly", "--hostonlyadapter2", $adapterName)
    }
} else {
    Write-Host "[5/6] Skipping host-only networking (use -HostOnly if you want it)." -ForegroundColor DarkGray
}

Write-Host "[6/6] Finishing touches..." -ForegroundColor Green
if ($Start) {
    Invoke-VBox @("startvm", $VmName, "--type", "gui")
}

Write-Host ""
if ($DryRun) {
    Write-Host "DRY RUN complete. Nothing was created or changed." -ForegroundColor Yellow
    Write-Host "Remove -DryRun and add -IsoPath to build the VM." -ForegroundColor Yellow
} else {
    Write-Host "VM setup complete." -ForegroundColor Green
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Start the VM in VirtualBox."
Write-Host "  2. Install Ubuntu Desktop inside the VM."
Write-Host "  3. Open a terminal in the VM and run vm_first_steps.sh."
Write-Host "  4. Shut the VM down cleanly."
Write-Host "  5. Take a snapshot so you can rewind:"
Write-Host "       powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -VmName `"$VmName`""
Write-Host ""
Write-Host "Safety reminders:" -ForegroundColor Yellow
Write-Host "  - Keep the VM on NAT unless you are doing the host-only exercise."
Write-Host "  - Do not enable shared folders for your whole home directory."
Write-Host "  - Take snapshots before experiments; delete them when finished."
Write-Host "  - Do not attack real networks from the VM."
