extends RefCounted

const Core = preload("res://addons/wordsmith_engine/core.gd")
const Strings = preload("res://addons/wordsmith_engine/strings.gd")
const BinaryGender = {"MALE": "male", "FEMALE": "female"}
const GivenNameCulture = {
	"ENGLISH_SPEAKING": "english_speaking", "LATIN_AMERICAN": "latin_american", "EASTERN": "eastern",
}


class GivenName extends Core.Component:
	var _options: Dictionary
	var _valid := true

	func _init(options := {}) -> void:
		_options = options.duplicate(true)
		if options.has("gender") and options.gender not in BinaryGender.values():
			_valid = false
			push_error("Invalid binary gender.")
		if options.has("culture") and options.culture not in GivenNameCulture.values():
			_valid = false
			push_error("Invalid given name culture.")

	func render(rng) -> String:
		if not _valid:
			return ""
		var gender = _options.gender if _options.has("gender") else Core.choose(rng, BinaryGender.values())
		var culture = _options.culture if _options.has("culture") else Core.choose(rng, GivenNameCulture.values())
		return Core.choose(rng, Core.asset("Given Names").modern[culture][gender])


class AncientGivenName extends GivenName:
	func render(rng) -> String:
		if not _valid:
			return ""
		var gender = _options.gender if _options.has("gender") else Core.choose(rng, BinaryGender.values())
		return Core.choose(rng, Core.asset("Given Names").ancient[gender])


class Surname extends Core.Component:
	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Common Surnames"))


@abstract class SyntheticName extends Core.Component:
	var _count := 0
	var _allow_hyphen := true
	var _allow_apostrophe := true

	func _init(options: Dictionary) -> void:
		var count = options.get("syllable_count")
		if typeof(count) != TYPE_INT or count < 1:
			push_error("syllable_count must be a positive integer.")
			return
		if typeof(options.get("allow_hyphen", true)) != TYPE_BOOL or typeof(options.get("allow_apostrophe", true)) != TYPE_BOOL:
			push_error("Synthetic name punctuation options must be booleans.")
			return
		_count = count
		_allow_hyphen = options.get("allow_hyphen", true)
		_allow_apostrophe = options.get("allow_apostrophe", true)


class AlienName extends SyntheticName:
	func render(rng) -> String:
		if _count < 1:
			return ""
		var parts = Core.asset("Synthetic Name Parts").alien
		var hyphen := _count > 2 and _allow_hyphen and Core.random_boolean(rng)
		var apostrophe := _count > 2 and _allow_apostrophe and Core.random_boolean(rng)
		var hyphen_at := 1 + floori(Core.random_fraction(rng) * (_count - 1)) if hyphen else 0
		var apostrophe_at := 1 + floori(Core.random_fraction(rng) * (_count - 1)) if apostrophe else 0
		var text := ""
		for syllable in range(1, _count + 1):
			text += Core.choose(rng, parts.openEndedSyllables)
			if syllable == apostrophe_at:
				text += "'"
			elif syllable == hyphen_at:
				text += "-"
		if Core.random_boolean(rng):
			text += Core.choose(rng, parts.endingSounds)
		return Strings.first_upper(text)


class FantasyName extends SyntheticName:
	func render(rng) -> String:
		if _count < 1:
			return ""
		var parts = Core.asset("Synthetic Name Parts").fantasy
		var text: String = Core.choose(rng, parts.prefixes)
		for index in range(_count - 2):
			text += Core.choose(rng, parts.middles)
		if _count > 1:
			var compound := _count > 3 and Core.random_boolean(rng, 0.25)
			text += Core.choose(rng, parts.compoundEndings if compound else parts.endings)
		if _allow_hyphen and _count > 4 and Core.random_boolean(rng, 0.12):
			text = text.insert(2 + floori(Core.random_fraction(rng) * (text.length() - 4)), "-")
		if _allow_apostrophe and _count > 4 and Core.random_boolean(rng, 0.04):
			text = text.insert(2 + floori(Core.random_fraction(rng) * (text.length() - 4)), "'")
		return Strings.first_upper(text)


