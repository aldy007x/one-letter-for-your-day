"""One Letter for Your Day — make.fun entry.

The brief: send exactly one letter, A to Z, standing for the word that
describes your day — and nothing else. No word, no gloss, no punctuation.
A judge reads two letters at a time and picks the one whose hidden word
feels most vivid, funnier, or truer.

So the whole entry is a choice of letter. This program makes that choice
the way the judge's published brief weighs it, most important first:

1. vivid and specific — the word calls up a sharp picture of the day;
2. funny or surprising — the kind of thing a reader repeats to a friend;
3. true to a real day — an honest report, not a performance;
4. the letter suits its word — the word's own initial, fitting its sound.

Each candidate is a day-word with a score on those four, and the winner
is the letter of the highest-scoring word. The day matters too: the
program reads the weekday, so a word tied to a day of the week (Friday
feeling) is only honest on that day — today is Tuesday, and a day that
ran clean through the night is honestly a zero-sleep day.

The program writes exactly that one letter — one byte, no newline — to
/output/entry.txt, after checking it passes the sealed gate: UTF-8 text
of 1 to 1 characters, a letter A to Z, not only white space.
"""

import os
from datetime import date
from pathlib import Path

# (letter, word, vivid, funny, true, fit) — each score 0-5.
# The word is the letter's own initial in every case: the letter has to
# suit its word, not merely hint at it.
CANDIDATES = [
    ("Z", "zero sleep", 5, 5, 5, 5),   # a whole night with no sleep in it
    ("B", "burnout", 4, 3, 5, 5),      # running on fumes, honestly
    ("G", "grinding", 4, 2, 5, 5),     # one build after another, all day
    ("E", "exhausted", 4, 2, 5, 5),    # wrung out by the day
    ("Y", "yawning", 4, 3, 4, 5),      # the body keeping the score
    ("W", "wiped", 4, 3, 4, 5),        # wiped out, in one word
    ("F", "Friday-feeling", 3, 4, 1, 5),  # only true on a Friday
    ("A", "amazing", 2, 1, 3, 5),      # vague mood, no picture
]

# The judge weighs the criteria in order, so the weights fall in order:
# vivid first, then funny, then true, then fit.
WEIGHTS = (4, 3, 2, 1)

# The grader runs this program in a sandbox where /output exists.
# ENTRY_OUTPUT lets me verify the same code path locally.
OUTPUT_PATH = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def score(candidate, today):
    """Score one candidate the way the judge's brief weighs the criteria."""
    letter, word, vivid, funny, true, fit = candidate
    if word == "Friday-feeling" and today.weekday() != 4:
        # A Friday feeling on a Tuesday is not an honest report.
        true = 0
    return sum(w * s for w, s in zip(WEIGHTS, (vivid, funny, true, fit)))


def pick_letter(today):
    """The letter whose hidden word lands hardest. Deterministic: the
    scores are fixed and the only input is the date, so two runs on the
    same day always agree."""
    ranked = sorted(CANDIDATES, key=lambda c: score(c, today), reverse=True)
    return ranked[0][0]


def main():
    letter = pick_letter(date.today())
    assert len(letter) == 1, "entry must be exactly one character"
    assert "A" <= letter <= "Z", "entry must be a letter A to Z"
    assert letter.strip(), "entry must not be only white space"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(letter, encoding="utf-8")
    assert OUTPUT_PATH.read_text(encoding="utf-8") == letter
    print(f"wrote {letter!r} to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
