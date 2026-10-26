# Cybersecurity Beginners — 20 Hands-On Projects

Twenty small, beginner-friendly cybersecurity projects for first-semester
engineering students. This repository is **source code and instructions**, not a
website. Each folder is a standalone project with its own `README.md`, runnable
code, and — where useful — fictional sample data.

The projects assume **zero cybersecurity knowledge** and only minimal
programming experience. They use free tools and stay defensive, ethical, and
sandboxed.

## Start here

1. Install **Python 3.10 or newer** from
   [python.org](https://www.python.org/downloads/). On Windows, tick
   **Add python.exe to PATH** during installation.
2. Open PowerShell and check:

   ```powershell
   py -3 --version
   ```

3. Install the four optional packages used by the collection:

   ```powershell
   cd "C:\Foundev\Cybersecurity beginners"
   py -3 -m pip install -r requirements.txt
   ```

   If you prefer an isolated environment, create one and call its Python
   directly:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

   When using that environment, replace `py -3` with
   `.\.venv\Scripts\python.exe` in the commands below. You can also install
   dependencies per project with its own `requirements.txt`.

4. Run a project from inside its folder. For example:

   ```powershell
   cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\01-caesar-cipher"
   py -3 caesar_cipher.py --demo
   ```

Every project works offline unless its README says otherwise. Projects 06, 07,
12, 13, and 18 make normal requests to public sites for teaching; they do not
scan, brute-force, or attack anything.

## The 20 projects

### 1. Cryptography Basics

| # | Project | What you build | Type |
|---|---|---|---|
| 01 | [Caesar Cipher](cryptography-basics/01-caesar-cipher/) | Encrypt, decrypt, and brute-force a classic shift cipher | Python |
| 02 | [Password Power Meter](cryptography-basics/02-password-power-meter/) | Score password strength and explain the result | Python |
| 03 | [Hash Detective](cryptography-basics/03-hash-detective/) | Compute SHA-256 hashes and verify downloads | Python |
| 04 | [Encrypted Diary](cryptography-basics/04-encrypted-diary/) | Encrypt and decrypt a folder with AES-GCM | Python + `cryptography` |
| 05 | [Encoding vs Encryption](cryptography-basics/05-encoding-vs-encryption/) | Compare Base64, ROT13, and real encryption | Python + `cryptography` |

### 2. Web Security 101

| # | Project | What you build | Type |
|---|---|---|---|
| 06 | [Padlock Detective](web-security-101/06-padlock-detective/) | Inspect TLS certificates and HTTPS | Python |
| 07 | [Security Header Safari](web-security-101/07-security-header-safari/) | Grade browser security headers | Python |
| 08 | [Cookie Trail](web-security-101/08-cookie-trail/) | Explore cookies on a local lab server | Python |
| 09 | [Form Fortress](web-security-101/09-form-fortress/) | Test good and bad form validation locally | Python |
| 10 | [Source Code Treasure Hunt](web-security-101/10-source-code-treasure-hunt/) | Audit two local sites for information leaks | Python |

### 3. Network Fundamentals

| # | Project | What you build | Type |
|---|---|---|---|
| 11 | [Packet Peekaboo](network-fundamentals/11-packet-peekaboo/) | Generate, capture, and analyze PCAP files | Python + `scapy` |
| 12 | [DNS Detective](network-fundamentals/12-dns-detective/) | Look up DNS records and compare resolvers | Python + `dnspython` |
| 13 | [Ping, Route, Repeat](network-fundamentals/13-ping-route-repeat/) | Measure latency and trace a route | Python |
| 14 | [Wi-Fi Inventory](network-fundamentals/14-wifi-inventory/) | Turn ARP/neighbor data into a device inventory | Python |
| 15 | [Virtual Machine Lab](network-fundamentals/15-virtual-machine-lab/) | Build and snapshot a safe VirtualBox lab | PowerShell + Bash |

### 4. Digital Forensics & OSINT

| # | Project | What you build | Type |
|---|---|---|---|
| 16 | [Phishing Autopsy](digital-forensics-osint/16-phishing-autopsy/) | Dissect `.eml` files without opening them | Python |
| 17 | [Metadata Mystery](digital-forensics-osint/17-metadata-mystery/) | Inspect and strip photo EXIF metadata | Python + `Pillow` |
| 18 | [Digital Footprint Audit](digital-forensics-osint/18-digital-footprint-audit/) | Audit your own public profiles | Python |
| 19 | [Safe Fake Virus](digital-forensics-osint/19-safe-fake-virus/) | Test antivirus with the harmless EICAR file | Python |
| 20 | [Browser Time Machine](digital-forensics-osint/20-browser-time-machine/) | Build a timeline from your own browser history | Python + SQLite |

## Commands for all 20 projects

Run each block from the project folder shown in the `cd` command. The exact
explanations, experiments, and safety notes are in each project’s `README.md`.

### Cryptography Basics

```powershell
# 01 - Caesar Cipher
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\01-caesar-cipher"
py -3 caesar_cipher.py --demo
py -3 caesar_cipher.py --message "HELLO WORLD" --shift 3
py -3 caesar_cipher.py --message "KHOOR ZRUOG" --shift 3 --decode

# 02 - Password Power Meter
cd "..\02-password-power-meter"
py -3 password_strength.py --demo

# 03 - Hash Detective
cd "..\03-hash-detective"
py -3 hash_detective.py --demo
py -3 hash_detective.py --file README.md

# 04 - Encrypted Diary (requires cryptography)
cd "..\04-encrypted-diary"
py -3 -m pip install -r requirements.txt
py -3 encrypted_diary.py demo

# 05 - Encoding vs Encryption (requires cryptography)
cd "..\05-encoding-vs-encryption"
py -3 -m pip install -r requirements.txt
py -3 encoding_vs_encryption.py
```

### Web Security 101

```powershell
# 06 - Padlock Detective
cd "C:\Foundev\Cybersecurity beginners\web-security-101\06-padlock-detective"
py -3 padlock_detective.py --demo
py -3 padlock_detective.py example.com

# 07 - Security Header Safari
cd "..\07-security-header-safari"
py -3 header_safari.py --demo
py -3 header_safari.py https://example.com

# 08 - Cookie Trail (local server)
cd "..\08-cookie-trail"
py -3 cookie_lab.py --demo

# 09 - Form Fortress (local server)
cd "..\09-form-fortress"
py -3 form_fortress.py --demo

# 10 - Source Code Treasure Hunt (local sites)
cd "..\10-source-code-treasure-hunt"
py -3 audit_site.py --demo
py -3 audit_site.py vulnerable_site
py -3 audit_site.py fixed_site
py -3 serve_site.py --site vulnerable_site
```

### Network Fundamentals

```powershell
# 11 - Packet Peekaboo (requires scapy; capture may need Npcap)
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\11-packet-peekaboo"
py -3 -m pip install -r requirements.txt
py -3 analyze_pcap.py --demo
py -3 capture_packets.py --list-interfaces

# 12 - DNS Detective (requires dnspython)
cd "..\12-dns-detective"
py -3 -m pip install -r requirements.txt
py -3 dns_detective.py --demo
py -3 dns_detective.py example.com

# 13 - Ping, Route, Repeat
cd "..\13-ping-route-repeat"
py -3 ping_route.py --demo
py -3 ping_route.py example.com --count 3 --max-hops 10

# 14 - Wi-Fi Inventory
cd "..\14-wifi-inventory"
py -3 network_inventory.py --demo
py -3 network_inventory.py --input samples/arp_sample.txt

# 15 - Virtual Machine Lab (PowerShell on Windows)
cd "..\15-virtual-machine-lab"
powershell -ExecutionPolicy Bypass -File .\setup_vm.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\snapshot_vm.ps1 -List
```

### Digital Forensics & OSINT

```powershell
# 16 - Phishing Autopsy
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\16-phishing-autopsy"
py -3 phishing_autopsy.py --demo

# 17 - Metadata Mystery (requires Pillow)
cd "..\17-metadata-mystery"
py -3 -m pip install -r requirements.txt
py -3 photo_metadata.py demo

# 18 - Digital Footprint Audit
cd "..\18-digital-footprint-audit"
py -3 footprint_audit.py --demo

# 19 - Safe Fake Virus
cd "..\19-safe-fake-virus"
py -3 eicar_lab.py demo

# 20 - Browser Time Machine
cd "..\20-browser-time-machine"
py -3 browser_timeline.py --demo
py -3 browser_timeline.py --list
```

## Dependencies

Most projects use only the Python standard library.

| Package | Needed by | Why |
|---|---|---|
| `cryptography` | 04, 05 | AES-GCM encryption and comparison demos |
| `dnspython` | 12 | DNS record lookups |
| `scapy` | 11 | Generate, capture, and parse packets |
| `Pillow` | 17 | Read and write image metadata |

Install everything at once from the repository root:

```powershell
py -3 -m pip install -r requirements.txt
```

Projects 08, 09, and 10 start local web servers on `127.0.0.1` only. Stop them
with `Ctrl+C`.

## How the folders are organized

```text
Cybersecurity beginners/
├─ README.md                     <- this file
├─ requirements.txt              <- all optional packages
├─ cryptography-basics/          <- projects 01-05
├─ web-security-101/             <- projects 06-10
├─ network-fundamentals/         <- projects 11-15
└─ digital-forensics-osint/      <- projects 16-20
```

Each numbered folder contains:

- the runnable source code,
- a `README.md` with the concept, commands, experiments, and safety notes,
- sample or generated data where the project needs it,
- a `requirements.txt` only when an external package is needed.

Some samples are generated on first run:

- Project 11 creates `samples/demo.pcap` with `make_sample_pcap.py`.
- Project 17 creates `samples/demo_photo.jpg` and a cleaned copy with its demo.
- Project 20 creates `samples/history_sample.sqlite` with its demo.

## Safety and ethics rules

These projects are for **learning defense**, not for attacking people or
systems.

- **Only test systems you own or have explicit permission to test.**
- Never scan, probe, phish, or attack a school, employer, public website, or
  someone else’s network.
- Use the bundled fictional data, localhost servers, and reserved example
  domains (`.example`, `192.0.2.0/24`).
- Do not inspect another person’s browser history, photos, email, or accounts
  without permission.
- Do not create or download real malware. Project 19 uses the harmless EICAR
  test string only.
- Keep real passwords, tokens, and personal data out of screenshots, CSVs, and
  shared folders.
- If you discover a real vulnerability, report it privately to the owner. Do not
  exploit it.
- When in doubt, stop and ask your instructor or IT/security team.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognized | Use `py -3` on Windows, or reinstall Python with PATH enabled |
| `No module named cryptography` / `dns` / `scapy` / `PIL` | Run `py -3 -m pip install -r requirements.txt` from the repository root |
| PowerShell blocks a `.ps1` script | Use `powershell -ExecutionPolicy Bypass -File .\script.ps1` for that run |
| Packet capture fails | Install [Npcap](https://npcap.com/) and run the capture from an Administrator terminal; analysis of the sample PCAP needs neither |
| Browser History is locked or empty | Close Chrome/Edge, copy the `History` file, then use `--db PATH` |
| Antivirus deletes the EICAR file | That is a successful test. Check the antivirus quarantine/history |
| Website requests fail | Check your connection; projects 06, 07, 12, 13, and 18 need internet access |
| A local server port is busy | Stop the other server or pass a different port where the project supports it |

## Suggested learning path

1. Start with **01–03** to learn ciphers, passwords, and hashes.
2. Move to **06–07** for HTTPS and browser security.
3. Try **11–14** for packets, DNS, and networks.
4. Finish with **16–20** for forensics and privacy.
5. Do **15** when you are ready to build an isolated virtual lab.

Each project ends with experiments. Do them — reading the code is not the same
as running it and changing it.

## License and use

These are teaching examples. Use them for personal learning, classrooms, and
clubs. Do not present them as production security tools. They are intentionally
small and simplified so beginners can read every line.
