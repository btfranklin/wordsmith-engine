class_name Wordsmith
extends RefCounted

const _Core = preload("core.gd")
const Component = _Core.Component
const RandomSource = _Core.RandomSource

const _Words = preload("words.gd")
const Adjective = _Words.Adjective
const Adverb = _Words.Adverb
const Article = _Words.Article
const ArtifactObject = _Words.ArtifactObject
const AuthoredArtifact = _Words.AuthoredArtifact
const BodyPart = _Words.BodyPart
const BusinessAnimal = _Words.BusinessAnimal
const BusinessColor = _Words.BusinessColor
const BusinessTrade = _Words.BusinessTrade
const CelestialObjectType = _Words.CelestialObjectType
const ChemicalCompoundName = _Words.ChemicalCompoundName
const CreatureType = _Words.CreatureType
const Determiner = _Words.Determiner
const GuildTrade = _Words.GuildTrade
const Habitat = _Words.Habitat
const IndustrialTrade = _Words.IndustrialTrade
const LandmarkAdjective = _Words.LandmarkAdjective
const LandmarkFeature = _Words.LandmarkFeature
const LocationAdjective = _Words.LocationAdjective
const MagicalConcept = _Words.MagicalConcept
const MartialSocialConcept = _Words.MartialSocialConcept
const NaturalNameRoot = _Words.NaturalNameRoot
const NauticalShipNameColor = _Words.NauticalShipNameColor
const NauticalShipNameObject = _Words.NauticalShipNameObject
const Noun = _Words.Noun
const NounForm = _Words.NounForm
const OperationColor = _Words.OperationColor
const OrganizationSymbol = _Words.OrganizationSymbol
const PrimitiveWeapon = _Words.PrimitiveWeapon
const Pronoun = _Words.Pronoun
const Season = _Words.Season
const ShipNameAdjective = _Words.ShipNameAdjective
const ShopType = _Words.ShopType
const SpellEffect = _Words.SpellEffect
const TavernAnimal = _Words.TavernAnimal
const TavernObject = _Words.TavernObject
const TimeOfDay = _Words.TimeOfDay
const UCBerkeleyEmotion = _Words.UCBerkeleyEmotion
const Verb = _Words.Verb
const VerbTense = _Words.VerbTense
const VillainousPersonNoun = _Words.VillainousPersonNoun
const WildAnimal = _Words.WildAnimal

const _Names = preload("names.gd")
const AlienName = _Names.AlienName
const AncientGivenName = _Names.AncientGivenName
const BinaryGender = _Names.BinaryGender
const FantasyName = _Names.FantasyName
const GivenName = _Names.GivenName
const GivenNameCulture = _Names.GivenNameCulture
const PersonName = _Names.PersonName
const Surname = _Names.Surname

const _Generators = preload("generators.gd")
const AlbumTitle = _Generators.AlbumTitle
const ArtifactName = _Generators.ArtifactName
const BandName = _Generators.BandName
const BusinessName = _Generators.BusinessName
const CelestialBodyName = _Generators.CelestialBodyName
const CompoundCreatureName = _Generators.CompoundCreatureName
const CompoundLandmarkName = _Generators.CompoundLandmarkName
const CreatureName = _Generators.CreatureName
const CriminalGangName = _Generators.CriminalGangName
const FestivalName = _Generators.FestivalName
const FictionalElementName = _Generators.FictionalElementName
const FictionalMineralName = _Generators.FictionalMineralName
const HeraldicSymbol = _Generators.HeraldicSymbol
const HighConceptMovieTitle = _Generators.HighConceptMovieTitle
const LandmarkName = _Generators.LandmarkName
const LiteraryTitle = _Generators.LiteraryTitle
const MovieTitle = _Generators.MovieTitle
const NauticalShipName = _Generators.NauticalShipName
const OperationName = _Generators.OperationName
const OrganizationName = _Generators.OrganizationName
const SimpleLiteraryTitle = _Generators.SimpleLiteraryTitle
const SimpleMovieTitle = _Generators.SimpleMovieTitle
const SpellName = _Generators.SpellName
const TavernName = _Generators.TavernName
const TownName = _Generators.TownName
const UnusualLiteraryTitle = _Generators.UnusualLiteraryTitle

const _Specials = preload("specials.gd")
const ExoticCharacter = _Specials.ExoticCharacter
const ReadableUniqueIdentifier = _Specials.ReadableUniqueIdentifier


static func seeded_random(value: int) -> RandomSource:
	return _Core.seeded_random(value)


static func component(callback: Callable) -> Component:
	return _Core.component(callback)


static func literal(value: String) -> Component:
	return _Core.literal(value)


static func empty() -> Component:
	return _Core.empty()


static func join(values: Array, separator: String) -> Component:
	return _Core.join(values, separator)


static func concat(parts: Array) -> Component:
	return _Core.concat(parts)


static func one_of(values: Array) -> Component:
	return _Core.one_of(values)


static func weighted_one_of(pairs: Array) -> Component:
	return _Core.weighted_one_of(pairs)


static func either(first: Variant, second: Variant, probability: float = 0.5) -> Component:
	return _Core.either(first, second, probability)


static func maybe(parts: Array, probability: float = 0.5) -> Component:
	return _Core.maybe(parts, probability)