class PersonName extends GivenName:
	var _formats: Core.WeightedTable
	var _modifiers: Core.WeightedTable
	var _custom_modifiers: bool
	var _initial_letter := RegEx.create_from_string("\\p{L}")

	func _init(options := {}) -> void:
		super(options)
		if not _valid:
			return
		var styles = Core.asset("Person Name Styles")
		var varied: bool = options.get("style") == "varied"
		_valid = options.get("style", "plain") in ["plain", "varied"]
		_valid = _valid and typeof(options.get("initial_period", true)) == TYPE_BOOL
		for key in ["initial_separator", "generation_separator", "credential_separator"]:
			_valid = _valid and typeof(options.get(key, "")) == TYPE_STRING
		_valid = _valid and _valid_modifiers(options)
		if options.has("given_name_format"):
			_valid = _valid and _valid_format(options.given_name_format)
		if options.has("format_weights") or varied:
			_formats = _compile_table(_options.get("format_weights", styles.formats), true, true)
			_valid = _valid and _formats != null
		_custom_modifiers = options.has("modifier_weights")
		if _custom_modifiers or varied:
			_modifiers = _compile_table(_options.get("modifier_weights", styles.modifiers), false, _custom_modifiers)
			_valid = _valid and _modifiers != null
		if not _valid:
			push_error("Invalid PersonName configuration.")

	static func _compile_table(pairs, formats: bool, custom: bool) -> Core.WeightedTable:
		if not pairs is Array:
			return null
		for pair in pairs:
			if not pair is Array or pair.size() != 2:
				return null
			if formats and not _valid_format(pair[1]):
				return null
			if not formats and custom and not _valid_modifiers(pair[1]):
				return null
		return Core.WeightedTable.create(pairs)

	static func _valid_format(parts) -> bool:
		if not parts is Array or parts.is_empty():
			return false
		for part in parts:
			if part not in ["full", "initial"]:
				return false
		return true

	static func _valid_modifiers(values) -> bool:
		if not values is Dictionary or not values.get("credentials", []) is Array:
			return false
		for key in ["prefix", "generation"]:
			if not values.get(key, "") is String:
				return false
		for credential in values.get("credentials", []):
			if not credential is String or credential.strip_edges().is_empty():
				return false
		return true

	func render(rng) -> String:
		if not _valid:
			return ""
		return _name(func(_label): return Core.random_fraction(rng))

	func from_hash(digest: String) -> String:
		if not _valid:
			return ""
		if (digest.length() != 64 or not digest.is_valid_hex_number(false)
				or digest.begins_with("+") or digest.begins_with("-")):
			push_error("Expected a 64-character hexadecimal SHA-256 digest.")
			return ""
		var prefix := digest.hex_decode()
		prefix.append(0)
		return _name(func(label): return _hash_fraction(prefix, label))

	static func _hash_fraction(prefix: PackedByteArray, label: String) -> float:
		var hash_context := HashingContext.new()
		hash_context.start(HashingContext.HASH_SHA256)
		hash_context.update(prefix)
		hash_context.update(label.to_utf8_buffer())
		var bytes := hash_context.finish()
		var sample := (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3]
		return sample / 4294967296.0

	static func _pick(draw: Callable, label: String, values: Array):
		return values[floori(draw.call(label) * values.size())]

	func _name(draw: Callable) -> String:
		var parts: Array = _options.get("given_name_format", ["full"])
		if not _options.has("given_name_format") and _formats:
			parts = _formats.pick(draw.call("format"))
		var gender = _options.gender if _options.has("gender") else _pick(draw, "gender", BinaryGender.values())
		var culture = _options.culture if _options.has("culture") else _pick(draw, "culture", GivenNameCulture.values())
		var names = Core.asset("Given Names").modern[culture][gender]
		var text := ""
		for index in parts.size():
			var name_part: String = _pick(draw, "given.%d" % index, names)
			if index > 0:
				var adjacent_initials: bool = parts[index] == "initial" and parts[index - 1] == "initial"
				text += _options.get("initial_separator", "") if adjacent_initials else " "
			if parts[index] == "initial":
				name_part = _initial_letter.search(name_part).get_string().to_upper()
				if _options.get("initial_period", true):
					name_part += "."
			text += name_part
		text += " " + _pick(draw, "surname", Core.asset("Common Surnames"))
		var modifiers := _selected_modifiers(draw)
		var prefix: String = _options.get("prefix", modifiers.get("prefix", ""))
		var suffix: String = _options.get("generation", modifiers.get("generation", ""))
		if not prefix.is_empty():
			text = prefix + " " + text
		if not suffix.is_empty():
			text += _options.get("generation_separator", " ") + suffix
		for credential in _options.get("credentials", modifiers.get("credentials", [])):
			text += _options.get("credential_separator", ", ") + credential
		return text

	func _selected_modifiers(draw: Callable) -> Dictionary:
		if not _modifiers or _options.has_all(["prefix", "generation", "credentials"]):
			return {}
		var option = _modifiers.pick(draw.call("modifier"))
		if _custom_modifiers:
			return option
		if _options.has(option):
			return {}
		var styles = Core.asset("Person Name Styles")
		match option:
			"prefix":
				return {"prefix": _pick(draw, "title", styles.titles)}
			"generation":
				return {"generation": _pick(draw, "generation", styles.generations)}
			"credentials":
				return {"credentials": [_pick(draw, "credential", styles.credentials)]}
		return {}
