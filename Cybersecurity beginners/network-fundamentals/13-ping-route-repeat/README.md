# Project 13 — Ping, Route, Repeat: Map a Trip Across the Internet

**Track:** Network Fundamentals  
**Type:** Coding (Python + OS commands)  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

Every message takes a road trip through many routers — like driving across the
country with lots of intersections. **Ping** tells you whether a destination is
awake and how long a reply takes. **Traceroute** shows the route it took. This
project measures both and turns the output into a readable summary.

## What the code does

`ping_route.py`:

- resolves a host name to an IP address,
- runs the normal `ping` command with a small packet count,
- parses minimum, average, and maximum latency,
- runs `tracert` (Windows) or `traceroute` (macOS/Linux),
- lists the hops and explains what stars and missing replies mean,
- includes a `--demo` mode against `example.com`.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\13-ping-route-repeat"

# Full demo
py -3 ping_route.py --demo

# A single host
py -3 ping_route.py example.com

# Gentle settings
py -3 ping_route.py example.com --count 3 --max-hops 10

# Ping only, no route trace
py -3 ping_route.py example.com --no-trace
```

On Linux, `traceroute` may need to be installed:

```bash
sudo apt install traceroute
```

## Experiments to try

1. Compare `example.com` with a site hosted far away. Which has higher latency?
2. Run the same trace twice. Do the hops or times change?
3. Find a hop that returns `* * *`. Look up why routers sometimes hide.
4. Ping your school’s public website. How many hops does it take?
5. Explain the difference between **latency** and **bandwidth**. Which does
   ping measure?

## What you learn

- ICMP, latency, and routing.
- How network diagnostics work.
- Why the internet is a path, not a direct wire.

## Safety

Use public, allowed destinations only. This tool runs `ping` and `traceroute`
with a small packet count and a short timeout. It is not a flood tool or a port
scanner. Do not probe networks you do not own or have permission to test.
