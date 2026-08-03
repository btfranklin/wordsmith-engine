import exoticCharacterSetsJson from "./assets/Exotic Character Sets.json" with {
  type: "json",
};
import { choose, concat, either, type RandomSource } from "./core.js";
import { Adjective, Adverb, Noun, Verb, VerbTense } from "./words.js";

type ExoticCharacterSets = Readonly<Record<string, readonly string[]>>;

const exoticCharacterSets = exoticCharacterSetsJson as unknown as ExoticCharacterSets;
const exoticCharacterSetNames = Object.freeze(Object.keys(exoticCharacterSets));

function assertCharacterSetsAreValid(): void {
  if (exoticCharacterSetNames.length === 0) {
    throw new Error("Exotic character assets require at least one set.");
  }

  const seen = new Set<string>();
  for (const setName of exoticCharacterSetNames) {
    const characterSet = exoticCharacterSets[setName];
    if (characterSet === undefined || characterSet.length === 0) {
      throw new Error(`Exotic character set is empty: ${setName}`);
    }
    for (const character of characterSet) {
      const codePoints = [...character];
      const value = codePoints[0]?.codePointAt(0);
      if (
        codePoints.length !== 1 ||
        value === undefined ||
        (value >= 0xd800 && value <= 0xdfff)
      ) {
        throw new Error(`Exotic character set contains a non-scalar value: ${setName}`);
      }
      if (seen.has(character)) {
        throw new Error(`Exotic character is duplicated: ${character}`);
      }
      seen.add(character);
    }
  }
}

assertCharacterSetsAreValid();

// biome-ignore lint/complexity/noStaticOnlyClass: Mirrors the established public API.
export class ExoticCharacter {
  static randomCharacter(rng: RandomSource): string {
    const setName = choose(rng, exoticCharacterSetNames);
    return choose(rng, exoticCharacterSets[setName] as readonly string[]);
  }

  static randomCharacterFromSet(setName: string, rng: RandomSource): string {
    const characterSet = exoticCharacterSets[setName];
    if (characterSet === undefined) {
      throw new RangeError(`Invalid character set requested: ${setName}`);
    }
    return choose(rng, characterSet);
  }
}

const REFERENCE_TIME_MILLISECONDS = Date.UTC(2001, 0, 1);

function timestampSuffix(): string {
  const microseconds = BigInt(Date.now() - REFERENCE_TIME_MILLISECONDS) * 1_000n;
  return microseconds.toString(36).toUpperCase();
}

// biome-ignore lint/complexity/noStaticOnlyClass: Mirrors the established public API.
export class ReadableUniqueIdentifier {
  static makeIdentifier(rng: RandomSource): string {
    const prefix = either(
      concat(new Adjective(), "_", new Noun()),
      concat(new Adverb(), "_", new Verb({ tense: VerbTense.presentPerfect })),
    ).render(rng);
    return `${prefix}_${timestampSuffix()}`;
  }
}
