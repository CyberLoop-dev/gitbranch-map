#!/usr/bin/env python3
"""Read-only overview of local Git branches."""
import argparse
import subprocess
import sys

FORMAT = "%(HEAD)|%(refname:short)|%(upstream:short)|%(upstream:track)|%(committerdate:short)|%(subject)"

def main():
    parser = argparse.ArgumentParser(description="Summarize local Git branches.")
    parser.parse_args()
    try:
        result = subprocess.run(
            ["git", "for-each-ref", "--format=" + FORMAT, "refs/heads"],
            check=True, text=True, capture_output=True
        )
    except FileNotFoundError:
        raise SystemExit("Git was not found on PATH.")
    except subprocess.CalledProcessError:
        raise SystemExit("Run this command inside a Git repository.")
    print(f"{'':1} {'BRANCH':24} {'UPSTREAM':24} {'TRACKING':18} {'DATE':10} SUBJECT")
    for line in result.stdout.splitlines():
        head, name, upstream, track, date, subject = (line.split("|", 5) + [""] * 6)[:6]
        marker = "*" if head == "*" else " "
        print(f"{marker} {name[:24]:24} {(upstream or '-'):24} {(track or 'in sync')[:18]:18} {date:10} {subject}")

if __name__ == "__main__":
    main()
