import adjectiveData from "./assets/Adjectives.json" with { type: "json" };
import adverbData from "./assets/Adverbs.json" with { type: "json" };
import chemicalCompoundData from "./assets/Chemical Compound Names.json" with {
  type: "json",
};
import curatedWordListsJson from "./assets/Curated Word Lists.json" with {
  type: "json",
};
import nounData from "./assets/Nouns.json" with { type: "json" };
import verbData from "./assets/Verbs.json" with { type: "json" };

import { Component } from "./core.js";
import { selectArticle, selectDeterminer } from "./core-grammar.js";
import { choose, type RandomSource } from "./random.js";

export const NounForm = Object.freeze({
  singular: "singular",
  plural: "plural",
} as const);
export type NounForm = (typeof NounForm)[keyof typeof NounForm];

export const VerbTense = Object.freeze({
  base: "base",
  past: "past",
  pastParticiple: "pastParticiple",
  present: "present",
  presentPerfect: "presentPerfect",
} as const);
export type VerbTense = (typeof VerbTense)[keyof typeof VerbTense];

const ADJECTIVES = adjectiveData as readonly string[];
const ADVERBS = adverbData as readonly string[];
const CHEMICAL_COMPOUNDS = chemicalCompoundData as readonly string[];
const NOUNS = nounData as unknown as readonly (readonly [string, string])[];
const VERBS = verbData as unknown as readonly (readonly [
  string,
  string,
  string,
  string,
  string,
])[];

const AUTHORED_ARTIFACTS: readonly string[] = curatedWordListsJson.authoredArtifacts;
const LOCATION_ADJECTIVES: readonly string[] = curatedWordListsJson.locationAdjectives;
const MARTIAL_SOCIAL_CONCEPTS: readonly string[] =
  curatedWordListsJson.martialSocialConcepts;
const UC_BERKELEY_EMOTIONS: readonly string[] = curatedWordListsJson.ucBerkeleyEmotions;
const VILLAINOUS_PERSON_NOUNS: readonly string[] =
  curatedWordListsJson.villainousPersonNouns;
const PRIMITIVE_WEAPONS: readonly string[] = curatedWordListsJson.primitiveWeapons;
const NAUTICAL_SHIP_NAME_OBJECTS: readonly string[] =
  curatedWordListsJson.nauticalShipNameObjects;
const NAUTICAL_SHIP_NAME_COLORS: readonly string[] =
  curatedWordListsJson.nauticalShipNameColors;
const SHIP_NAME_ADJECTIVES: readonly string[] = curatedWordListsJson.shipNameAdjectives;
const TIMES_OF_DAY: readonly string[] = curatedWordListsJson.timesOfDay;

function assertBoolean(value: unknown, name: string): asserts value is boolean {
  if (typeof value !== "boolean") {
    throw new TypeError(`${name} must be a boolean.`);
  }
}

abstract class OptionComponent extends Component {
  readonly #options: readonly string[];

  protected constructor(options: readonly string[]) {
    super();
    this.#options = options;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return choose(rng, this.#options);
  }
}

export class Adjective extends OptionComponent {
  constructor() {
    super(ADJECTIVES);
  }
}
export class Adverb extends OptionComponent {
  constructor() {
    super(ADVERBS);
  }
}
export class ChemicalCompoundName extends OptionComponent {
  constructor() {
    super(CHEMICAL_COMPOUNDS);
  }
}
export class AuthoredArtifact extends OptionComponent {
  constructor() {
    super(AUTHORED_ARTIFACTS);
  }
}
export class LocationAdjective extends OptionComponent {
  constructor() {
    super(LOCATION_ADJECTIVES);
  }
}
export class MartialSocialConcept extends OptionComponent {
  constructor() {
    super(MARTIAL_SOCIAL_CONCEPTS);
  }
}
export class UCBerkeleyEmotion extends OptionComponent {
  constructor() {
    super(UC_BERKELEY_EMOTIONS);
  }
}
export class NauticalShipNameObject extends OptionComponent {
  constructor() {
    super(NAUTICAL_SHIP_NAME_OBJECTS);
  }
}
export class NauticalShipNameColor extends OptionComponent {
  constructor() {
    super(NAUTICAL_SHIP_NAME_COLORS);
  }
}
export class ShipNameAdjective extends OptionComponent {
  constructor() {
    super(SHIP_NAME_ADJECTIVES);
  }
}
export class TimeOfDay extends OptionComponent {
  constructor() {
    super(TIMES_OF_DAY);
  }
}

