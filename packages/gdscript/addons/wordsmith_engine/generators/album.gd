extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const GroupsPlaces = preload("groups_places.gd")


class ShortAlbumTitle extends Core.Component:
	func render(rng) -> String:
		var form = Core.choose(rng, ["singular", "plural"])
		return Core.weighted_one_of([
			[2, Words.Noun.new({"form": "plural"})],
			[2, Core.join([Words.Adjective.new(), Words.Noun.new({"form": form})], " ")],
			[1.4, Core.join([Words.TimeOfDay.new(), Words.Noun.new({"form": "plural"})], " ")],
			[1.2, Words.UCBerkeleyEmotion.new()],
			[1.2, Words.MartialSocialConcept.new()],
			[1, Words.AuthoredArtifact.new()],
		]).title_case().render(rng)


class FragmentAlbumTitle extends Core.Component:
	func render(rng) -> String:
		var form = Core.choose(rng, ["singular", "plural"])
		return Core.weighted_one_of([
			[
				1.8,
				Core.join([
					Core.one_of(["no", "new", "old", "last", "first"]),
					Words.Noun.new({"form": form}),
				], " "),
			],
			[1.6, Core.join([Words.TimeOfDay.new(), "with", Words.Noun.new({"form": "plural"})], " ")],
			[1.4, Core.join([Words.Noun.new(), "for", Words.Noun.new({"form": "plural"})], " ")],
			[
				1.2,
				Core.join([
					Words.UCBerkeleyEmotion.new(),
					"for",
					Names.PersonName.new({"culture": "english_speaking"}),
				], " "),
			],
			[1, Core.join([Words.Verb.new({"tense": "base"}), "the", Words.Noun.new()], " ")],
		]).title_case().render(rng)


class DocumentaryAlbumTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[2, Core.join([GroupsPlaces.TownName.new(), Core.one_of(["sessions", "recordings"])], " ")],
			[
				1.6,
				Core.join([
					Names.PersonName.new({"culture": "english_speaking"}).possessive_form(),
					Words.AuthoredArtifact.new(),
				], " "),
			],
			[1.4, Core.join([Words.AuthoredArtifact.new(), "from", GroupsPlaces.TownName.new()], " ")],
			[
				1.4,
				Core.join([
					Core.one_of(["songs for", "music for"]),
					Core.one_of([
						Words.Noun.new({"form": "plural"}),
						Words.UCBerkeleyEmotion.new(),
						Words.MartialSocialConcept.new(),
					]),
				], " "),
			],
			[1, Core.join([Words.TimeOfDay.new(), Core.one_of(["sessions", "recordings"])], " ")],
		]).title_case().render(rng)


class CollisionAlbumTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[1.8, Core.concat([Words.Noun.new(), " / ", Words.Noun.new()])],
			[1.6, Core.join([Words.Noun.new(), "and", Words.Noun.new({"form": "plural"})], " ")],
			[1.4, Core.join([Words.Adjective.new(), "and", Words.Adjective.new()], " ")],
			[1.2, Core.join([Words.UCBerkeleyEmotion.new(), "and", Words.Noun.new({"form": "plural"})], " ")],
			[1, Core.join([Words.MartialSocialConcept.new(), "/", Words.UCBerkeleyEmotion.new()], " ")],
		]).title_case().render(rng)


class AlbumTitle extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[0.35, ShortAlbumTitle.new()],
			[0.25, FragmentAlbumTitle.new()],
			[0.22, DocumentaryAlbumTitle.new()],
			[0.18, CollisionAlbumTitle.new()],
		]).render(rng)
