# Project 12 — The Internet’s Address Book: A DNS Detective Story

**Track:** Network Fundamentals  
**Type:** Coding (Python) + CLI  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

Computers find each other with numbers called IP addresses, but people prefer
names like `example.com`. DNS is the internet’s contact list, translating names
into numbers behind the scenes. This project looks up the main record types
behind a domain and explains what they do.

## What the code does

`dns_detective.py` queries:

| Record | Meaning |
|---|---|
| `A` | IPv4 address |
| `AAAA` | IPv6 address |
| `MX` | Mail servers |
| `TXT` | Text records such as SPF and verification strings |
| `NS` | Authoritative name servers |
| `CNAME` | An alias to another name |

It handles missing records, timeouts, and nonexistent domains, and can print
JSON for a report.

## Install

```powershell
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\12-dns-detective"
py -3 -m pip install -r requirements.txt
```

## Run it

```powershell
# Look up the common records
py -3 dns_detective.py example.com

# Only mail and text records
py -3 dns_detective.py example.com --type MX,TXT

# Ask a specific public resolver
py -3 dns_detective.py example.com --nameserver 1.1.1.1

# Built-in demo
py -3 dns_detective.py --demo
```

Compare with the tools built into your operating system:

```powershell
nslookup example.com
Resolve-DnsName example.com
```

## The hosts-file bonus experiment (optional)

1. Make a backup of your hosts file:
   - Windows: `C:\Windows\System32\drivers\etc\hosts`
   - Linux/macOS: `/etc/hosts`
2. Add a line such as:
   ```text
   127.0.0.1   my-fake-site.example
   ```
3. Ping `my-fake-site.example` and see it resolve locally.
4. Remove the line and restore the backup.

You need administrator/root permission. This changes only your own machine.

## Experiments to try

1. Compare the MX records of a university and a news site.
2. Find the TXT records for a domain. Can you spot an SPF policy?
3. Look up a domain that does not exist. What status does the tool report?
4. Change the resolver to `1.1.1.1` or `8.8.8.8`. Do the answers differ?
5. Explain why DNS is often called “the phone book of the internet,” and why
   DNS privacy matters even when a website uses HTTPS.

## What you learn

- DNS resolution and common record types.
- Caching and TTL.
- How DNS can be misconfigured, monitored, or abused.

## Safety

This tool performs ordinary lookups. It does not scan, brute-force subdomains,
or attempt zone transfers. Only look up domains you are allowed to query.
