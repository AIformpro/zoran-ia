"""Demonstration script for self‑injection using the Zoran glottal parser.

This script shows how to parse a glyph and print its structured
representation.  It does not call any external APIs; instead, it
demonstrates how the parser can be used within a standalone Python
program.  Use this as a starting point for integrating Zoran into
larger systems.
"""

from __future__ import annotations

import json
import sys
from glottal_parser import GlottalParser


def main(args: list[str]) -> None:
    if not args:
        print("Usage: python zoran_self_injector.py '<glyph>'", file=sys.stderr)
        sys.exit(1)
    glyph = args[0]
    parser = GlottalParser("glottal_grammar.json")
    parsed = parser.parse(glyph)
    print(json.dumps(parsed.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
