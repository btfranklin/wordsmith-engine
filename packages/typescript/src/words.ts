import adjectiveData from "./assets/Adjectives.json" with { type: "json" };
import adverbData from "./assets/Adverbs.json" with { type: "json" };
import chemicalCompoundData from "./assets/Chemical Compound Names.json" with {
  type: "json",
};
import nounData from "./assets/Nouns.json" with { type: "json" };
import verbData from "./assets/Verbs.json" with { type: "json" };

import { Component } from "./core.js";
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

const AUTHORED_ARTIFACTS = [
  "almanac",
  "atlas",
  "book",
  "catalog",
  "codex",
  "field guide",
  "inventory",
  "letter",
  "manual",
  "notebook",
  "record",
  "score",
] as const;
const LOCATION_ADJECTIVES = [
  "ancient",
  "beautiful",
  "blissful",
  "breezy",
  "charming",
  "cloudy",
  "colorful",
  "dangerous",
  "dreamy",
  "dry",
  "enchanted",
  "enchanting",
  "fertile",
  "floral",
  "foggy",
  "forgotten",
  "freezing",
  "frozen",
  "ghostly",
  "gloomy",
  "glorious",
  "grand",
  "grassy",
  "haunted",
  "hilly",
  "looming",
  "majestic",
  "misty",
  "moonshine",
  "muddy",
  "mysterious",
  "mystical",
  "peaceful",
  "quiet",
  "rainy",
  "reedy",
  "rocky",
  "sandy",
  "shady",
  "silent",
  "snowy",
  "stony",
  "stormy",
  "sunny",
  "windswept",
  "windy",
] as const;
const MARTIAL_SOCIAL_CONCEPTS = [
  "ambush",
  "anger",
  "betrayal",
  "bravery",
  "conquest",
  "courage",
  "death",
  "deception",
  "delight",
  "despair",
  "devastation",
  "discipline",
  "domination",
  "famine",
  "freedom",
  "fury",
  "glory",
  "hatred",
  "honor",
  "independence",
  "justice",
  "liberation",
  "liberty",
  "mercy",
  "murder",
  "pestilence",
  "plunder",
  "pride",
  "rage",
  "regret",
  "reprisal",
  "retribution",
  "revenge",
  "righteousness",
  "slaughter",
  "terror",
  "transgression",
  "treachery",
  "treason",
  "triumph",
  "vengeance",
  "victory",
  "wrath",
] as const;
const UC_BERKELEY_EMOTIONS = [
  "admiration",
  "adoration",
  "appreciation",
  "amusement",
  "anxiety",
  "awe",
  "awkwardness",
  "boredom",
  "calmness",
  "confusion",
  "craving",
  "disgust",
  "empathy",
  "entrancement",
  "envy",
  "excitement",
  "fear",
  "horror",
  "interest",
  "joy",
  "nostalgia",
  "romance",
  "sadness",
  "satisfaction",
  "lust",
  "sympathy",
  "triumph",
] as const;
const VILLAINOUS_PERSON_NOUNS = [
  "bandit",
  "brigand",
  "bruiser",
  "buccaneer",
  "burglar",
  "charlatan",
  "corsair",
  "criminal",
  "crook",
  "deceiver",
  "delinquent",
  "demon",
  "desperado",
  "devil",
  "dodger",
  "gunman",
  "hood",
  "scoundrel",
  "sinner",
  "blackguard",
  "brute",
  "creep",
  "dog",
  "filcher",
  "good-for-nothing",
  "goon",
  "grifter",
  "hellion",
  "highwayman",
  "hijacker",
  "hoodlum",
  "hooligan",
  "imp",
  "knave",
  "libertine",
  "looter",
  "lowlife",
  "maggot",
  "malefactor",
  "marauder",
  "mischief-maker",
  "miscreant",
  "mountebank",
  "mugger",
  "murderer",
  "ne'er-do-well",
  "offender",
  "outlaw",
  "pilferer",
  "pirate",
  "profligate",
  "punk",
  "prowler",
  "plunderer",
  "racketeer",
  "rapscallion",
  "rascal",
  "ravager",
  "reprobate",
  "robber",
  "rogue",
  "rook",
  "ruffian",
  "scalawag",
  "shark",
  "swindler",
  "thief",
  "thug",
  "troublemaker",
  "wretch",
  "vagabond",
  "varlet",
  "villain",
] as const;
const PRIMITIVE_WEAPONS = [
  "sword",
  "blade",
  "mace",
  "hammer",
  "knife",
  "dagger",
  "axe",
  "halberd",
  "glaive",
  "spear",
  "lance",
  "pike",
  "bow",
  "crossbow",
] as const;
const NAUTICAL_SHIP_NAME_OBJECTS = [
  "blade",
  "breeze",
  "concubine",
  "consort",
  "crown",
  "dagger",
  "dancer",
  "demon",
  "destiny",
  "devil",
  "disciple",
  "dragon",
  "dream",
  "dryad",
  "falcon",
  "flame",
  "fox",
  "ghost",
  "gypsy",
  "harpy",
  "heart",
  "hound",
  "jewel",
  "knave",
  "knight",
  "kraken",
  "lance",
  "mage",
  "maiden",
  "nightmare",
  "nymph",
  "paladin",
  "pearl",
  "princess",
  "queen",
  "revenant",
  "rogue",
  "rose",
  "serpent",
  "shield",
  "spear",
  "spirit",
  "stallion",
  "star",
  "storm",
  "sword",
  "treasure",
  "trinity",
  "warlock",
  "wench",
  "widow",
  "witch",
  "wizard",
  "wolf",
] as const;
const NAUTICAL_SHIP_NAME_COLORS = [
  "amber",
  "black",
  "blue",
  "bronze",
  "copper",
  "golden",
  "gray",
  "green",
  "ivory",
  "jade",
  "obsidian",
  "red",
  "silver",
  "white",
] as const;
const SHIP_NAME_ADJECTIVES = [
  "adamantine",
  "adventurous",
  "ancient",
  "angry",
  "beastly",
  "beautiful",
  "courageous",
  "dancing",
  "dastardly",
  "draconian",
  "elder",
  "enchanted",
  "enchanting",
  "heroic",
  "immortal",
  "indestructible",
  "invincible",
  "magnificent",
  "malicious",
  "mighty",
  "nefarious",
  "perfect",
  "pious",
  "precious",
  "priceless",
  "relentless",
  "righteous",
  "saintly",
  "sinful",
  "sinister",
  "sylvan",
  "terrible",
  "terrific",
  "unstoppable",
  "unyielding",
  "valiant",
  "vengeful",
  "virtuous",
  "wandering",
  "windward",
  "wrathful",
  "yearning",
  "youthful",
] as const;
const TIMES_OF_DAY = [
  "midnight",
  "night",
  "morning",
  "dawn",
  "sunrise",
  "daytime",
  "midday",
  "afternoon",
  "evening",
  "dusk",
  "twilight",
  "sunset",
] as const;

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
    this.isBeforeVowel = isBeforeVowel;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    const value = choose(rng, ["a", "the"]);
    return value === "a" && this.isBeforeVowel ? "an" : value;
  }
}

export class Determiner extends Component {
  readonly isBeforeVowel: boolean;

  constructor({ isBeforeVowel = false }: { readonly isBeforeVowel?: boolean } = {}) {
    super();
    this.isBeforeVowel = isBeforeVowel;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    const value = choose(rng, ["a", "the", "my", "your", "our", "her", "his"]);
    return value === "a" && this.isBeforeVowel ? "an" : value;
  }
}

export class VillainousPersonNoun extends Component {
  readonly isPlural: boolean;

  constructor({ isPlural }: { readonly isPlural: boolean }) {
    super();
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
