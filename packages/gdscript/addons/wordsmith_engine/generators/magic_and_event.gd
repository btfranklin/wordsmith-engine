extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const Words = preload("../words.gd")
const PlacesOrganizations = preload("places_organizations.gd")
const Materials = preload("materials.gd")
const GroupsPlaces = preload("groups_places.gd")


class ArtifactName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[4, Core.join(["The", Words.ArtifactObject.new(), "of", Words.MagicalConcept.new()], " ")],
			[3, Core.join([Names.Surname.new().possessive_form(), Words.ArtifactObject.new()], " ")],
			[2, Core.join([Materials.FictionalMineralName.new(), Words.PrimitiveWeapon.new()], " ")],
			[
				1,
				Core.join([
					"The",
					Words.ArtifactObject.new(),
					"of",
					PlacesOrganizations.LandmarkName.new(),
				], " "),
			],
		]).title_case().render(rng)


class SpellName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[4, Core.join([Words.SpellEffect.new(), "of", Words.MagicalConcept.new()], " ")],
			[
				3,
				Core.join([
					Names.Surname.new().possessive_form(),
					Core.one_of(Core.asset("Spell Name Parts").spellModifiers),
					Words.SpellEffect.new(),
				], " "),
			],
			[
				2,
				Core.join([
					Core.one_of(Core.asset("Spell Name Parts").spellCommands),
					"the",
					Core.one_of(Core.asset("Spell Name Parts").spellTargets),
				], " "),
			],
			[1, Core.join([Words.SpellEffect.new(), "of", Words.TimeOfDay.new()], " ")],
		]).title_case().render(rng)


class OperationName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				4,
				Core.join([
					"Operation",
					Core.one_of(Core.asset("Operation Name Parts").operationAdjectives),
					PlacesOrganizations.HeraldicSymbol.new(),
				], " "),
			],
			[3, Core.join(["Project", Words.OperationColor.new(), Words.WildAnimal.new()], " ")],
			[2, Core.join(["Operation", PlacesOrganizations.CompoundLandmarkName.new()], " ")],
			[1, Core.join([PlacesOrganizations.LandmarkName.new(), "Expedition"], " ")],
		]).title_case().render(rng)


class FestivalName extends Core.Component:
	func render(rng) -> String:
		return Core.weighted_one_of([
			[
				4,
				Core.join([
					"The",
					Core.one_of(Core.asset("Festival Name Parts").festivalTypes),
					"of",
					Core.one_of(Core.asset("Festival Name Parts").festivalThemes),
				], " "),
			],
			[
				3,
				Core.join([
					GroupsPlaces.TownName.new(),
					Words.Season.new(),
					Core.one_of(Core.asset("Festival Name Parts").festivalTypes),
				], " "),
			],
			[
				2,
				Core.join([
					Words.TimeOfDay.new(),
					Core.one_of(Core.asset("Festival Name Parts").festivalTypes),
				], " "),
			],
			[
				1,
				Core.concat([
					Words.OrganizationSymbol.new(),
					Core.one_of(Core.asset("Festival Name Parts").festivalSuffixes),
				]),
			],
		]).title_case().render(rng)
