extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const GroupsPlaces = preload("groups_places.gd")


class CompoundCreatureName extends Core.Component:
	func render(rng) -> String:
		return Core.concat([
			Words.NaturalNameRoot.new({"context": "creature"}),
			Words.BodyPart.new(),
		]).title_case().render(rng)


class BusinessName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[4, Core.join([Names.Surname.new(), "& Sons"], " ")],
			[
				3,
				Core.join([
					Words.BusinessColor.new(),
					Words.BusinessAnimal.new(),
					Words.BusinessTrade.new(),
				], " "),
			],
			[2, Core.join([GroupsPlaces.TownName.new(), Words.IndustrialTrade.new()], " ")],
			[1, Core.join([Names.Surname.new().possessive_form(), Words.ShopType.new()], " ")],
		]).title_case().render(rng)


class CelestialBodyName extends Core.Component:
	func render(rng) -> String:
		var synthetic_name = Names.FantasyName.new({
			"syllable_count": 3,
			"allow_hyphen": false,
			"allow_apostrophe": false,
		}).title_case()
		return Core.weighted_one_of([
			[4, synthetic_name],
			[
				3,
				Core.join([
					synthetic_name,
					Core.one_of(["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]),
				], " "),
			],
			[
				2,
				Core.join([
					Names.Surname.new().possessive_form(),
					Words.CelestialObjectType.new(),
				], " ").title_case(),
			],
			[
				1,
				Core.join([
					"The",
					Words.CelestialObjectType.new(),
					"of",
					Core.one_of(Core.asset("Celestial Name Parts").celestialConcepts),
				], " ").title_case(),
			],
		]).render(rng)


class CreatureName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[4, Core.join([CompoundCreatureName.new(), Words.CreatureType.new()], " ")],
			[
				3,
				Core.join([
					Core.one_of(Core.asset("Creature Name Parts").descriptors),
					Words.Habitat.new(),
					Words.WildAnimal.new(),
				], " "),
			],
			[
				2,
				Core.join([
					Core.one_of(Core.asset("Creature Name Parts").behaviorAdjectives),
					Words.CreatureType.new(),
				], " "),
			],
			[1, CompoundCreatureName.new()],
		]).title_case().render(rng)
