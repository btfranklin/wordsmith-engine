import surnamesJson from "./assets/Common Surnames.json" with { type: "json" };
import givenNamesJson from "./assets/Given Names.json" with { type: "json" };
import personNameStylesJson from "./assets/Person Name Styles.json" with {
  type: "json",
};
import syntheticNamePartsJson from "./assets/Synthetic Name Parts.json" with {
  type: "json",
};
import { Component, choose, type RandomSource, randomBoolean } from "./core.js";
import { randomFraction } from "./random.js";
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

export type GivenNamePart = "full" | "initial";
export type PersonNameStyle = "plain" | "varied";

export interface PersonNameModifiers {
  readonly prefix?: string | undefined;
  readonly generation?: string | undefined;
  readonly credentials?: readonly string[] | undefined;
}

type NameWeights<T> = readonly (readonly [weight: number, value: T])[];

export interface PersonNameOptions extends GivenNameOptions, PersonNameModifiers {
  readonly style?: PersonNameStyle | undefined;
  readonly givenNameFormat?: readonly GivenNamePart[] | undefined;
  readonly initialPeriod?: boolean | undefined;
  readonly initialSeparator?: string | undefined;
  readonly generationSeparator?: string | undefined;
  readonly credentialSeparator?: string | undefined;
  readonly formatWeights?: NameWeights<readonly GivenNamePart[]> | undefined;
  readonly modifierWeights?: NameWeights<PersonNameModifiers> | undefined;
}

interface NameDraw {
  readonly label: string;
  readonly count: number;
  readonly boundaries?: readonly number[];
}

type NameSelection<T> = Generator<NameDraw, T, number>;

interface WeightedChoices<T> {
  readonly values: readonly T[];
  readonly boundaries: readonly number[];
}

function compileWeights<T>(pairs: NameWeights<T>): WeightedChoices<T> {
  const values: T[] = [];
  const boundaries: number[] = [];
  let total = 0;
  let largest = 0;
  for (const [weight, value] of pairs) {
    if (!Number.isFinite(weight) || weight < 0) {
      throw new RangeError("Weights must be finite and non-negative.");
    }
    if (weight > 0) {
      total += weight;
      largest = Math.max(largest, weight);
      values.push(value);
      boundaries.push(total);
    }
  }
  if (!(total > 0) || !Number.isFinite(total)) {
    throw new RangeError("Weights must have a finite positive total.");
  }
  if (total <= 2 ** -1022) {
    total = 0;
    boundaries.length = 0;
    for (const [weight] of pairs) {
      if (weight > 0) {
        total += weight / largest;
        boundaries.push(total);
      }
    }
  }
  return { values, boundaries };
}

function drawIndex(fraction: number, { count, boundaries }: NameDraw): number {
  if (boundaries === undefined) {
    return Math.floor(fraction * count);
  }
  const target = fraction * (boundaries.at(-1) as number);
  const index = boundaries.findIndex((boundary) => target < boundary);
  return index < 0 ? count - 1 : index;
}

function* selectNameValue<T>(label: string, values: readonly T[]): NameSelection<T> {
  const index = yield { label, count: values.length };
  return values[index] as T;
}

function* selectWeighted<T>(
  label: string,
  choices: WeightedChoices<T>,
): NameSelection<T> {
  const index = yield {
    label,
    count: choices.values.length,
    boundaries: choices.boundaries,
  };
  return choices.values[index] as T;
}

function snapshotFormat(parts: readonly GivenNamePart[]): readonly GivenNamePart[] {
  if (
    !Array.isArray(parts) ||
    parts.length === 0 ||
    Array.from(parts).some((part) => part !== "full" && part !== "initial")
  ) {
    throw new RangeError("Given name format must contain full or initial parts.");
  }
  return Object.freeze([...parts]);
}

function snapshotModifiers(modifiers: PersonNameModifiers): PersonNameModifiers {
  const { prefix, generation, credentials } = modifiers;
  if (
    (prefix !== undefined && typeof prefix !== "string") ||
    (generation !== undefined && typeof generation !== "string")
  ) {
    throw new TypeError("Prefix and generation must be strings.");
  }
  if (
    credentials !== undefined &&
    (!Array.isArray(credentials) ||
      Array.from(credentials).some(
        (value) => typeof value !== "string" || !value.trim(),
      ))
  ) {
    throw new TypeError("Credentials must be a sequence of nonempty strings.");
  }
  return {
    prefix,
    generation,
    credentials:
      credentials === undefined ? undefined : Object.freeze([...credentials]),
  };
}

const personNameStyles = personNameStylesJson as unknown as {
  readonly formats: NameWeights<readonly GivenNamePart[]>;
  readonly modifiers: NameWeights<"none" | "prefix" | "generation" | "credentials">;
  readonly titles: readonly string[];
  readonly generations: readonly string[];
  readonly credentials: readonly string[];
};
const defaultNameFormats = compileWeights(personNameStyles.formats);
const defaultNameModifiers = compileWeights(personNameStyles.modifiers);

export class PersonName extends Component {
  readonly gender: BinaryGender | undefined;
  readonly culture: GivenNameCulture | undefined;
  readonly #style: PersonNameStyle;
  readonly #givenNameFormat: readonly GivenNamePart[] | undefined;
  readonly #initialPeriod: boolean;
  readonly #initialSeparator: string;
  readonly #generationSeparator: string;
  readonly #credentialSeparator: string;
  readonly #overrides: PersonNameModifiers;
  readonly #formats: WeightedChoices<readonly GivenNamePart[]> | undefined;
  readonly #modifiers: WeightedChoices<PersonNameModifiers> | undefined;

