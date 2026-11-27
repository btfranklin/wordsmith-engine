extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const GroupsPlaces = preload("groups_places.gd")


class LiteraryTitleObject extends Core.Component:
	var plural: bool
	func _init(options: Dictionary = {}) -> void:
		plural = options.get("is_plural", false)

	func render(rng) -> String:
		var data = Core.asset("Literary Title Parts")
		return Core.choose(rng, data.pluralObjects if plural else data.objects)


class SentientLiteraryTitleObject extends Core.Component:
	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Literary Title Parts").sentientObjects)


class TitleQuality extends Core.Component:
	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Literary Title Parts").qualities)


class TitleAbstraction extends Core.Component:
	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Literary Title Parts").abstractions)


class AbstractSubject extends Core.Component:
	func render(rng) -> String:
		return Core.one_of([
			TitleAbstraction.new(),
			Words.UCBerkeleyEmotion.new(),
			Words.MartialSocialConcept.new(),
		]).render(rng)


class ResonantSubject extends Core.Component:
	func render(rng) -> String:
		return Core.one_of([
			LiteraryTitleObject.new({"is_plural": true}),
			AbstractSubject.new(),
			Names.PersonName.new({"culture": "english_speaking"}),
			GroupsPlaces.TownName.new(),
		]).render(rng)


class TitleNounPhrase extends Core.Component:
	var wrapped: Core.Component
	var requires_modifier: bool
	var modifier_probability: float
	func _init(value: Core.Component, options: Dictionary = {}) -> void:
		wrapped = value
		requires_modifier = options.get("requires_modifier", false)
		modifier_probability = options.get("modifier_probability", 0.45)

	func render(rng) -> String:
		var modifier = TitleQuality.new()
		var part = modifier if requires_modifier else Core.maybe([modifier], modifier_probability)
		return Core.join(["the", part, wrapped], " ").render(rng)


class TitleVerb extends Core.Component:
	var form: String
	func _init(options: Dictionary = {}) -> void:
		form = options.get("form", "finite")

	func render(rng) -> String:
		var row = Core.choose(rng, Core.asset("Literary Title Parts").verbs)
		return row[["base", "finite", "gerund"].find(form)]


class ImpossibleAction extends Core.Component:
	func render(rng) -> String:
		return Core.one_of([
			Core.join([
				TitleVerb.new({"form": "gerund"}),
				TitleNounPhrase.new(LiteraryTitleObject.new()),
			], " "),
			Core.join([TitleVerb.new({"form": "gerund"}), AbstractSubject.new()], " "),
			Core.join(["cataloging", LiteraryTitleObject.new({"is_plural": true})], " "),
			Core.join(["repairing", TitleNounPhrase.new(LiteraryTitleObject.new())], " "),
			Core.join([
				"teaching",
				TitleNounPhrase.new(SentientLiteraryTitleObject.new()),
				"to",
				TitleVerb.new({"form": "base"}),
			], " "),
		]).render(rng)


class PlaceSuffix extends Core.Component:
	func render(rng) -> String:
		return Core.choose(rng, Core.asset("Literary Title Parts").placeSuffixes)


class LiteraryTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[0.78, SimpleLiteraryTitle.new()],
			[0.22, UnusualLiteraryTitle.new()],
		]).render(rng)


class SimpleLiteraryTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[3, TitleNounPhrase.new(LiteraryTitleObject.new(), {"requires_modifier": true})],
			[
				2.5,
				Core.join([TitleNounPhrase.new(LiteraryTitleObject.new()), "of", ResonantSubject.new()], " "),
			],
			[
				2.5,
				Core.join([
					TitleNounPhrase.new(LiteraryTitleObject.new()),
					"at",
					GroupsPlaces.TownName.new(),
				], " "),
			],
			[2, Core.join([AbstractSubject.new(), "and", AbstractSubject.new()], " ")],
			[2, Core.join([AbstractSubject.new(), "in", GroupsPlaces.TownName.new()], " ")],
			[
				1.8,
				Core.join([
					TitleNounPhrase.new(Words.AuthoredArtifact.new()),
					"of",
					ResonantSubject.new(),
				], " "),
			],
			[
				1.5,
				Core.join([
					Names.PersonName.new({"culture": "english_speaking"}).possessive_form(),
					Words.AuthoredArtifact.new(),
				], " "),
			],
			[
				1.5,
				Core.join([
					Core.one_of([
						"a field guide to",
						"a history of",
						"a map of",
						"a study of",
						"an atlas of",
						"notes on",
						"the book of",
						"the grammar of",
					]),
					ResonantSubject.new(),
				], " "),
			],
			[1.2, Core.join([Words.TimeOfDay.new(), "with", ResonantSubject.new()], " ")],
			[
				1.2,
				Core.one_of([
					Core.join(["passage through", LiteraryTitleObject.new({"is_plural": true})], " "),
					Core.join(["the road to", AbstractSubject.new()], " "),
					Core.join(["the road to", GroupsPlaces.TownName.new()], " "),
					Core.join(["the voyage into", AbstractSubject.new()], " "),
					Core.join(["the voyage to", GroupsPlaces.TownName.new()], " "),
				]),
			],
			[1, Core.join([GroupsPlaces.TownName.new(), PlaceSuffix.new()], " ")],
		]).title_case().render(rng)


class UnusualLiteraryTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				2.4,
				Core.join([
					Core.one_of([
						"a manual for",
						"a recipe for",
						"instructions for",
						"rules for",
						"the practice of",
					]),
					ImpossibleAction.new(),
				], " "),
			],
			[
				2.2,
				Core.join([
					TitleNounPhrase.new(SentientLiteraryTitleObject.new()),
					"that",
					TitleVerb.new(),
				], " "),
			],
			[
				2,
				Core.join([
					TitleNounPhrase.new(LiteraryTitleObject.new()),
					"between",
					LiteraryTitleObject.new({"is_plural": true}),
				], " "),
			],
			[
				1.8,
				Core.join([
					Core.one_of(["after", "before", "if", "until", "when", "while"]),
					TitleNounPhrase.new(SentientLiteraryTitleObject.new()),
					TitleVerb.new(),
				], " "),
			],
			[
				1.6,
				Core.join([
					Core.one_of(["how", "why"]),
					TitleNounPhrase.new(SentientLiteraryTitleObject.new()),
					TitleVerb.new(),
				], " "),
			],
			[1.5, Core.join([AbstractSubject.new(), "after", AbstractSubject.new()], " ")],
			[1.4, Core.join([PlaceSuffix.new(), "for", ResonantSubject.new()], " ")],
			[
				1.2,
				Core.join([
					TitleNounPhrase.new(Words.AuthoredArtifact.new()),
					"against",
					AbstractSubject.new(),
				], " "),
			],
			[
				1,
				Core.join([
					TitleNounPhrase.new(LiteraryTitleObject.new()),
					"inside",
					TitleNounPhrase.new(LiteraryTitleObject.new()),
				], " "),
			],
		]).title_case().render(rng)
