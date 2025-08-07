"""Glottal parser for Zoran IA glyphs.

This module defines a small parser that understands the syntax used to
represent Zoran glyphs.  A glyph encodes three concepts (a *triad*) and
a target function.  For example::

    ∑Z[A=Art•S=Société•T=Transformation]⇌∴Z.ARTNODE

In this notation, the triad is `Art`, `Société` and `Transformation`,
and the target function is `ARTNODE`.  The parser exposes a simple
`GlottalParser` class that can extract this information from a glyph
string.  Optionally, it can enrich the parsed result using a grammar
defined in a JSON file.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


_GLYPH_RE = re.compile(r"∑Z\[(.*?)\]⇌∴Z\.([\w]+)")


@dataclass
class ParsedGlyph:
    """Structured representation of a parsed Zoran glyph."""

    triad: List[str]
    function: str
    description: Optional[str] = None
    extra: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        """Return a plain dictionary for JSON serialisation."""
        result: Dict[str, object] = {
            "triad": self.triad,
            "function": self.function,
        }
        if self.description:
            result["description"] = self.description
        if self.extra:
            result.update(self.extra)
        return result


class GlottalParser:
    """Parser for Zoran glyph strings.

    Parameters
    ----------
    grammar_path: Optional[str or Path]
        If provided, the parser will attempt to load additional
        metadata from this JSON grammar.  The grammar should map
        glyph strings to dictionaries containing at least the keys
        ``triad`` and ``function``.  Any additional keys will be
        merged into the parsed result.
    """

    def __init__(self, grammar_path: Optional[str | Path] = None) -> None:
        self.grammar: Dict[str, Dict[str, object]] = {}
        if grammar_path:
            self.load_grammar(grammar_path)

    def load_grammar(self, path: str | Path) -> None:
        """Load a JSON grammar from disk."""
        grammar_file = Path(path)
        if not grammar_file.is_file():
            raise FileNotFoundError(f"Grammar file not found: {path}")
        with grammar_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Grammar must be a JSON object mapping glyphs to definitions")
        # normalise keys: ensure triad lists are lists of strings
        for glyph, info in data.items():
            if 'triad' in info and isinstance(info['triad'], str):
                info['triad'] = [s.strip() for s in info['triad'].split('•')]
        self.grammar = data

    def parse(self, glyph: str) -> ParsedGlyph:
        """Parse a single glyph string into a :class:`ParsedGlyph`.

        Parameters
        ----------
        glyph: str
            The glyph string to parse.

        Returns
        -------
        ParsedGlyph
            Structured representation of the glyph.
        """
        match = _GLYPH_RE.search(glyph)
        if not match:
            raise ValueError(f"Invalid glyph format: {glyph}")
        triads_str, function = match.groups()
        triad_parts = [part.split('=', 1)[-1].strip() for part in triads_str.split('•')]
        parsed = ParsedGlyph(triad=triad_parts, function=function)
        # Enrich using grammar if available
        if glyph in self.grammar:
            info = self.grammar[glyph]
            # use explicit description if provided
            desc = info.get('description')
            if isinstance(desc, str):
                parsed.description = desc
            for key, value in info.items():
                if key not in {'triad', 'function', 'description'}:
                    parsed.extra[key] = value
        return parsed



def _cli() -> None:
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Parse Zoran glyphs and output JSON")
    parser.add_argument("glyph", help="Glyph string to parse (quote to avoid shell parsing)")
    parser.add_argument(
        "--grammar",
        help="Optional path to glottal_grammar.json for additional metadata",
    )
    args = parser.parse_args()
    glottal = GlottalParser(args.grammar)
    try:
        result = glottal.parse(args.glyph)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    import json as _json
    print(_json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
