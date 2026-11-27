extends SceneTree

const Strings = preload("res://addons/wordsmith_engine/strings.gd")
const PersonCases = preload("res://tests/person_names.gd")

var failures: Array[String] = []
var fixture_dir: String
var api: Script = Wordsmith


class ScriptedRandom extends Wordsmith.RandomSource:
	var row: Dictionary
	var draws := 0

	func _init(trace: Dictionary) -> void:
		row = trace

	func random() -> float:
		var index := draws
		draws += 1
		var values: Array = row.get("fractions", [])
		if row.get("cycle", false):
			return values[index % values.size()]
		return values[index] if index < values.size() else row.get("repeat", 0)


func check(actual: Variant, expected: Variant, label: String) -> void:
	if actual != expected:
		failures.append("%s: got %s, expected %s" % [label, actual, expected])


func sequence_part(part, order: Array, source):
	if part is String:
		return part
	match part.kind:
		"empty":
			return Wordsmith.empty()
		"sequence":
			var parts := []
			for child in part.parts:
				parts.append(sequence_part(child, order, source))
			return Wordsmith.join(parts, part.separator)
		"probe":
			return Wordsmith.component(func(rng):
				check(rng, source, part.label)
				order.append(part.label)
				rng.random()
				return part.text)
		_:
			failures.append("Unknown sequence part: %s" % part)
			return null


func sequences(rows: Array) -> void:
	for row in rows:
		var rng := ScriptedRandom.new({})
		var order := []
		var parts := []
		for part in row.parts:
			parts.append(sequence_part(part, order, rng))
		var sequence = Wordsmith.join(parts, row.separator)
		check(order.size(), 0, row.name)
		if row.has("mutationAfterConstruction"):
			var change = row.mutationAfterConstruction
			parts[int(change.index)] = change.replacement
		check(sequence.render(rng), row.expected, row.name)
		check(order, row.get("expectedRenderOrder", []), row.name)
		check(rng.draws, row.get("expectedRandomDraws", 0), row.name)


func weights(rows: Array) -> void:
	var special := {"NaN": NAN, "Infinity": INF, "-Infinity": -INF}
	for row in rows:
		var pairs := []
		for weight in row.weights:
			pairs.append([special.get(weight, weight), "ok"])
		var value = Wordsmith.weighted_one_of(pairs)
		check(value != null, row.accepted, row.name)
		if value != null:
			check(value.render(ScriptedRandom.new({})), "ok", row.name)


func traces(rows: Array) -> void:
	for row in rows:
		var rng := ScriptedRandom.new(row)
		var generator = api.get_script_constant_map()[row.generator]
		var options := {}
		for key: String in row.get("configuration", {}):
			var value = row.configuration[key]
			options[key.to_snake_case()] = int(value) if key == "syllableCount" else value
		var component = generator.new(options) if not options.is_empty() else generator.new()
		check(component.render(rng), row.expected, row.name)
		check(rng.draws, row.expectedDraws, row.name)


func transforms(data: Dictionary) -> void:
	for method: String in data:
		for row in data[method]:
			var actual
			if method == "startsWithVowel":
				actual = Strings.starts_with_vowel(row.input)
			else:
				actual = Wordsmith.literal(row.input).call(method.to_snake_case()).render(ScriptedRandom.new({}))
			check(actual, row.expected, "%s(%s)" % [method, row.input])


func decode_numbers(value: Variant) -> Variant:
	if value is Dictionary:
		if value.has("binary64"):
			return value.binary64.hex_decode().decode_double(0)
		for key in value:
			value[key] = decode_numbers(value[key])
	elif value is Array:
		for i in value.size():
			value[i] = decode_numbers(value[i])
	return value


func _initialize() -> void:
	fixture_dir = OS.get_cmdline_user_args()[0]
	for filename in DirAccess.get_files_at(fixture_dir):
		var data = decode_numbers(JSON.parse_string(FileAccess.get_file_as_string(fixture_dir.path_join(filename))))
		match filename:
			"component-sequences.json": sequences(data.cases)
			"generator-traces.json": traces(data.cases)
			"weighted-choices.json": weights(data.cases)
			"string-transforms.json": transforms(data)
			"person-names.json": failures.append_array(PersonCases.run(data))
			"public-api.json":
				for symbol: String in data.gdscriptRuntime:
					check(api.get_script_constant_map().has(symbol) or api.has_method(symbol), true, symbol)
			_: failures.append("Unknown fixture file: %s" % filename)
	if failures.is_empty():
		print("Wordsmith conformance passed")
	else:
		for failure in failures:
			printerr(failure)
	quit(0 if failures.is_empty() else 1)
