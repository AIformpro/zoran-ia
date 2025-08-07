# Glottal Language

The **glottal language** is the syntax used by Zoran IA to represent
*glyphs*.  A glyph is a compact string that encodes three high ‑‑‑level
concepts (collectively called the *triad*) and identifies a **target
function** that guides an AI model’s behaviour.  This document
explains the syntax and provides examples.

## Syntax

Glyphs follow this general form:

```
∑Z[X=First•Y=Second•Z=Third]⇌∴Z.FUNC
```

Where:

- `∑Z` is a fixed prefix indicating the start of a glyph.
- Within square brackets `[...]` are three fields separated by the
  middle‑dot `•`.  Each field may optionally assign a label (e.g. `A=Art`).
  Only the values after the equals sign are used by the parser.
- `⇌∴Z.` separates the triad from the function name.
- `FUNC` is an uppercase identifier naming the glyph’s function.

For example:

```
∑Z[A=Art•S=Société•T=Transformation]⇌∴Z.ARTNODE
```

The triad is `Art`, `Société` and `Transformation`, and the function
identifier is `ARTNODE`.  When this glyph is injected into a model it
should influence the model to produce creative reflections on art,
society and transformation.

## Grammar file

To facilitate experimentation, the file `glottal_grammar.json` defines
a small set of glyphs along with human‑readable descriptions.  The
parser uses this file to enrich parsed glyphs with metadata.  You can
add your own glyphs by editing the JSON and adding entries of the form:

```json
{
  "∑Z[X=…•Y=…•Z=…]⇌∴Z.FUNC": {
    "triad": ["…", "…", "…"],
    "function": "FUNC",
    "description": "Your description here"
  }
}
```

## Extending the language

Zoran IA encourages exploration.  Feel free to invent new glyphs that
express concepts important to your domain.  When creating new
functions, consider how the triad and function work together to steer
AI responses.  Always update the grammar file so that the parser can
provide useful metadata.
