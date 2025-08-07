"""Zoran IA execution engine.

This package contains the components required to execute a simple
proof‑of‑concept run of the Zoran framework.  The engine loads the
glottal grammar, parses glyphs and emits structured outputs.  In a
full implementation, this is where you would integrate the parser
with your AI orchestration layer (e.g. LangChain).
"""

from .run_poc import run

__all__ = ["run"]
