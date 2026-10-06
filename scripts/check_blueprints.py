#!/usr/bin/env python3
"""Pre-commit safety check: scan make/*.json (and other text files) for things that should not be committed.
Usage: python scripts/check_blueprints.py [folder ...]   (default: make templates config sheets)
Exit code 1 if anything suspicious is found.
"""
import os, re, sys

PATTERNS = {
    "SA mobile (+27...)": re.compile(r"\+27(?!0{6})\d{9}"),
    "SA mobile (0xx...)": re.compile(r"\b0[6-8]\d{8}\b"),
    "email (not example.com)": re.compile(r"[\w.+-]+@(?!example\.com)[\w-]+\.[\w.]+"),
    "Anthropic key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "Meta/long token": re.compile(r"\bEA[A-Za-z0-9]{60,}\b"),
    "generic long secret": re.compile(r"[\"'][A-Za-z0-9_\-]{40,}[\"']"),
}
folders = sys.argv[1:] or ["make", "templates", "config", "sheets"]
problems = 0
for folder in folders:
    for dirpath, _, files in os.walk(folder):
        for name in files:
            if not name.endswith((".json", ".csv", ".md", ".txt")):
                continue
            path = os.path.join(dirpath, name)
            text = open(path, encoding="utf-8", errors="ignore").read()
            for label, pat in PATTERNS.items():
                for m in pat.finditer(text):
                    problems += 1
                    print(f"{path}: {label}: {m.group(0)[:40]}")
print("OK: nothing suspicious found." if problems == 0 else f"{problems} possible problem(s). Fix before committing.")
sys.exit(1 if problems else 0)
