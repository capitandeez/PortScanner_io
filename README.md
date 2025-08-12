# PortScanner_io

**Fast, lightweight, extensible port scanner** written in Python for security professionals and developers. Ethical use only — scan systems you own or have permission for.

## Features
- TCP Connect scan (-sT)
- (Planned) SYN scan (-sS) — requires root
- Banner grabbing
- Threaded, fast scans
- Flexible target input: IP, range, CIDR, hostname
- Port selectors: single, range, top ports, full 1-65535
- Output: CLI table, JSON, CSV
- Proxy support (HTTP/SOCKS) via environment or future integration
- Save/load scan configs

## Installation
```bash
git clone https://github.com/youruser/PortScanner_io.git
cd PortScanner_io
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt