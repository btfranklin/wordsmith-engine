extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")


class BandName extends Core.Component:
	func render(rng) -> String:
		return Core.one_of([
			Core.join(["The", Words.Adjective.new()], " "),
			Core.join(["The", Words.Noun.new()], " "),
			Core.join(["The", Words.Noun.new({"form": "plural"})], " "),
			Core.join([Words.Adjective.new(), Words.Noun.new()], " "),
			Core.join(["The", Words.Adjective.new(), Words.Noun.new({"form": "plural"})], " "),
			Core.join([
				Names.GivenName.new({"culture": "english_speaking"}),
				"and the",
				Words.Noun.new({"form": "plural"}),
			], " "),
			Core.join([
				Names.GivenName.new({"culture": "english_speaking"}).possessive_form(),
				Words.Noun.new({"form": "plural"}),
			], " "),
		]).title_case().render(rng)


class TownName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[9, Core.join([Names.Surname.new(), Core.one_of(["Bay", "Point", "City", "Park"])], " ")],
			[10, Core.join([Core.one_of(["Fort", "Port", "Cape"]), Names.Surname.new()], " ")],
			[
				5,
				Core.join([
					Names.Surname.new(),
					Core.one_of(["River", "Hill", "Town", "Beach", "Village"]),
				], " "),
			],
			[5, Core.join([Core.one_of(["Saint", "Mount", "Lake"]), Names.Surname.new()], " ")],
			[
				2,
				Core.join([
					"New",
					Core.concat([Names.Surname.new(), Core.one_of(["ton", "burg", "ville", "town", "dale"])]),
				], " "),
			],
			[
				4,
				Core.join([
					Words.LocationAdjective.new().first_upper(),
					Core.one_of(["Bay", "Point", "City", "Park"]),
				], " "),
			],
			[
				3,
				Core.join([
					Words.LocationAdjective.new().first_upper(),
					Core.one_of(["River", "Hill", "Town", "Beach", "Village"]),
				], " "),
			],
			[62, Core.concat([Names.Surname.new(), Core.one_of(["ton", "burg", "ville", "town", "dale"])])],
		]).render(rng)


class CriminalGangName extends Core.Component:
	func render(rng) -> String:
		if Core.random_boolean(rng, 0.25):
			return Core.join([
				Names.GivenName.new({"culture": "english_speaking"}).possessive_form(),
				Core.either(
					Words.VillainousPersonNoun.new({"is_plural": true}),
					Words.PrimitiveWeapon.new({"is_plural": true}),
				),
			], " ").title_case().render(rng)
		return Core.join([
			"the",
			Core.one_of([
				Core.join([
					Words.MartialSocialConcept.new(),
					Words.VillainousPersonNoun.new({"is_plural": true}),
				], " "),
				Core.join([
					Words.PrimitiveWeapon.new(),
					Words.VillainousPersonNoun.new({"is_plural": true}),
				], " "),
				Core.join([Words.VillainousPersonNoun.new({"is_plural": true}), "of", TownName.new()], " "),
				Core.join([TownName.new(), Words.VillainousPersonNoun.new({"is_plural": true})], " "),
				Core.join([Words.Adjective.new(), Words.VillainousPersonNoun.new({"is_plural": true})], " "),
				Core.join([
					Words.Adjective.new(),
					Words.VillainousPersonNoun.new({"is_plural": true}),
					"of",
					TownName.new(),
				], " "),
			]).title_case(),
		], " ").render(rng)
