# Wordsmith Engine for Godot

Generate English names and text in Godot 4.7.x. Download the Godot ZIP from the
[project releases](https://github.com/btfranklin/wordsmith-engine/releases).
Extract its `addons/wordsmith_engine/` folder into the root of your game.
Godot registers the `Wordsmith` class when it imports the project.

```gdscript
var rng = Wordsmith.seeded_random(5343)
var ship = Wordsmith.NauticalShipName.new()
print(ship.render(rng))
```

Use `Wordsmith.join(parts, separator)` to compose strings and components.
Subclass `Wordsmith.Component` and implement `render(rng) -> String` to supply
your own component. Pass the same source to each child. The
[ship example](examples/ship.gd) shows both uses.

Construct configurable generators with a dictionary. For example,
`Wordsmith.FantasyName.new({"syllable_count": 3})` builds a three-syllable
name generator. Use `Wordsmith.PersonName.new().from_hash(digest)` for the
same name across all three languages. See the [API mapping](../../spec/API.md).

When exporting, include the add-on scripts and every JSON word list. The
[example export preset](export_presets.cfg) includes the asset folder. Run
`python3 packages/gdscript/check.py` from the repository root to test the API,
install the ZIP in a clean project, and run the exported game. Set `GODOT`
to select an editor executable.
