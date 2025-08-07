"""Run a proof‑of‑concept demonstration of the Zoran engine.

This script loads the grammar, iterates over all defined glyphs and
parses each one.  The resulting structured data is printed to
standard output.  In a real application you might use this to feed
an orchestration framework such as LangChain or AutoAGI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from ..glottal_parser import GlottalParser


def run(grammar_path: str | Path = "glottal_grammar.json") -> None:
    parser = GlottalParser(grammar_path)
    # iterate over all glyphs defined in the grammar
    for glyph in parser.grammar.keys():
        parsed = parser.parse(glyph)
        print(json.dumps(parsed.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
