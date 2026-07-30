# Exotic Character Assets

`src/wordsmith/assets/Exotic Character Sets.json` contains curated Unicode
character sets used by `ExoticCharacter`.

## Alchemical Symbols

The `alchemicalSymbols` set contains the complete original Unicode alchemical
repertoire: the 116 consecutive characters from U+1F700 through U+1F773.

The source of truth is the Unicode Consortium's
[Alchemical Symbols names list](https://www.unicode.org/charts/nameslist/n_1F700.html).
Unicode characters and code points may be used without permission; the
Consortium's separately licensed code-chart glyph artwork is not copied into
this package.

Characters after U+1F773 are intentionally excluded. Although some reside in
the Alchemical Symbols block, they are astronomical symbols rather than members
of the original alchemical repertoire.

To refresh or verify this set:

1. Check the current Unicode names list for changes to the encoded repertoire.
2. Generate the inclusive sequence with
   `list(map(chr, range(0x1F700, 0x1F774)))`.
3. Run `pdm run pytest tests/test_exotic_character.py`.

Glyph appearance is font-dependent. The asset guarantees Unicode character
identity, not a particular historical or typographic drawing.
