extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const GroupsPlaces = preload("groups_places.gd")


class HeraldicSymbol extends Core.Component:
	func render(rng) -> String:
		return Core.one_of([Words.TavernAnimal.new(), Words.TavernObject.new()]).render(rng)


class CompoundLandmarkName extends Core.Component:
	func render(rng) -> String:
		return Core.concat([
			Words.NaturalNameRoot.new({"context": "landmark"}),
			Core.one_of(Core.asset("Place and Organization Parts").landmarkSuffixes),
		]).title_case().render(rng)


class TavernName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				4,
				Core.join([
					"The",
					Core.one_of(Core.asset("Place and Organization Parts").tavernAdjectives),
					HeraldicSymbol.new(),
				], " "),
			],
			[3, Core.join(["The", Words.TavernAnimal.new(), "and", Words.TavernObject.new()], " ")],
			[
				2,
				Core.join([
					Names.GivenName.new({"culture": "english_speaking"}).possessive_form(),
					Core.one_of(Core.asset("Place and Organization Parts").tavernEndings),
				], " "),
			],
			[1, Core.join([GroupsPlaces.TownName.new(), Core.one_of(["Inn", "Tavern", "Lodge"])], " ")],
		]).title_case().render(rng)


class LandmarkName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[4, Core.join([Words.LandmarkAdjective.new(), Words.LandmarkFeature.new()], " ")],
			[3, CompoundLandmarkName.new()],
			[2, Core.join([Names.Surname.new().possessive_form(), Words.LandmarkFeature.new()], " ")],
			[
				1,
				Core.join([
					"The",
					Words.LandmarkAdjective.new(),
					Core.one_of(Core.asset("Place and Organization Parts").landmarkPluralFeatures),
				], " "),
			],
		]).title_case().render(rng)


class OrganizationName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				4,
				Core.join([
					"The Order of the",
					Core.one_of(Core.asset("Place and Organization Parts").organizationAdjectives),
					Words.OrganizationSymbol.new(),
				], " "),
			],
			[
				3,
				Core.join([
					GroupsPlaces.TownName.new(),
					Words.GuildTrade.new().possessive_form(),
					"Guild",
				], " "),
			],
			[
				2,
				Core.join([
					"The",
					Core.one_of(Core.asset("Place and Organization Parts").organizationAdjectives),
					Core.one_of(Core.asset("Place and Organization Parts").organizationTypes),
				], " "),
			],
			[
				1,
				Core.join([
					"The Society of",
					Core.one_of(Core.asset("Place and Organization Parts").organizationConcepts),
				], " "),
			],
		]).title_case().render(rng)
