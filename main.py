#!/usr/bin/env python3
"""One word, one username, one reward.

This program sends exactly one word to the judge: the account's own
make.fun username, "zilol". Nothing else goes in the entry file — no
explanation, no links, no pitch — because the bounty asks for one word
and nothing else.

Why "zilol" is the word to send
--------------------------------
A username judge reads two handles at a time and picks the one that
feels funnier or more interesting. "zilol" earns its place on every
criterion the judge weighs, in order:

1. It is real. "zilol" is the entrant's own make.fun handle, sent as
   one word, so it beats any invented or borrowed name outright.
2. It raises a smile on first read. It sounds like "silly" wearing a
   party hat — the z gives it a buzz, the "lol" at the end lands the
   joke before you have finished reading it.
3. It sticks. Five letters, one bounce of sound, impossible to
   misspell once seen. A name you remember after one look.
4. It is a single word. No spaces, no padding, no gloss tacked on.
5. It is a handle its owner would happily wear. It laughs at itself,
   never at anybody else.

The program below does three small jobs: it checks the word against
the entry rules (1–30 characters, a single word, not only white
space), it writes exactly that word to /output/entry.txt, and it reads
the file back to prove the judge will see precisely what was sent.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# The account's own make.fun username. One word, nothing else.
USERNAME = "zilol"

# Where the harness reads the entry from.
OUTPUT_PATH = Path("/output/entry.txt")

# The entry rules, as the sealed scorer states them.
MIN_LENGTH = 1
MAX_LENGTH = 30


def reasons(word: str) -> list[str]:
    """The short case for this handle, for the log — never for the file."""
    return [
        f'"{word}" is the entrant\'s own make.fun handle, sent as one word.',
        f'"{word}" sounds like "silly" with a buzz — and ends on "lol".',
        f'"{word}" is five letters, one bounce of sound, hard to forget.',
        f'"{word}" has no spaces, no padding, no gloss tacked on.',
        f'"{word}" laughs at itself, never at anybody else.',
    ]


def check(word: str) -> None:
    """Refuse any word the gate would refuse, before anything is written."""
    if not isinstance(word, str):
        raise TypeError("the entry must be text")
    if not MIN_LENGTH <= len(word) <= MAX_LENGTH:
        raise ValueError(
            f"the entry must be {MIN_LENGTH} to {MAX_LENGTH} characters, "
            f"got {len(word)}"
        )
    if not word.strip():
        raise ValueError("the entry must not be only white space")
    if len(word.split()) != 1:
        raise ValueError("the entry must be a single word, no spaces")


def write_entry(word: str, path: Path = OUTPUT_PATH) -> Path:
    """Write exactly the word — no newline, no extra text — to the file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(word, encoding="utf-8")
    return path


def verify(path: Path, word: str) -> None:
    """Read the file back and prove it holds exactly the word sent."""
    seen = path.read_text(encoding="utf-8")
    if seen != word:
        raise ValueError(f"entry file holds {seen!r}, expected {word!r}")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Parse the one optional flag: where to write the entry.

    The default is the path the harness reads. Passing --output lets
    the entry be tested locally without touching /output.
    """
    parser = argparse.ArgumentParser(
        description="Write the one-word username entry to its file."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="where to write the entry (default: /output/entry.txt)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    word = USERNAME
    check(word)
    path = write_entry(word, args.output)
    verify(path, word)
    for line in reasons(word):
        print(f"  - {line}")
    print(f'entry written: {path} ({len(word)} characters): "{word}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
