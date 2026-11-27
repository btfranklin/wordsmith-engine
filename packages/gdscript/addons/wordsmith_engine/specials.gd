extends RefCounted

const Core := preload("core.gd")
const Words := preload("words.gd")


class ExoticCharacter:
	static func random_character(rng) -> String:
		var sets: Dictionary = Core.asset("Exotic Character Sets")
		return Core.choose(rng, sets[Core.choose(rng, sets.keys())])

	static func random_character_from_set(set_name: String, rng) -> String:
		var sets: Dictionary = Core.asset("Exotic Character Sets")
		if not sets.has(set_name):
			push_error("Unknown exotic character set: " + set_name)
			return ""
		return Core.choose(rng, sets[set_name])


class ReadableUniqueIdentifier:
	const REFERENCE_SECONDS := 978307200
	const DIGITS := "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	static func make_identifier(rng) -> String:
		var prefix := Core.either(
			Core.concat([Words.Adjective.new(), "_", Words.Noun.new()]),
			Core.concat([Words.Adverb.new(), "_", Words.Verb.new({"tense": Words.VerbTense.PRESENT_PERFECT})])
		).render(rng)
		var elapsed := int((Time.get_unix_time_from_system() - REFERENCE_SECONDS) * 1000000)
		var suffix := ""
		while elapsed > 0:
			suffix = DIGITS[elapsed % 36] + suffix
			@warning_ignore("integer_division")
			elapsed /= 36
		return prefix + "_" + suffix