  constructor(options: PersonNameOptions = {}) {
    super();
    if (options.gender !== undefined && !isBinaryGender(options.gender)) {
      throw new TypeError(`Unsupported binary gender: ${String(options.gender)}`);
    }
    if (options.culture !== undefined && !isGivenNameCulture(options.culture)) {
      throw new TypeError(`Unsupported given-name culture: ${String(options.culture)}`);
    }
    const {
      style = "plain",
      givenNameFormat,
      initialPeriod = true,
      initialSeparator = "",
      generationSeparator = " ",
      credentialSeparator = ", ",
      formatWeights,
      modifierWeights,
    } = options;
    if (style !== "plain" && style !== "varied") {
      throw new RangeError("Style must be plain or varied.");
    }
    if (typeof initialPeriod !== "boolean") {
      throw new TypeError("Initial period must be a boolean.");
    }
    if (
      [initialSeparator, generationSeparator, credentialSeparator].some(
        (separator) => typeof separator !== "string",
      )
    ) {
      throw new TypeError("Separators must be strings.");
    }
    this.gender = options.gender;
    this.culture = options.culture;
    this.#style = style;
    this.#givenNameFormat =
      givenNameFormat === undefined ? undefined : snapshotFormat(givenNameFormat);
    this.#initialPeriod = initialPeriod;
    this.#initialSeparator = initialSeparator;
    this.#generationSeparator = generationSeparator;
    this.#credentialSeparator = credentialSeparator;
    this.#overrides = snapshotModifiers(options);
    this.#formats =
      formatWeights === undefined
        ? undefined
        : compileWeights(
            formatWeights.map(([weight, format]) => [weight, snapshotFormat(format)]),
          );
    this.#modifiers =
      modifierWeights === undefined
        ? undefined
        : compileWeights(
            modifierWeights.map(([weight, modifiers]) => [
              weight,
              snapshotModifiers(modifiers),
            ]),
          );
    Object.freeze(this);
  }

  override render(rng: RandomSource): string {
    const selection = this.#selectName();
    let step = selection.next();
    while (!step.done) {
      step = selection.next(drawIndex(randomFraction(rng), step.value));
    }
    return step.value;
  }

  async fromHash(digest: string): Promise<string> {
    if (
      typeof digest !== "string" ||
      digest.length !== 64 ||
      !/^[0-9a-f]+$/iu.test(digest)
    ) {
      throw new RangeError("Expected a 64-character hexadecimal SHA-256 digest.");
    }
    const bytes = new Uint8Array(33);
    for (let index = 0; index < 32; index += 1) {
      bytes[index] = Number.parseInt(digest.slice(index * 2, index * 2 + 2), 16);
    }

    const encoder = new TextEncoder();
    const selection = this.#selectName();
    let step = selection.next();
    while (!step.done) {
      const { label } = step.value;
      const labelBytes = encoder.encode(label);
      const input = new Uint8Array(bytes.length + labelBytes.length);
      input.set(bytes);
      input.set(labelBytes, bytes.length);
      const hash = await globalThis.crypto.subtle.digest("SHA-256", input);
      const fraction = new DataView(hash).getUint32(0) / 2 ** 32;
      step = selection.next(drawIndex(fraction, step.value));
    }
    return step.value;
  }

  *#selectName(): NameSelection<string> {
    let parts = this.#givenNameFormat;
    if (parts === undefined) {
      const formats =
        this.#formats ?? (this.#style === "varied" ? defaultNameFormats : undefined);
      parts =
        formats === undefined ? ["full"] : yield* selectWeighted("format", formats);
    }
    const gender = this.gender ?? (yield* selectNameValue("gender", BINARY_GENDERS));
    const culture =
      this.culture ?? (yield* selectNameValue("culture", GIVEN_NAME_CULTURES));
    const names = givenNames.modern[culture][gender];
    const given: string[] = [];
    for (const [index, part] of parts.entries()) {
      const value = yield* selectNameValue(`given.${index}`, names);
      if (index > 0) {
        given.push(
          parts[index - 1] === "initial" && part === "initial"
            ? this.#initialSeparator
            : " ",
        );
      }
      if (part === "initial") {
        const letter = value.match(/\p{L}/u)?.[0] as string;
        given.push(letter.toUpperCase(), this.#initialPeriod ? "." : "");
      } else {
        given.push(value);
      }
    }
    const surname = yield* selectNameValue("surname", surnames);
    const modifiers = yield* this.#selectModifiers();
    const prefix = this.#overrides.prefix ?? modifiers.prefix;
    const generation = this.#overrides.generation ?? modifiers.generation;
    const credentials = this.#overrides.credentials ?? modifiers.credentials ?? [];
    return (
      (prefix ? `${prefix} ` : "") +
      `${given.join("")} ${surname}` +
      (generation ? this.#generationSeparator + generation : "") +
      credentials.map((credential) => this.#credentialSeparator + credential).join("")
    );
  }

  *#selectModifiers(): NameSelection<PersonNameModifiers> {
    const { prefix, generation, credentials } = this.#overrides;
    if (prefix !== undefined && generation !== undefined && credentials !== undefined) {
      return {};
    }
    if (this.#modifiers !== undefined) {
      return yield* selectWeighted("modifier", this.#modifiers);
    }
    if (this.#style === "varied") {
      const category = yield* selectWeighted("modifier", defaultNameModifiers);
      if (category === "prefix" && prefix === undefined) {
        return { prefix: yield* selectNameValue("title", personNameStyles.titles) };
      }
      if (category === "generation" && generation === undefined) {
        return {
          generation: yield* selectNameValue(
            "generation",
            personNameStyles.generations,
          ),
        };
      }
      if (category === "credentials" && credentials === undefined) {
        const credential = yield* selectNameValue(
          "credential",
          personNameStyles.credentials,
        );
        return { credentials: [credential] };
      }
    }
    return {};
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
