# Project 15 — Build a Cyber Playground: Your First Safe Virtual Machine

**Track:** Network Fundamentals  
**Type:** Automation (PowerShell + Bash)  
**Time:** ~90 minutes (mostly downloading/installing Ubuntu)  
**Difficulty:** Beginner

## The concept

A **virtual machine (VM)** is a computer inside your computer. It has its own
operating system, disk, and network settings. If an experiment goes wrong, you
delete the VM or restore a snapshot — your real computer stays safe. Think of it
as a padded practice room for cybersecurity.

This project gives you scripts to:

1. create a VirtualBox VM with sensible, safer defaults,
2. install a few beginner tools inside Ubuntu,
3. take a named snapshot so you can rewind.

The scripts do **not** download an operating system for you and do **not**
attack anything.

## What the code does

| File | Runs where | Purpose |
|---|---|---|
| `setup_vm.ps1` | Windows host | Creates the VirtualBox VM, disk, DVD drive, NAT network, optional host-only network |
| `vm_first_steps.sh` | Inside Ubuntu VM | Installs Python, curl, git, nano; creates `~/cyber-lab` with a local page |
| `snapshot_vm.ps1` | Windows host | Takes or lists snapshots |

`setup_vm.ps1` supports `-DryRun`, which prints every `VBoxManage` command
without changing anything. Try that first.

## What you need (all free)

- [VirtualBox](https://www.virtualbox.org/) installed on Windows.
- An Ubuntu Desktop ISO. Download the **official** ISO from
  [ubuntu.com/download/desktop](https://ubuntu.com/download/desktop).
- At least 8 GB of RAM on the host (4 GB for the VM), 30 GB free disk space,
  and virtualization enabled in your BIOS/UEFI.
- Administrator rights for the first VirtualBox install.

Do **not** download ISOs from random mirror sites. Check the official download
page and, if offered, verify the SHA-256 checksum with Project 03.

## Step 1 — Preview the VM setup

Open PowerShell in this folder:

```powershell
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\15-virtual-machine-lab"

powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 -DryRun
```

Read the commands. No VM is created in dry-run mode.

## Step 2 — Create the VM

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 `
  -IsoPath "C:\ISOs\ubuntu-24.04-desktop-amd64.iso"
```

Useful options:

```powershell
# Smaller VM for an 8 GB host
powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 `
  -IsoPath "C:\ISOs\ubuntu-24.04-desktop-amd64.iso" `
  -MemoryMB 3072 -Cpus 2 -DiskMB 20480

# Add an isolated host-only network (optional, may need Administrator)
powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 `
  -IsoPath "C:\ISOs\ubuntu-24.04-desktop-amd64.iso" -HostOnly

# Create and start
powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 `
  -IsoPath "C:\ISOs\ubuntu-24.04-desktop-amd64.iso" -Start
```

If a VM with the same name already exists, the script stops instead of deleting
it. Choose a new `-VmName` or remove the old VM manually in VirtualBox.

## Step 3 — Install Ubuntu

1. Start the VM in VirtualBox.
2. Choose **Try or Install Ubuntu**.
3. Use a normal installation. You can use a fake name and a throwaway password.
4. When installation finishes, reboot and log in.
5. In the VM menu, choose **Devices → Insert Guest Additions CD image** and
   install Guest Additions if you want a resizable window and clipboard support.

## Step 4 — Run the first-steps script inside the VM

Copy `vm_first_steps.sh` into the VM using a shared folder, a USB drive, or by
typing it in. Then:

```bash
chmod +x vm_first_steps.sh
./vm_first_steps.sh
```

It installs a few tools and creates `~/cyber-lab`. Start the local page:

```bash
cd ~/cyber-lab
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000` inside the VM. Press `Ctrl+C` to stop the server.

## Step 5 — Take a snapshot

Shut the VM down cleanly, then on the Windows host:

```powershell
powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1
```

List snapshots:

```powershell
powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -List
```

Take a lesson-specific snapshot:

```powershell
powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -SnapshotName "before-lab-02"
```

Restore if an experiment goes wrong:

```powershell
VBoxManage snapshot "CyberStarterLab" restore "clean-install"
```

## Network modes in plain language

| Mode | What it means | Use it for |
|---|---|---|
| **NAT** | The VM can browse out, but other machines cannot easily reach it | Default safe mode |
| **Host-only** | Only the host and other host-only VMs can talk to it | Local client/server labs |
| **Bridged** | The VM appears as a real device on your LAN | Only with explicit permission |

Keep **NAT** for normal lessons. Add **host-only** when you need two VMs to talk
to each other without exposing them to the real network.

## Safety rules

- This lab is for **defensive** learning and isolated experiments.
- Never attack a real website, school network, or public IP address.
- Do not enable shared folders for your entire home directory. Share one small
  practice folder, read-only if possible.
- Keep the VM updated, but do not install random “hacking tools” you do not
  understand.
- Snapshots are not backups of your host computer. Keep important files outside
  the VM.
- If you no longer need the VM, delete it and its disk from VirtualBox to free
  space.
