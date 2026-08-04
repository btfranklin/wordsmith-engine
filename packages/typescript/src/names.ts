import surnamesJson from "./assets/Common Surnames.json" with { type: "json" };
import givenNamesJson from "./assets/Given Names.json" with { type: "json" };
import syntheticNamePartsJson from "./assets/Synthetic Name Parts.json" with {
  type: "json",
};
import { Component, choose, join, type RandomSource, randomBoolean } from "./core.js";
import { firstUpper } from "./strings.js";

export const BinaryGender = Object.freeze({
  male: "male",
  female: "female",
} as const);
export type BinaryGender = (typeof BinaryGender)[keyof typeof BinaryGender];

export const GivenNameCulture = Object.freeze({
  englishSpeaking: "english_speaking",
  latinAmerican: "latin_american",
  eastern: "eastern",
} as const);
export type GivenNameCulture = (typeof GivenNameCulture)[keyof typeof GivenNameCulture];

const BINARY_GENDERS = Object.freeze([BinaryGender.male, BinaryGender.female] as const);
const GIVEN_NAME_CULTURES = Object.freeze([
  GivenNameCulture.englishSpeaking,
  GivenNameCulture.latinAmerican,
  GivenNameCulture.eastern,
] as const);

interface GivenNamesAsset {
  readonly modern: Readonly<
    Record<GivenNameCulture, Readonly<Record<BinaryGender, readonly string[]>>>
  >;
  readonly ancient: Readonly<Record<BinaryGender, readonly string[]>>;
}

const givenNames = givenNamesJson as unknown as GivenNamesAsset;
const surnames = surnamesJson as readonly string[];

function isBinaryGender(value: unknown): value is BinaryGender {
  return BINARY_GENDERS.includes(value as BinaryGender);
}

function isGivenNameCulture(value: unknown): value is GivenNameCulture {
  return GIVEN_NAME_CULTURES.includes(value as GivenNameCulture);
}

function randomInteger(rng: RandomSource, minimum: number, maximum: number): number {
  const values = Array.from(
    { length: maximum - minimum },
    (_, index) => minimum + index,
  );
  return choose(rng, values);
}

export interface GivenNameOptions {
  readonly gender?: BinaryGender | undefined;
  readonly culture?: GivenNameCulture | undefined;
}

export class GivenName extends Component {
  readonly gender: BinaryGender | undefined;
  readonly culture: GivenNameCulture | undefined;

  constructor(options: GivenNameOptions = {}) {
    super();
    if (options.gender !== undefined && !isBinaryGender(options.gender)) {
      throw new TypeError(`Unsupported binary gender: ${String(options.gender)}`);
    }
    if (options.culture !== undefined && !isGivenNameCulture(options.culture)) {
      throw new TypeError(`Unsupported given-name culture: ${String(options.culture)}`);
    }
    this.gender = options.gender;
    this.culture = options.culture;
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    const gender = this.gender ?? choose(rng, BINARY_GENDERS);
    const culture = this.culture ?? choose(rng, GIVEN_NAME_CULTURES);
    return choose(rng, givenNames.modern[culture][gender]);
  }
}

export interface AncientGivenNameOptions {
  readonly gender?: BinaryGender | undefined;
}

export class AncientGivenName extends Component {
  readonly gender: BinaryGender | undefined;

  constructor(options: AncientGivenNameOptions = {}) {
    super();
    if (options.gender !== undefined && !isBinaryGender(options.gender)) {
      throw new TypeError(`Unsupported binary gender: ${String(options.gender)}`);
    }
    this.gender = options.gender;
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    const gender = this.gender ?? choose(rng, BINARY_GENDERS);
    return choose(rng, givenNames.ancient[gender]);
  }
}

export class Surname extends Component {
  constructor() {
    super();
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    return choose(rng, surnames);
  }
}

export interface PersonNameOptions {
  readonly gender?: BinaryGender | undefined;
  readonly culture?: GivenNameCulture | undefined;
}

export class PersonName extends Component {
  readonly gender: BinaryGender | undefined;
  readonly culture: GivenNameCulture | undefined;

  constructor(options: PersonNameOptions = {}) {
    super();
    if (options.gender !== undefined && !isBinaryGender(options.gender)) {
      throw new TypeError(`Unsupported binary gender: ${String(options.gender)}`);
    }
    if (options.culture !== undefined && !isGivenNameCulture(options.culture)) {
      throw new TypeError(`Unsupported given-name culture: ${String(options.culture)}`);
    }
    this.gender = options.gender;
    this.culture = options.culture;
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    return join(
      [new GivenName({ gender: this.gender, culture: this.culture }), new Surname()],
      " ",
    ).render(rng);
  }
}

