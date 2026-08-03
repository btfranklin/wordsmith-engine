import assert from "node:assert/strict";
import { test } from "node:test";
import * as wordsmith from "../dist/index.js";

const expectedExports = [
  "Adjective",
  "Adverb",
  "AlienName",
  "AlbumTitle",
  "AncientGivenName",
  "Article",
  "AuthoredArtifact",
  "BandName",
  "BinaryGender",
  "ChemicalCompoundName",
  "Component",
  "CriminalGangName",
  "Determiner",
  "ExoticCharacter",
  "FantasyName",
  "FictionalElementName",
  "FictionalMineralName",
  "GivenName",
  "GivenNameCulture",
  "HighConceptMovieTitle",
  "LiteraryTitle",
  "LocationAdjective",
  "MartialSocialConcept",
  "MovieTitle",
  "NauticalShipName",
  "NauticalShipNameColor",
  "NauticalShipNameObject",
  "Noun",
  "NounForm",
  "PersonName",
  "PrimitiveWeapon",
  "Pronoun",
  "ReadableUniqueIdentifier",
  "ShipNameAdjective",
  "SimpleLiteraryTitle",
  "SimpleMovieTitle",
  "Surname",
  "TimeOfDay",
  "TownName",
  "UCBerkeleyEmotion",
  "UnusualLiteraryTitle",
  "Verb",
  "VerbTense",
  "VillainousPersonNoun",
  "component",
  "concat",
  "either",
  "empty",
  "join",
  "literal",
  "maybe",
  "oneOf",
  "seededRandom",
  "weightedOneOf",
  "ws",
] as const;

test("the root module exposes the complete documented runtime surface", () => {
  assert.deepEqual(Object.keys(wordsmith).sort(), [...expectedExports].sort());
});

test("the root module supports a real asset-backed composition", () => {
  const rng = wordsmith.seededRandom(5343);
  const value = wordsmith
    .join(["The", new wordsmith.Adjective(), new wordsmith.Noun()], " ")
    .titleCase()
    .render(rng);
  assert.match(value, /^The /);
});
