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

From the repository root, refresh and synchronize the asset with:

```bash
python tools/update_name_assets.py
python tools/sync_assets.py
```
