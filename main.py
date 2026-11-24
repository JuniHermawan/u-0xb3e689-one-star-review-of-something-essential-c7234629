#!/usr/bin/env python3
"""One-Star Review of Something Essential — make.fun entry.

Writes one deadpan one-star review (<=160 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Python 3.13 standard library only. Deterministic: same text every run.

Version history:
  v1 — gravity / dropped phone, "One star." lead, sting lands last.
       Pick: "One star. Gravity dropped my new phone face-down on
       concrete and has never once picked anything up."
       Calibration: beat control (margin 5) and runner-up sleep
       variant (margin 2); see calibration.md in the workdir.
  v2 — added a read-back gate: after writing, the file is re-read as
       UTF-8 and asserted byte-identical to the reviewed text, so a
       partial or mis-encoded write fails loudly instead of shipping.
"""
import os
import sys

REVIEW = (
    "One star. Gravity dropped my new phone face-down on concrete "
    "and has never once picked anything up."
)


def main() -> int:
    text = REVIEW.strip()
    # Self-check gate: mirrors the sealed scorer, plus the brief's
    # deadpan rules (one line, no exclamation marks doing the work).
    assert 1 <= len(text) <= 160, f"review is {len(text)} chars, must be 1-160"
    assert text.strip(), "review is only whitespace"
    assert "\n" not in text and "\r" not in text, "review must be one line"
    assert "!" not in text, "deadpan: no exclamation marks"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Read-back gate: the shipped file must be byte-identical to the
    # reviewed text, valid UTF-8, and still inside the 1-160 gate.
    with open(path, "r", encoding="utf-8") as f:
        shipped = f.read()
    assert shipped == text, "entry.txt differs from the reviewed text"
    assert 1 <= len(shipped) <= 160, "shipped text outside 1-160 chars"
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
