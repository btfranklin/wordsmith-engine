# Name Assets

`assets/Given Names.json` contains the canonical grouped given-name lists used by
`GivenName` and `AncientGivenName`.

The generated data comes from Wikidata Query Service results, using English
labels for items classified as male, female, or unisex given names. Wikidata
structured data is published under CC0-1.0. The grouped asset records the
refresh date and source URL in its `_meta` section.

Grouping rules:

- `english_speaking`: English-language given names.
- `latin_american`: Spanish-language and Portuguese-language given names.
- `eastern`: Japanese, Chinese, Korean, Vietnamese, Thai, Hindi, Sanskrit,
  Arabic, and Persian given names.
- `ancient`: Ancient Greek, Latin, Egyptian, Biblical Hebrew, Sumerian, and
  Akkadian given names.

Unisex given names are intentionally included in both the male and female lists.
Curated additions supplied by B.T. Franklin are included in the English-speaking
group.

The updater stops if any culture or gender query returns no names. Curated
additions do not hide an empty query result. The updater writes a complete
temporary file before it replaces the canonical asset, so a failed refresh
preserves the previous file.

From the repository root, refresh and synchronize the asset with:

```bash
python tools/update_name_assets.py
python tools/sync_assets.py
```

## Place and organization parts

`assets/Place and Organization Parts.json` contains project-authored word lists
for `TavernName`, `LandmarkName`, and `OrganizationName`. These lists are covered
by the repository license. They contain tavern animals and objects, landmark
features and compound parts, and organization symbols, trades, and concepts.
They are fictional naming vocabulary, not a register of real places or groups.

Edit this canonical file, then run `python tools/sync_assets.py`. Package copies
must preserve its bytes and list order. `tools/validate_assets.py` checks the
required keys and rejects empty lists, empty entries, and duplicate entries.

## Business, celestial, and creature parts

The following canonical assets contain project-authored naming vocabulary,
covered by the repository license:

- `assets/Business Name Parts.json`: colors, animals, trades, and shop types.
- `assets/Celestial Name Parts.json`: celestial objects and concepts.
- `assets/Creature Name Parts.json`: appearance roots, body parts, habitats,
  descriptors, animals, behavior adjectives, and creature types.

These lists support fictional names. They are not registers of companies,
astronomical objects, or species. Edit canonical assets and synchronize them
with `python tools/sync_assets.py`. Validation checks the required keys and
nonempty, unique entries. Preserve list order for seeded selection.
