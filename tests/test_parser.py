"""Unit tests for the Zoran glottal parser."""

import unittest
import sys
from pathlib import Path

# Allow the tests to import modules from the parent directory
TEST_DIR = Path(__file__).resolve().parent
ROOT_DIR = TEST_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from glottal_parser import GlottalParser  # type: ignore


class TestGlottalParser(unittest.TestCase):
    def setUp(self) -> None:
        # Locate the grammar file relative to the project root
        grammar_path = ROOT_DIR / "glottal_grammar.json"
        self.parser = GlottalParser(str(grammar_path))

    def test_parse_valid_glyph(self):
        glyph = "∑Z[A=Art•S=Société•T=Transformation]⇌∴Z.ARTNODE"
        parsed = self.parser.parse(glyph).to_dict()
        self.assertEqual(parsed["triad"], ["Art", "Société", "Transformation"])
        self.assertEqual(parsed["function"], "ARTNODE")
        self.assertIn("description", parsed)

    def test_parse_invalid_glyph(self):
        with self.assertRaises(ValueError):
            self.parser.parse("invalid glyph")

    def test_parse_custom_glyph_without_grammar(self):
        parser = GlottalParser()  # no grammar loaded
        glyph = "∑Z[X=Alpha•Y=Beta•Z=Gamma]⇌∴Z.FOO"
        parsed = parser.parse(glyph)
        self.assertEqual(parsed.triad, ["Alpha", "Beta", "Gamma"])
        self.assertEqual(parsed.function, "FOO")
        self.assertIsNone(parsed.description)


if __name__ == '__main__':
    unittest.main()
