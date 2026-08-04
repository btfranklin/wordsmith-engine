import {
  AlienName,
  ExoticCharacter,
  FictionalElementName,
  FictionalMineralName,
  NauticalShipName,
  PersonName,
  seededRandom,
} from "../dist/index.js";

const worldSeed = "example:world-5343";
const stream = (name: string) => seededRandom(`${worldSeed}:${name}`);

const generated = [
  ["Person", new PersonName().render(stream("person-name"))],
  ["Alien", new AlienName({ syllableCount: 3 }).render(stream("alien-name"))],
  ["Vessel", new NauticalShipName().render(stream("nautical-vessel"))],
  ["Element", new FictionalElementName().render(stream("element"))],
  ["Mineral", new FictionalMineralName().render(stream("mineral"))],
  ["Character", ExoticCharacter.randomCharacter(stream("exotic-character"))],
] as const;

for (const [label, value] of generated) {
  console.log(`${label}: ${value}`);
}
