extends RefCounted

const Names = preload("res://addons/wordsmith_engine/names.gd")


class Draws:
	var fractions: Array
	var consumed := 0

	func _init(values: Array) -> void:
		fractions = values

	func random() -> float:
		consumed += 1
		return fractions[consumed - 1] if consumed <= fractions.size() else 0.0


static func _options(configuration: Dictionary) -> Dictionary:
	var options := {}
	for key in configuration:
		options[key.to_snake_case()] = configuration[key]
	return options


static func run(cases: Dictionary) -> Array[String]:
	var failures: Array[String] = []
	for case in cases.draws:
		var rng := Draws.new(case.fractions)
		var person := Names.PersonName.new(_options(case.configuration))
		var actual := person.render(rng)
		if actual != case.expected or rng.consumed != case.fractions.size():
			failures.append("%s: got '%s' in %d draws" % [case.name, actual, rng.consumed])
	for case in cases.hashes:
		var person := Names.PersonName.new(_options(case.configuration))
		if person.from_hash(case.digest) != case.expected:
			failures.append("PersonName.from_hash failed for %s" % case.digest)
	var credentials := ["PhD."]
	var parts := ["full"]
	var weights := [[1, parts]]
	var saved := Names.PersonName.new({"credentials": credentials, "format_weights": weights})
	credentials.clear()
	parts.clear()
	weights.clear()
	if saved.from_hash("0".repeat(64)) != "Kandi Santos, PhD.":
		failures.append("PersonName did not snapshot its options.")
	var plain := Names.PersonName.new()
	if plain.from_hash("FF".repeat(32)) != plain.from_hash("ff".repeat(32)):
		failures.append("PersonName digest depends on letter case.")
	return failures
