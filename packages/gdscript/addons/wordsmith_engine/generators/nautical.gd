extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const GroupsPlaces = preload("groups_places.gd")


class NauticalShipName extends Core.Component:
	func render(rng) -> String:
		var possessive_name = Core.join([
			Core.either(
				Words.MartialSocialConcept.new().first_upper(),
				Core.either(
					Names.GivenName.new({"gender": "female", "culture": "english_speaking"}),
					Names.GivenName.new({"gender": "male", "culture": "english_speaking"}),
					0.75,
				),
				0.33,
			).possessive_form(),
			Core.either(
				Core.either(Words.NauticalShipNameObject.new(), Words.PrimitiveWeapon.new()),
				Words.MartialSocialConcept.new(),
			),
		], " ")
		return Core.weighted_one_of([
			[4, Names.GivenName.new({"gender": "female", "culture": "english_speaking"})],
			[3, Words.MartialSocialConcept.new()],
			[1, GroupsPlaces.TownName.new()],
			[
				1,
				Core.either(
					Names.AncientGivenName.new({"gender": "female"}),
					Names.FantasyName.new({"syllable_count": 3}),
				),
			],
			[1, Words.NauticalShipNameObject.new()],
			[1, Words.ShipNameAdjective.new()],
			[
				1,
				Core.join([
					Words.NauticalShipNameColor.new(),
					Core.either(Words.NauticalShipNameObject.new(), Words.PrimitiveWeapon.new(), 0.75),
				], " "),
			],
			[
				2,
				Core.join([
					Words.ShipNameAdjective.new(),
					Core.either(Words.NauticalShipNameObject.new(), Words.PrimitiveWeapon.new(), 0.85),
				], " "),
			],
			[
				1,
				Core.join([
					Words.TimeOfDay.new(),
					Core.either(Words.MartialSocialConcept.new(), Words.PrimitiveWeapon.new(), 0.75),
				], " "),
			],
			[
				1,
				Core.join([
					GroupsPlaces.TownName.new(),
					Core.either(Words.NauticalShipNameObject.new(), Words.PrimitiveWeapon.new(), 0.85),
				], " "),
			],
			[
				1,
				Core.join([
					Core.either(Words.NauticalShipNameObject.new(), Words.PrimitiveWeapon.new()),
					"of",
					Core.either(Words.MartialSocialConcept.new(), GroupsPlaces.TownName.new()),
				], " "),
			],
			[1, possessive_name],
		]).title_case().render(rng)
