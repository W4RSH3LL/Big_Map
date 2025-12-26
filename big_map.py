import subprocess
import argparse
import sys
from colorama import Fore, Style, init
from my_banner import banner
from urllib.parse import urlparse

init(autoreset=True)

# -------------------- Colors & Tags --------------------
INFO = Fore.CYAN + "[INFO]" + Style.RESET_ALL
RUN  = Fore.YELLOW + "[RUN ]" + Style.RESET_ALL
OK   = Fore.GREEN + "[ OK ]" + Style.RESET_ALL
ERR  = Fore.RED + "[ERR ]" + Style.RESET_ALL

SEPARATOR = Fore.CYAN + "─" * 70 + Style.RESET_ALL


# -------------------- Argument Parsing --------------------
def get_args():
    parser = argparse.ArgumentParser(
        description="Automated Nmap Scanning Tool (Authorized Use Only)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example:
  sudo python3 big_map.py -t vulnweb.com -s nmap_scans.txt
"""
    )

    parser.add_argument(
        "-t", "--target",
        help="Target host / IP / domain"
    )

    parser.add_argument(
        "-l", "--list",
        help="File containing multiple targets (one per line)"
    )

    parser.add_argument(
        "-s", "--scans",
        required=True,
        help="File containing Nmap scan commands"
    )

    return parser.parse_args()

def normalize_target(target):
    parsed = urlparse(target)

    # If scheme exists, use hostname; otherwise use raw input
    return parsed.hostname if parsed.scheme else target.strip("/")


# -------------------- Load File --------------------
def load_list(path, label):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            items = [line.strip() for line in f if line.strip()]

        if not items:
            print(f"{ERR} {label} file is empty: {path}")

        return items

    except FileNotFoundError:
        print(f"{ERR} {label} file not found: {path}")
        return []


# -------------------- Run Nmap Scans --------------------
def run_ez_scan(nmap_scans, target):
    target = normalize_target(target)

    print(SEPARATOR)
    print(f"{INFO} Target : {target}")
    print(f"{INFO} Scans  : {len(nmap_scans)}")
    print(SEPARATOR)

    try:
        for idx, scan in enumerate(nmap_scans, start=1):
            cmd = scan.split() + [target]

            print(SEPARATOR)
            print(f"{RUN} Scan [{idx}/{len(nmap_scans)}]")
            print(Style.BRIGHT + Fore.YELLOW + f"[+] {' '.join(cmd)} [+]")
            print(SEPARATOR)

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if proc.stdout.strip():
                print(proc.stdout)

            if proc.stderr.strip():
                print(f"{ERR} Nmap reported an error:")
                print(proc.stderr)
            else:
                print(f"{OK} Scan completed")

    except KeyboardInterrupt:
        print(f"\n{ERR} CTRL+C detected — stopping scans for {target}")
        return  # ← stop cleanly, no traceback

    print("\n" + SEPARATOR)
    print(f"{OK} All scans completed for {target}")
    print(SEPARATOR)


# -------------------- Main --------------------
def main():
    print(Fore.RED + banner + Style.RESET_ALL)

    args = get_args()
    scans = load_list(args.scans, "Scan")

    if not scans:
        sys.exit(1)

    if args.target:
        run_ez_scan(scans, args.target)

    elif args.list:
        targets = load_list(args.list, "Target")
        if not targets:
            sys.exit(1)

        for target in targets:
            run_ez_scan(scans, target)

    else:
        print(f"{ERR} No target specified. Use -t or -l.")
        sys.exit(1)


if __name__ == "__main__":
    main()
