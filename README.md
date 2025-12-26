# Big Map 🗺️  
**Automated Nmap Scanning Tool (Authorized Use Only)**

Big Map is a Python-based automation wrapper around **Nmap** that allows you to run multiple predefined Nmap scan profiles against one or more targets with clean, colorized CLI output.

It is designed for **authorized security testing, lab environments, and learning purposes**.


![Big Map Screenshot](/assets/big_map_screenshot.png)

---

## ✨ Features

- Run **multiple Nmap scans automatically** from a file
- Supports **single targets or target lists**
- Accepts **domains, IPs, and URLs** (URLs are normalized automatically)
- Clean, colorized CLI output using `colorama`
- Graceful handling of **CTRL+C (KeyboardInterrupt)**
- Modular and easy to extend

---

## Installation
```bash
git clone https://github.com/W4RSH3LL/Big_Map.git
cd Big_Map/
pip3 install -r requirements.txt
```

---

## Usage

- **Single Target:**
```bash
sudo python3 big_map.py -t vulnweb.com -s nmap_scans.txt
```

- **Multiple Targets: (From File)**
```bash
sudo python3 big_map.py -l targets.txt -s nmap_scans.txt
```

---

## 📄 Scan File Format
Your scan file (`nmap_scans.txt`) should contain one Nmap command **per line**, without the target.

Example:

```bash
nmap -Pn -T4 -p 1-1000
nmap -sS -Pn -T4 --max-retries 2 -p-
nmap -sV -Pn -p 80,443
nmap -A -Pn -T4 -p 1-1000
nmap -sU -Pn -p 53,67,123
```

Big Map automatically appends the target to each scan.

---

## ⚠️ Legal Disclaimer

This tool is intended for authorized use only.
You are responsible for ensuring you have explicit permission to scan any target.
Unauthorized scanning may be illegal in your jurisdiction.
