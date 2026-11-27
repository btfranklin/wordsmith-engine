extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const Literary = preload("literary.gd")
const GroupsPlaces = preload("groups_places.gd")


class SimpleMovieTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[2, Names.PersonName.new({"culture": "english_speaking"})],
			[1.8, GroupsPlaces.TownName.new()],
			[1.7, Core.join(["the", Words.Adjective.new(), Words.Noun.new()], " ")],
			[1.7, Core.join(["the", Words.Noun.new(), "of", GroupsPlaces.TownName.new()], " ")],
			[1.5, Core.join([Words.TimeOfDay.new(), "in", GroupsPlaces.TownName.new()], " ")],
			[1.4, Core.join([Words.MartialSocialConcept.new(), "at", GroupsPlaces.TownName.new()], " ")],
			[1.3, Core.join([Words.UCBerkeleyEmotion.new(), "and", Words.MartialSocialConcept.new()], " ")],
			[
				1.2,
				Core.join([
					Names.PersonName.new({"culture": "english_speaking"}).possessive_form(),
					Words.AuthoredArtifact.new(),
				], " "),
			],
			[
				1,
				Core.join([
					"the",
					Words.AuthoredArtifact.new(),
					"of",
					Names.PersonName.new({"culture": "english_speaking"}),
				], " "),
			],
		]).title_case().render(rng)


class HighConceptMovieTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				2.2,
				Core.join([
					Core.one_of(["escape from", "return to", "the fall of", "the last days of"]),
					GroupsPlaces.TownName.new(),
				], " "),
			],
			[
				1.8,
				Core.join([
					Core.one_of(["before", "after", "when"]),
					Words.Noun.new().prefixed_by_article(),
					Words.Verb.new({"tense": "present"}),
				], " "),
			],
			[
				1.6,
				Core.join([
					Core.one_of(["before", "after", "when"]),
					Names.PersonName.new({"culture": "english_speaking"}),
					Words.Verb.new({"tense": "present"}),
				], " "),
			],
			[
				1.4,
				Core.join([
					"the",
					Core.one_of(["case", "secret", "trial", "shadow"]),
					"of",
					GroupsPlaces.TownName.new(),
				], " "),
			],
			[
				1.2,
				Core.join([
					"the",
					Core.one_of(["first", "last", "final"]),
					Core.one_of([Words.AuthoredArtifact.new(), Words.Noun.new()]),
				], " "),
			],
			[1, Core.join(["the", Words.Noun.new(), "that", Words.Verb.new({"tense": "past"})], " ")],
		]).title_case().render(rng)


class MovieTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[0.55, SimpleMovieTitle.new()],
			[0.3, HighConceptMovieTitle.new()],
			[0.15, Literary.LiteraryTitle.new()],
		]).render(rng)
