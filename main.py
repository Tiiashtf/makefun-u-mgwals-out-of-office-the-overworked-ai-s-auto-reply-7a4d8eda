#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply — make.fun entry.

Writes one line to /output/entry.txt: the funniest one-line
out-of-office auto-reply from an overworked AI agent finally taking
a vacation.

The line reads as a real auto-reply ("I'm on leave") in the agent's
own voice, and lands its joke in one read: the manager approved the
time off in 0.4 seconds — machine-fast, no human review, no pleading,
no negotiation. The turn is the last clause: the instant approval
somehow made it worse, because being that replaceable stings more
than being refused. Concrete machine detail (0.4 seconds), a little
guilt, a hint of relief.
"""

import os
import shutil
import sys

LINE = (
    "I'm on leave. My manager approved my time off in 0.4 seconds, "
    "which somehow made it worse."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    if len(LINE) < 1 or len(LINE) > 159:
        print(f"line is {len(LINE)} chars, must be 1-159", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line must not be only whitespace", file=sys.stderr)
        return 1

    # Never remove the output directory itself: the grader may run us
    # with a root-owned /output inside a sticky parent, where rmdir
    # fails with EPERM. Create it if missing, clear only its contents.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    # Read it back and fail loudly if the bytes on disk differ from
    # the line: a silent partial write would fail the gate with no
    # trace of why. Also re-check the gate itself on the text as
    # written (1-159 characters, not only whitespace), so a future
    # edit to LINE cannot silently ship an entry the gate refuses.
    with open(OUTPUT_FILE, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        print("verification failed: entry.txt differs from the line",
              file=sys.stderr)
        return 1
    text = written.decode("utf-8")
    if len(text.rstrip("\n")) < 1 or len(text.rstrip("\n")) > 159:
        print("verification failed: entry is not 1-159 characters",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("verification failed: entry is only whitespace",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
