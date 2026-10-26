# Project 14 — Who’s on My Wi-Fi? Build a Home Network Inventory

**Track:** Network Fundamentals  
**Type:** Coding (Python) + Router  
**Time:** ~45 minutes  
**Difficulty:** Beginner

## The concept

Good security starts with knowing what is connected to your network — like
counting every door and window in your house before bed. Your router keeps a
guest list of devices, and the local ARP/neighbor table can help you
double-check it. This project builds a simple inventory and highlights mystery
guests.

## What the code does

`network_inventory.py`:

- reads your operating system’s ARP/neighbor table (`arp -a` or `ip neigh`),
- extracts IP addresses and MAC addresses,
- filters out multicast and broadcast noise,
- flags locally administered (often privacy-randomized) MAC addresses,
- merges an optional `known_devices.csv` with owner/trust notes,
- writes a clean CSV inventory,
- includes a demo using a safe sample table.

It does **not** scan, ping, or probe any device.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\14-wifi-inventory"

# Try it on the bundled sample first
py -3 network_inventory.py --demo

# Read your own neighbor table
py -3 network_inventory.py

# Add your known-device list
py -3 network_inventory.py --known samples/known_devices.csv --output inventory.csv

# Or parse a saved ARP output
py -3 network_inventory.py --input samples/arp_sample.txt
```

The code is cross-platform:

| OS | Command used |
|---|---|
| Windows | `arp -a` |
| Linux | `ip neigh` (falls back to `arp -an`) |
| macOS | `arp -an` |

## Build your own guest list

1. Copy `samples/known_devices.csv` to `known_devices.csv`.
2. Add the MAC addresses of your own devices.
3. Give each one an owner and a trust level (`trusted`, `guest`, `review`).
4. Run the script again and compare.
5. Log in to your own router (with the owner’s permission) and compare its
   device list with the inventory.

## Experiments to try

1. Which devices on your network have a randomized MAC address? Why do phones
   do that?
2. Can you match every IP address to a physical device?
3. Find one device you cannot identify. What would you check next?
4. Compare the inventory before and after a guest joins the Wi-Fi.
5. Explain why an unknown device is not automatically an attacker, but is worth
   investigating.

## What you learn

- Asset inventory and network visibility.
- ARP, MAC addresses, and basic access control.
- How to investigate calmly instead of guessing.

## Safety

Only inventory a network you own or have explicit permission to manage. This
tool reads a local table; it does not perform discovery scans. Do not use it on
a school, workplace, or public network without permission.