export class Noun extends Component {
  readonly form: NounForm;

  constructor({ form = NounForm.singular }: { readonly form?: NounForm } = {}) {
    super();
    if (!Object.values(NounForm).includes(form)) {
      throw new RangeError("Invalid noun form.");
    }
    this.form = form;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return choose(rng, NOUNS)[this.form === NounForm.singular ? 0 : 1];
  }
}

export class Verb extends Component {
  readonly tense: VerbTense;

  constructor({ tense = VerbTense.base }: { readonly tense?: VerbTense } = {}) {
    super();
    if (!Object.values(VerbTense).includes(tense)) {
      throw new RangeError("Invalid verb tense.");
    }
    this.tense = tense;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    const indices: Record<VerbTense, number> = {
      [VerbTense.base]: 0,
      [VerbTense.past]: 1,
      [VerbTense.pastParticiple]: 2,
      [VerbTense.present]: 3,
      [VerbTense.presentPerfect]: 4,
    };
    return choose(rng, VERBS)[indices[this.tense]] as string;
  }
}

export class Pronoun extends Component {
  readonly isSingular: boolean;
  readonly isThirdPerson: boolean;

  constructor({
    isSingular,
    isThirdPerson,
  }: { readonly isSingular: boolean; readonly isThirdPerson: boolean }) {
    super();
    assertBoolean(isSingular, "isSingular");
    assertBoolean(isThirdPerson, "isThirdPerson");
    this.isSingular = isSingular;
    this.isThirdPerson = isThirdPerson;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    if (this.isThirdPerson) {
      return this.isSingular ? choose(rng, ["he", "she", "it"]) : "they";
    }
    return this.isSingular ? choose(rng, ["I", "you"]) : choose(rng, ["we", "you"]);
  }
}

export class Article extends Component {
  readonly isBeforeVowel: boolean;

  constructor({ isBeforeVowel = false }: { readonly isBeforeVowel?: boolean } = {}) {
    super();
    assertBoolean(isBeforeVowel, "isBeforeVowel");
    this.isBeforeVowel = isBeforeVowel;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return selectArticle(rng, { isBeforeVowel: this.isBeforeVowel });
  }
}

export class Determiner extends Component {
  readonly isBeforeVowel: boolean;

  constructor({ isBeforeVowel = false }: { readonly isBeforeVowel?: boolean } = {}) {
    super();
    assertBoolean(isBeforeVowel, "isBeforeVowel");
    this.isBeforeVowel = isBeforeVowel;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return selectDeterminer(rng, { isBeforeVowel: this.isBeforeVowel });
  }
}

export class VillainousPersonNoun extends Component {
  readonly isPlural: boolean;

  constructor({ isPlural }: { readonly isPlural: boolean }) {
    super();
    assertBoolean(isPlural, "isPlural");
    this.isPlural = isPlural;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    let value: string = choose(rng, VILLAINOUS_PERSON_NOUNS);
    if (!this.isPlural) return value;
    if (["ay", "ey", "iy", "oy", "uy"].some((ending) => value.endsWith(ending)))
      value += "s";
    else if (value.endsWith("y")) value = `${value.slice(0, -1)}ies`;
    else if (["x", "ss", "sh", "ch"].some((ending) => value.endsWith(ending)))
      value += "es";
    else if (value.endsWith("ife"))
      value = value === "lowlife" ? `${value}s` : `${value.slice(0, -2)}ves`;
    else if (["rf", "ief"].some((ending) => value.endsWith(ending)))
      value = `${value.slice(0, -1)}ves`;
    else if (value.endsWith("man")) value = `${value.slice(0, -2)}en`;
    else if (!value.endsWith("s")) value += "s";
    return value;
  }
}

export class PrimitiveWeapon extends Component {
  readonly isPlural: boolean;

  constructor({ isPlural = false }: { readonly isPlural?: boolean } = {}) {
    super();
    assertBoolean(isPlural, "isPlural");
    this.isPlural = isPlural;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    let value: string = choose(rng, PRIMITIVE_WEAPONS);
    if (this.isPlural)
      value = value.endsWith("ife") ? `${value.slice(0, -2)}ves` : `${value}s`;
    return value;
  }
}
