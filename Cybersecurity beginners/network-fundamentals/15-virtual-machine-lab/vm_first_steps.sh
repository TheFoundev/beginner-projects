#!/usr/bin/env bash
# Project 15 - First steps inside your Ubuntu cyber lab VM
#
# Run this INSIDE the virtual machine, not on your real computer:
#   chmod +x vm_first_steps.sh
#   ./vm_first_steps.sh
#
# It installs a few beginner tools, creates a small local web page, and prints
# the commands for starting a local practice server.
#
# Safety: this only changes the throwaway VM. It does not scan or attack
# anything on your network.

set -euo pipefail

if [[ "${EUID}" -eq 0 ]]; then
    SUDO=""
else
    SUDO="sudo"
fi

if ! command -v apt-get >/dev/null 2>&1; then
    echo "This script expects Ubuntu or another Debian-based Linux."
    echo "Install the tools manually and create ~/cyber-lab."
    exit 1
fi

echo "============================================================"
echo "  CYBER STARTER LAB - FIRST STEPS"
echo "============================================================"
echo "Updating package lists..."
$SUDO apt-get update

echo "Installing beginner tools..."
$SUDO apt-get install -y python3 python3-pip python3-venv curl git nano

LAB="$HOME/cyber-lab"
mkdir -p "$LAB"

cat > "$LAB/index.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My Cyber Lab</title>
  <style>
    body { max-width: 720px; margin: 60px auto; padding: 0 20px;
           font-family: system-ui, sans-serif; line-height: 1.6;
           background: #f7f7f2; color: #172033; }
    .card { background: #fff; border: 1px solid #d9dee7;
            border-radius: 16px; padding: 28px; }
    code { background: #eef1f5; padding: 2px 5px; border-radius: 5px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>My Cyber Lab is alive</h1>
    <p>This page is served from <code>127.0.0.1:8000</code> inside your VM.</p>
    <p>It is isolated from the real internet unless you intentionally give the
    VM network access. Use it for local web-security experiments.</p>
  </div>
</body>
</html>
HTML

cat > "$LAB/README.txt" <<'TEXT'
Cyber Lab notes
===============

Start a local web server:
  cd ~/cyber-lab
  python3 -m http.server 8000 --bind 127.0.0.1

Open:
  http://127.0.0.1:8000

Stop the server:
  Ctrl+C

Safety checklist:
  [ ] The VM has a snapshot named clean-install.
  [ ] I am not attacking real websites or networks.
  [ ] I keep fake data in the VM, not real passwords.
  [ ] I shut down the VM cleanly after each session.
TEXT

echo ""
echo "Installed tools:"
python3 --version
curl --version | head -n 1
git --version

echo ""
echo "Created: $LAB"
echo "Files  : index.html, README.txt"
echo ""
echo "Your VM's IPv4 addresses:"
ip -4 addr show scope global 2>/dev/null | awk '/inet / {print "  " $2 " on " $NF}'
echo ""
echo "Next commands:"
echo "  cd ~/cyber-lab"
echo "  python3 -m http.server 8000 --bind 127.0.0.1"
echo "  # Open http://127.0.0.1:8000 inside the VM"
echo ""
echo "Before experiments, take a snapshot from the host:"
echo "  powershell -ExecutionPolicy Bypass -File .\\snapshot_vm.ps1"
echo ""
echo "Done. Keep the lab isolated and have fun."