const ALIEN_OPEN_ENDED_SYLLABLES: readonly string[] =
  syntheticNamePartsJson.alien.openEndedSyllables;

const ALIEN_ENDING_SOUNDS: readonly string[] =
  syntheticNamePartsJson.alien.endingSounds;

interface SyntheticNameOptions {
  readonly syllableCount: number;
  readonly allowHyphen?: boolean | undefined;
  readonly allowApostrophe?: boolean | undefined;
}

function validateSyntheticNameOptions(options: SyntheticNameOptions): void {
  if (!Number.isSafeInteger(options.syllableCount) || options.syllableCount < 1) {
    throw new RangeError("Syllable count must be greater than 0.");
  }
  if (options.allowHyphen !== undefined && typeof options.allowHyphen !== "boolean") {
    throw new TypeError("allowHyphen must be a boolean.");
  }
  if (
    options.allowApostrophe !== undefined &&
    typeof options.allowApostrophe !== "boolean"
  ) {
    throw new TypeError("allowApostrophe must be a boolean.");
  }
}

export type AlienNameOptions = SyntheticNameOptions;

export class AlienName extends Component {
  readonly syllableCount: number;
  readonly allowHyphen: boolean;
  readonly allowApostrophe: boolean;

  constructor(options: AlienNameOptions) {
    super();
    validateSyntheticNameOptions(options);
    this.syllableCount = options.syllableCount;
    this.allowHyphen = options.allowHyphen ?? true;
    this.allowApostrophe = options.allowApostrophe ?? true;
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    const willUseHyphen =
      this.syllableCount > 2 && this.allowHyphen && randomBoolean(rng);
    const willUseApostrophe =
      this.syllableCount > 2 && this.allowApostrophe && randomBoolean(rng);
    const hyphenSyllable = willUseHyphen
      ? randomInteger(rng, 1, this.syllableCount)
      : 0;
    const apostropheSyllable = willUseApostrophe
      ? randomInteger(rng, 1, this.syllableCount)
      : 0;

    let text = "";
    for (
      let currentSyllable = 1;
      currentSyllable <= this.syllableCount;
      currentSyllable += 1
    ) {
      text += choose(rng, ALIEN_OPEN_ENDED_SYLLABLES);
      if (currentSyllable === apostropheSyllable) {
        text += "'";
      } else if (currentSyllable === hyphenSyllable) {
        text += "-";
      }
    }

    if (randomBoolean(rng)) {
      text += choose(rng, ALIEN_ENDING_SOUNDS);
    }
    return firstUpper(text);
  }
}

const FANTASY_PREFIXES: readonly string[] = syntheticNamePartsJson.fantasy.prefixes;

const FANTASY_MIDDLES: readonly string[] = syntheticNamePartsJson.fantasy.middles;

const FANTASY_ENDINGS: readonly string[] = syntheticNamePartsJson.fantasy.endings;

const FANTASY_COMPOUND_ENDINGS: readonly string[] =
  syntheticNamePartsJson.fantasy.compoundEndings;

export type FantasyNameOptions = SyntheticNameOptions;

export class FantasyName extends Component {
  readonly syllableCount: number;
  readonly allowHyphen: boolean;
  readonly allowApostrophe: boolean;

  constructor(options: FantasyNameOptions) {
    super();
    validateSyntheticNameOptions(options);
    this.syllableCount = options.syllableCount;
    this.allowHyphen = options.allowHyphen ?? true;
    this.allowApostrophe = options.allowApostrophe ?? true;
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    const pieces: string[] = [choose(rng, FANTASY_PREFIXES)];
    for (let index = 0; index < this.syllableCount - 2; index += 1) {
      pieces.push(choose(rng, FANTASY_MIDDLES));
    }

    if (this.syllableCount > 1) {
      pieces.push(
        this.syllableCount > 3 && randomBoolean(rng, 0.25)
          ? choose(rng, FANTASY_COMPOUND_ENDINGS)
          : choose(rng, FANTASY_ENDINGS),
      );
    }

    let text = pieces.join("");
    if (this.allowHyphen && this.syllableCount > 4 && randomBoolean(rng, 0.12)) {
      const splitAt = randomInteger(rng, 2, text.length - 2);
      text = `${text.slice(0, splitAt)}-${text.slice(splitAt)}`;
    }
    if (this.allowApostrophe && this.syllableCount > 4 && randomBoolean(rng, 0.04)) {
      const splitAt = randomInteger(rng, 2, text.length - 2);
      text = `${text.slice(0, splitAt)}'${text.slice(splitAt)}`;
    }

    return firstUpper(text);
  }
}
