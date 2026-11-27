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

const hash = await globalThis.crypto.subtle.digest(
  "SHA-256",
  new TextEncoder().encode("character:editor"),
);
const digest = Array.from(new Uint8Array(hash), (byte) =>
  byte.toString(16).padStart(2, "0"),
).join("");
const editor = new PersonName({
  givenNameFormat: ["initial", "initial"],
  prefix: "Dr.",
  generation: "IV",
  credentials: ["PhD."],
});
console.log(`Editor: ${await editor.fromHash(digest)}`);
console.log(`Varied: ${await new PersonName({ style: "varied" }).fromHash(digest)}`);
