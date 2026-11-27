extends RefCounted

const Core = preload("res://addons/wordsmith_engine/core.gd")

const NounForm = {"SINGULAR": "singular", "PLURAL": "plural"}
const VerbTense = {
	"BASE": "base", "PAST": "past", "PAST_PARTICIPLE": "pastParticiple",
	"PRESENT": "present", "PRESENT_PERFECT": "presentPerfect",
}


class Vocabulary extends Core.Component:
	var _asset_name: String
	var _key: String

	func _init(asset_name: String, key := "") -> void:
		_asset_name = asset_name
		_key = key

	func render(rng) -> String:
		var data = Core.asset(_asset_name)
		return Core.choose(rng, data if _key.is_empty() else data[_key])


class Adjective extends Vocabulary:
	func _init() -> void:
		super("Adjectives")


class Adverb extends Vocabulary:
	func _init() -> void:
		super("Adverbs")


class ChemicalCompoundName extends Vocabulary:
	func _init() -> void:
		super("Chemical Compound Names")


class AuthoredArtifact extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "authoredArtifacts")


class LocationAdjective extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "locationAdjectives")


class TavernAnimal extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "animals")


class TavernObject extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "tavernObjects")


class BusinessAnimal extends Vocabulary:
	func _init() -> void:
		super("Business Name Parts", "animals")


class WildAnimal extends Vocabulary:
	func _init() -> void:
		super("Creature Name Parts", "animals")


class BusinessColor extends Vocabulary:
	func _init() -> void:
		super("Business Name Parts", "colors")


class LandmarkAdjective extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "landmarkAdjectives")


class LandmarkFeature extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "landmarkFeatures")


class Habitat extends Vocabulary:
	func _init() -> void:
		super("Creature Name Parts", "habitats")


class BodyPart extends Vocabulary:
	func _init() -> void:
		super("Creature Name Parts", "bodyParts")


class CreatureType extends Vocabulary:
	func _init() -> void:
		super("Creature Name Parts", "creatureTypes")


class GuildTrade extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "tradesPlural")


class BusinessTrade extends Vocabulary:
	func _init() -> void:
		super("Business Name Parts", "trades")


class IndustrialTrade extends Vocabulary:
	func _init() -> void:
		super("Business Name Parts", "industrialTrades")


class ShopType extends Vocabulary:
	func _init() -> void:
		super("Business Name Parts", "shopTypes")


class CelestialObjectType extends Vocabulary:
	func _init() -> void:
		super("Celestial Name Parts", "celestialObjects")


class OrganizationSymbol extends Vocabulary:
	func _init() -> void:
		super("Place and Organization Parts", "organizationSymbols")


class ArtifactObject extends Vocabulary:
	func _init() -> void:
		super("Artifact Objects")


class SpellEffect extends Vocabulary:
	func _init() -> void:
		super("Spell Effects")


class MagicalConcept extends Vocabulary:
	func _init() -> void:
		super("Magical Concepts")


class OperationColor extends Vocabulary:
	func _init() -> void:
		super("Operation Colors")


class Season extends Vocabulary:
	func _init() -> void:
		super("Seasons")


class MartialSocialConcept extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "martialSocialConcepts")


class UCBerkeleyEmotion extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "ucBerkeleyEmotions")


class NauticalShipNameObject extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "nauticalShipNameObjects")


class NauticalShipNameColor extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "nauticalShipNameColors")


class ShipNameAdjective extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "shipNameAdjectives")


class TimeOfDay extends Vocabulary:
	func _init() -> void:
		super("Curated Word Lists", "timesOfDay")


class NaturalNameRoot extends Core.Component:
	var _context: String

	func _init(options: Dictionary) -> void:
		if options.get("context") in ["landmark", "creature"]:
			_context = options.context
		else:
			push_error("NaturalNameRoot requires landmark or creature.")

	func render(rng) -> String:
		match _context:
			"landmark":
				return Core.choose(rng, Core.asset("Place and Organization Parts").landmarkRoots)
			"creature":
				return Core.choose(rng, Core.asset("Creature Name Parts").appearanceRoots)
		return ""


class Noun extends Core.Component:
	var _index: int

	func _init(options := {}) -> void:
		_index = ["singular", "plural"].find(options.get("form", "singular"))
		if _index < 0:
			push_error("Invalid noun form.")

	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Nouns"))[_index] if _index >= 0 else ""


class Verb extends Core.Component:
	var _index: int

	func _init(options := {}) -> void:
		_index = VerbTense.values().find(options.get("tense", "base"))
		if _index < 0:
			push_error("Invalid verb tense.")

	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Verbs"))[_index] if _index >= 0 else ""


class Pronoun extends Core.Component:
	var _choices: Array
	var _fixed := ""

	func _init(options: Dictionary) -> void:
		if typeof(options.get("is_singular")) != TYPE_BOOL or typeof(options.get("is_third_person")) != TYPE_BOOL:
			push_error("Pronoun requires boolean is_singular and is_third_person.")
		elif options.is_third_person:
			if options.is_singular:
				_choices = ["he", "she", "it"]
			else:
				_fixed = "they"
		else:
			_choices = ["I", "you"] if options.is_singular else ["we", "you"]

	func render(rng) -> String:
		return _fixed if _choices.is_empty() else Core.choose(rng, _choices)


class Article extends Core.Component:
	var _before_vowel

	func _init(options := {}) -> void:
		_before_vowel = options.get("is_before_vowel", false)
		if typeof(_before_vowel) != TYPE_BOOL:
			push_error("is_before_vowel must be a boolean.")

	func render(rng) -> String:
		return Core.select_article(rng, _before_vowel) if typeof(_before_vowel) == TYPE_BOOL else ""


class Determiner extends Article:
	func render(rng) -> String:
		return Core.select_determiner(rng, _before_vowel) if typeof(_before_vowel) == TYPE_BOOL else ""


class VillainousPersonNoun extends Core.Component:
	var _plural

	func _init(options: Dictionary) -> void:
		_plural = options.get("is_plural")
		if typeof(_plural) != TYPE_BOOL:
			push_error("VillainousPersonNoun requires boolean is_plural.")

	func render(rng) -> String:
		if typeof(_plural) != TYPE_BOOL:
			return ""
		var word: String = Core.choose(rng, Core.asset("Curated Word Lists").villainousPersonNouns)
		if not _plural:
			return word
		if word.ends_with("y"):
			return word + "s" if word[-2] in "aeiou" else word.left(-1) + "ies"
		for ending in ["x", "ss", "sh", "ch"]:
			if word.ends_with(ending):
				return word + "es"
		if word.ends_with("ife") and word != "lowlife":
			return word.left(-2) + "ves"
		if word.ends_with("rf") or word.ends_with("ief"):
			return word.left(-1) + "ves"
		if word.ends_with("man"):
			return word.left(-2) + "en"
		return word if word.ends_with("s") else word + "s"


class PrimitiveWeapon extends Core.Component:
	var _plural

	func _init(options := {}) -> void:
		_plural = options.get("is_plural", false)
		if typeof(_plural) != TYPE_BOOL:
			push_error("is_plural must be a boolean.")

	func render(rng) -> String:
		if typeof(_plural) != TYPE_BOOL:
			return ""
		var word: String = Core.choose(rng, Core.asset("Curated Word Lists").primitiveWeapons)
		if not _plural:
			return word
		return word.left(-2) + "ves" if word.ends_with("ife") else word + "s"
