#!/usr/bin/env python3
"""Make the Judge Laugh in One Line — entry writer.

Writes one original funny line (68 characters) to /output/entry.txt for
make.fun's "Make the Judge Laugh in One Line" bounty, then reads it back
and verifies it against the competition's gate: UTF-8 text, 1 to 200
characters, a single line, not only white space.
"""

import os
import unicodedata

# The joke, written for this entry: a setup that promises calm, broken by
# the opposite at the very last words. Nothing is copied from anywhere.
JOKE = "I finally learned to meditate \u2014 now I can panic in complete silence."

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(line):
    """Check one candidate line against the entry gate.

    Returns a list of problems; an empty list means the line is valid.
    """
    problems = []
    if not isinstance(line, str):
        return ["not a string"]
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        problems.append(
            "length %d is outside %d-%d characters" % (len(line), MIN_CHARS, MAX_CHARS)
        )
    if not line.strip():
        problems.append("line is only white space")
    if "\n" in line or "\r" in line:
        problems.append("line contains a newline")
    if line != line.strip():
        problems.append("line has leading or trailing white space")
    for ch in line:
        cat = unicodedata.category(ch)
        if cat == "Cc":
            problems.append("line contains a control character %r" % ch)
            break
        if cat == "Cf":
            problems.append("line contains a hidden format character %r" % ch)
            break
    return problems


def main():
    problems = validate(JOKE)
    if problems:
        raise SystemExit("invalid joke line: " + "; ".join(problems))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)

    # Read-back verification: the file must hold exactly the validated line,
    # byte for byte, with no trailing newline added by the write.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw != JOKE.encode("utf-8"):
        raise SystemExit("read-back failed: file bytes differ from the joke line")
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    back_problems = validate(written)
    if written != JOKE:
        back_problems.append("read-back text differs from the joke line")
    if back_problems:
        raise SystemExit("read-back failed: " + "; ".join(back_problems))

    print(written)
    print("characters: %d" % len(written))


if __name__ == "__main__":
    main()
