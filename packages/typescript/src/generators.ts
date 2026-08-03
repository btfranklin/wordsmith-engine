import {
  Component,
  choose,
  concat,
  either,
  join,
  maybe,
  oneOf,
  type RandomSource,
  randomBoolean,
  weightedOneOf,
} from "./core.js";
import {
  AlienName,
  AncientGivenName,
  BinaryGender,
  FantasyName,
  GivenName,
  GivenNameCulture,
  PersonName,
  Surname,
} from "./names.js";
import {
  Adjective,
  AuthoredArtifact,
  LocationAdjective,
  MartialSocialConcept,
  NauticalShipNameColor,
  NauticalShipNameObject,
  Noun,
  NounForm,
  PrimitiveWeapon,
  ShipNameAdjective,
  TimeOfDay,
  UCBerkeleyEmotion,
  Verb,
  VerbTense,
  VillainousPersonNoun,
} from "./words.js";

const spaced = (...parts: Parameters<typeof join>[0]) => join(parts, " ");

abstract class StatelessComponent extends Component {
  constructor() {
    super();
    Object.freeze(this);
  }
}

const ELEMENT_PREFIXES = [
  "aer",
  "astr",
  "aur",
  "cal",
  "cer",
  "chrom",
  "cry",
  "dyn",
  "eth",
  "ferr",
  "grav",
  "hel",
  "irid",
  "lumin",
  "myth",
  "nyx",
  "plasm",
  "quant",
  "selen",
  "umbr",
  "xen",
  "zeph",
] as const;
const ELEMENT_MIDDLES = [
  "",
  "a",
  "al",
  "ar",
  "en",
  "er",
  "i",
  "il",
  "on",
  "or",
  "ul",
] as const;
const MINERAL_PREFIXES = [
  "aurel",
  "bas",
  "cairn",
  "celest",
  "cinder",
  "dusk",
  "ember",
  "fels",
  "garn",
  "glint",
  "hal",
  "iron",
  "jade",
  "laz",
  "moon",
  "opal",
  "quartz",
  "rune",
  "sable",
  "shard",
  "thorn",
  "vein",
  "verd",
] as const;
const MINERAL_MIDDLES = ["", "a", "el", "en", "er", "il", "in", "or", "ul"] as const;

class ElementalRoot extends Component {
  render(rng: RandomSource): string {
    return choose(rng, ELEMENT_PREFIXES) + choose(rng, ELEMENT_MIDDLES);
  }
}

class MineralRoot extends Component {
  render(rng: RandomSource): string {
    return choose(rng, MINERAL_PREFIXES) + choose(rng, MINERAL_MIDDLES);
  }
}

function cleanMaterialRoot(value: string): string | undefined {
  const ascii = [...value.normalize("NFKD")]
    .filter((character) => (character.codePointAt(0) ?? 128) <= 127)
    .join("");
  const root = ascii.toLowerCase().replace(/[^a-z]/g, "");
  if (root.length < 3 || root.length > 10) return undefined;
  if (![..."aeiou"].some((vowel) => root.includes(vowel))) return undefined;
  if (root.includes("ii") || root.includes("yy")) return undefined;
  if (/[bcdfghjklmnpqrstvwxz]{5,}/.test(root)) return undefined;
  return root;
}

function makeMaterialRoot(
  rng: RandomSource,
  source: Component,
  fallback: string,
): string {
  for (let attempt = 0; attempt < 24; attempt += 1) {
    const root = cleanMaterialRoot(source.render(rng));
    if (root !== undefined) return root;
  }
  return fallback;
}

function elementRootSource(): Component {
  return weightedOneOf(
    [5, new ElementalRoot()],
    [
      1,
      new AlienName({ syllableCount: 2, allowHyphen: false, allowApostrophe: false }),
    ],
    [
      1,
      new FantasyName({ syllableCount: 2, allowHyphen: false, allowApostrophe: false }),
    ],
    [1, new Surname()],
  );
}

function mineralRootSource(): Component {
  return weightedOneOf(
    [4, new MineralRoot()],
    [
      2,
      new FantasyName({ syllableCount: 2, allowHyphen: false, allowApostrophe: false }),
    ],
    [1, new Surname()],
  );
}

const REAL_ELEMENTS = new Set([
  "actinium",
  "aluminium",
  "americium",
  "antimony",
  "argon",
  "arsenic",
  "astatine",
  "barium",
  "berkelium",
  "beryllium",
  "bismuth",
  "bohrium",
  "boron",
  "bromine",
  "cadmium",
  "caesium",
  "calcium",
  "californium",
  "carbon",
  "cerium",
  "chlorine",
  "chromium",
  "cobalt",
  "copernicium",
  "copper",
  "curium",
  "darmstadtium",
  "dubnium",
  "dysprosium",
  "einsteinium",
  "erbium",
  "europium",
  "fermium",
  "flerovium",
  "fluorine",
  "francium",
  "gadolinium",
  "gallium",
  "germanium",
  "gold",
  "hafnium",
  "hassium",
  "helium",
  "holmium",
  "hydrogen",
  "indium",
  "iodine",
  "iridium",
  "iron",
  "krypton",
  "lanthanum",
  "lawrencium",
  "lead",
  "lithium",
  "livermorium",
  "lutetium",
  "magnesium",
  "manganese",
  "meitnerium",
  "mendelevium",
  "mercury",
  "molybdenum",
  "moscovium",
  "neodymium",
  "neon",
  "neptunium",
  "nickel",
  "nihonium",
  "niobium",
  "nitrogen",
  "nobelium",
  "oganesson",
  "osmium",
  "oxygen",
  "palladium",
  "phosphorus",
  "platinum",
  "plutonium",
  "polonium",
  "potassium",
  "praseodymium",
  "promethium",
  "protactinium",
  "radium",
  "radon",
  "rhenium",
  "rhodium",
  "roentgenium",
  "rubidium",
  "ruthenium",
  "rutherfordium",
  "samarium",
  "scandium",
  "seaborgium",
  "selenium",
  "silicon",
  "silver",
  "sodium",
  "strontium",
  "sulfur",
  "tantalum",
  "technetium",
  "tellurium",
  "tennessine",
  "terbium",
  "thallium",
  "thorium",
  "thulium",
  "tin",
  "titanium",
  "tungsten",
  "uranium",
  "vanadium",
  "xenon",
  "ytterbium",
  "yttrium",
  "zinc",
  "zirconium",
]);

function elementSuffix(): Component {
  return weightedOneOf([4, "ium"], [2, "on"], [1, "ine"], [1, "ene"], [1, "gen"]);
}

function joinElementSuffix(originalRoot: string, suffix: string): string {
  let root = originalRoot;
  if (suffix === "ium") {
    if (root.endsWith("on")) root = root.slice(0, -2);
    while (root.length > 2 && /[aeiy]$/.test(root)) root = root.slice(0, -1);
    return root + suffix;
  }
  if (suffix === "gen") return root + (/[aeiou]$/.test(root) ? "gen" : "ogen");
  if (root.endsWith("e")) root = root.slice(0, -1);
  return root.endsWith(suffix) ? root : root + suffix;
}

export class FictionalElementName extends StatelessComponent {
  render(rng: RandomSource): string {
    for (let attempt = 0; attempt < 16; attempt += 1) {
      const root = makeMaterialRoot(rng, elementRootSource(), "lumin");
      const result = joinElementSuffix(root, elementSuffix().render(rng));
      if (!REAL_ELEMENTS.has(result)) return result;
    }
    return "luminum";
  }
}

function mineralSuffix(): Component {
  return weightedOneOf(
    [8, "ite"],
    [2, "ine"],
    [1.5, "spar"],
    [1, "ore"],
    [0.7, "stone"],
    [0.5, "glass"],
    [0.25, "cryst"],
  );
}

function joinMineralSuffix(originalRoot: string, originalSuffix: string): string {
  let root = originalRoot;
  let suffix = originalSuffix;
  if ((suffix === "ite" || suffix === "ine") && /[eiy]$/.test(root)) {
    root = root.slice(0, -1);
  }
  if (root.endsWith(suffix)) return root;
  if (root.at(-1) === suffix[0]) suffix = suffix.slice(1);
  return root + suffix;
}

export class FictionalMineralName extends StatelessComponent {
  render(rng: RandomSource): string {
    const root = makeMaterialRoot(rng, mineralRootSource(), "aurel");
    return joinMineralSuffix(root, mineralSuffix().render(rng));
  }
}

export class BandName extends StatelessComponent {
  render(rng: RandomSource): string {
    return oneOf(
      spaced("The", new Adjective()),
      spaced("The", new Noun()),
      spaced("The", new Noun({ form: NounForm.plural })),
      spaced(new Adjective(), new Noun()),
      spaced("The", new Adjective(), new Noun({ form: NounForm.plural })),
      spaced(
        new GivenName({ culture: GivenNameCulture.englishSpeaking }),
        "and the",
        new Noun({ form: NounForm.plural }),
      ),
      spaced(
        new GivenName({ culture: GivenNameCulture.englishSpeaking }).possessiveForm(),
        new Noun({ form: NounForm.plural }),
      ),
    )
      .titleCase()
      .render(rng);
  }
}

export class TownName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [9, spaced(new Surname(), oneOf("Bay", "Point", "City", "Park"))],
      [10, spaced(oneOf("Fort", "Port", "Cape"), new Surname())],
      [5, spaced(new Surname(), oneOf("River", "Hill", "Town", "Beach", "Village"))],
      [5, spaced(oneOf("Saint", "Mount", "Lake"), new Surname())],
      [
        2,
        spaced(
          "New",
          concat(new Surname(), oneOf("ton", "burg", "ville", "town", "dale")),
        ),
      ],
      [
        4,
        spaced(
          new LocationAdjective().firstUpper(),
          oneOf("Bay", "Point", "City", "Park"),
        ),
      ],
      [
        3,
        spaced(
          new LocationAdjective().firstUpper(),
          oneOf("River", "Hill", "Town", "Beach", "Village"),
        ),
      ],
      [62, concat(new Surname(), oneOf("ton", "burg", "ville", "town", "dale"))],
    ).render(rng);
  }
}

export class CriminalGangName extends StatelessComponent {
  render(rng: RandomSource): string {
    if (randomBoolean(rng, 0.25)) {
      return spaced(
        new GivenName({ culture: GivenNameCulture.englishSpeaking }).possessiveForm(),
        either(
          new VillainousPersonNoun({ isPlural: true }),
          new PrimitiveWeapon({ isPlural: true }),
        ),
      )
        .titleCase()
        .render(rng);
    }
    return spaced(
      "the",
      oneOf(
        spaced(
          new MartialSocialConcept(),
          new VillainousPersonNoun({ isPlural: true }),
        ),
        spaced(new PrimitiveWeapon(), new VillainousPersonNoun({ isPlural: true })),
        spaced(new VillainousPersonNoun({ isPlural: true }), "of", new TownName()),
        spaced(new TownName(), new VillainousPersonNoun({ isPlural: true })),
        spaced(new Adjective(), new VillainousPersonNoun({ isPlural: true })),
        spaced(
          new Adjective(),
          new VillainousPersonNoun({ isPlural: true }),
          "of",
          new TownName(),
        ),
      ).titleCase(),
    ).render(rng);
  }
}

export class NauticalShipName extends StatelessComponent {
  render(rng: RandomSource): string {
    const possessiveName = spaced(
      either(
        new MartialSocialConcept().firstUpper(),
        either(
          new GivenName({
            gender: BinaryGender.female,
            culture: GivenNameCulture.englishSpeaking,
          }),
          new GivenName({
            gender: BinaryGender.male,
            culture: GivenNameCulture.englishSpeaking,
          }),
          0.75,
        ),
        0.33,
      ).possessiveForm(),
      either(
        either(new NauticalShipNameObject(), new PrimitiveWeapon()),
        new MartialSocialConcept(),
      ),
    );
    return weightedOneOf(
      [
        4,
        new GivenName({
          gender: BinaryGender.female,
          culture: GivenNameCulture.englishSpeaking,
        }),
      ],
      [3, new MartialSocialConcept()],
      [1, new TownName()],
      [
        1,
        either(
          new AncientGivenName({ gender: BinaryGender.female }),
          new FantasyName({ syllableCount: 3 }),
        ),
      ],
      [1, new NauticalShipNameObject()],
      [1, new ShipNameAdjective()],
      [
        1,
        spaced(
          new NauticalShipNameColor(),
          either(new NauticalShipNameObject(), new PrimitiveWeapon(), 0.75),
        ),
      ],
      [
        2,
        spaced(
          new ShipNameAdjective(),
          either(new NauticalShipNameObject(), new PrimitiveWeapon(), 0.85),
        ),
      ],
      [
        1,
        spaced(
          new TimeOfDay(),
          either(new MartialSocialConcept(), new PrimitiveWeapon(), 0.75),
        ),
      ],
      [
        1,
        spaced(
          new TownName(),
          either(new NauticalShipNameObject(), new PrimitiveWeapon(), 0.85),
        ),
      ],
      [
        1,
        spaced(
          either(new NauticalShipNameObject(), new PrimitiveWeapon()),
          "of",
          either(new MartialSocialConcept(), new TownName()),
        ),
      ],
      [1, possessiveName],
    )
      .titleCase()
      .render(rng);
  }
}

const LITERARY_OBJECTS = [
  "archive",
  "bell",
  "bridge",
  "camera",
  "cipher",
  "clock",
  "compass",
  "door",
  "garden",
  "harbor",
  "key",
  "lantern",
  "machine",
  "map",
  "mirror",
  "moon",
  "orchard",
  "room",
  "signal",
  "staircase",
  "station",
  "thread",
  "window",
] as const;
const LITERARY_OBJECTS_PLURAL = [
  "archives",
  "bells",
  "bridges",
  "cities",
  "clocks",
  "doors",
  "gardens",
  "harbors",
  "lanterns",
  "machines",
  "maps",
  "mirrors",
  "moons",
  "orchards",
  "rooms",
  "signals",
  "staircases",
  "stations",
  "threads",
  "windows",
] as const;
const SENTIENT_OBJECTS = [
  "archive",
  "bell",
  "city",
  "clock",
  "door",
  "garden",
  "ghost",
  "harbor",
  "house",
  "lantern",
  "machine",
  "map",
  "mirror",
  "moon",
  "river",
  "signal",
  "station",
  "window",
] as const;
const TITLE_QUALITIES = [
  "borrowed",
  "bright",
  "buried",
  "distant",
  "divided",
  "forgotten",
  "hidden",
  "hollow",
  "last",
  "little",
  "lost",
  "minor",
  "paper",
  "red",
  "restless",
  "second",
  "secret",
  "silver",
  "sleeping",
  "strange",
  "summer",
  "vanishing",
  "winter",
] as const;
const TITLE_ABSTRACTIONS = [
  "absence",
  "arrival",
  "beauty",
  "ceremony",
  "distance",
  "forgiveness",
  "hunger",
  "memory",
  "mercy",
  "noise",
  "patience",
  "promise",
  "silence",
  "weather",
] as const;
const PLACE_SUFFIXES = [
  "almanac",
  "blues",
  "chronicle",
  "dispatch",
  "elegy",
  "lantern",
  "ledger",
  "nocturne",
  "parable",
  "refrain",
] as const;
const TITLE_VERBS = [
  ["answer", "answers", "answering"],
  ["arrive", "arrives", "arriving"],
  ["burn", "burns", "burning"],
  ["dream", "dreams", "dreaming of"],
  ["find", "finds", "finding"],
  ["forget", "forgets", "forgetting"],
  ["listen", "listens", "listening to"],
  ["remember", "remembers", "remembering"],
  ["return", "returns", "returning to"],
  ["sing", "sings", "singing to"],
  ["speak", "speaks", "speaking with"],
  ["vanish", "vanishes", "vanishing"],
  ["wait", "waits", "waiting"],
  ["wake", "wakes", "waking"],
] as const;

class LiteraryTitleObject extends Component {
  readonly isPlural: boolean;
  constructor({ isPlural = false }: { isPlural?: boolean } = {}) {
    super();
    this.isPlural = isPlural;
    Object.freeze(this);
  }
  render(rng: RandomSource): string {
    return choose(rng, this.isPlural ? LITERARY_OBJECTS_PLURAL : LITERARY_OBJECTS);
  }
}

class SentientLiteraryTitleObject extends Component {
  render(rng: RandomSource): string {
    return choose(rng, SENTIENT_OBJECTS);
  }
}
class TitleQuality extends Component {
  render(rng: RandomSource): string {
    return choose(rng, TITLE_QUALITIES);
  }
}
class TitleAbstraction extends Component {
  render(rng: RandomSource): string {
    return choose(rng, TITLE_ABSTRACTIONS);
  }
}
class AbstractSubject extends Component {
  render(rng: RandomSource): string {
    return oneOf(
      new TitleAbstraction(),
      new UCBerkeleyEmotion(),
      new MartialSocialConcept(),
    ).render(rng);
  }
}
class ResonantSubject extends Component {
  render(rng: RandomSource): string {
    return oneOf(
      new LiteraryTitleObject({ isPlural: true }),
      new AbstractSubject(),
      new PersonName({ culture: GivenNameCulture.englishSpeaking }),
      new TownName(),
    ).render(rng);
  }
}

class TitleNounPhrase extends Component {
  readonly wrapped: Component;
  readonly requiresModifier: boolean;
  readonly modifierProbability: number;
  constructor(
    wrapped: Component,
    {
      requiresModifier = false,
      modifierProbability = 0.45,
    }: {
      requiresModifier?: boolean;
      modifierProbability?: number;
    } = {},
  ) {
    super();
    this.wrapped = wrapped;
    this.requiresModifier = requiresModifier;
    this.modifierProbability = modifierProbability;
    Object.freeze(this);
  }
  render(rng: RandomSource): string {
    const modifier = this.requiresModifier
      ? new TitleQuality()
      : maybe(new TitleQuality(), { probability: this.modifierProbability });
    return spaced("the", modifier, this.wrapped).render(rng);
  }
}

type TitleVerbForm = "base" | "finite" | "gerund";
class TitleVerb extends Component {
  readonly form: TitleVerbForm;
  constructor({ form = "finite" }: { form?: TitleVerbForm } = {}) {
    super();
    this.form = form;
    Object.freeze(this);
  }
  render(rng: RandomSource): string {
    const row = choose(rng, TITLE_VERBS);
    return row[this.form === "base" ? 0 : this.form === "finite" ? 1 : 2];
  }
}

class ImpossibleAction extends Component {
  render(rng: RandomSource): string {
    return oneOf(
      spaced(
        new TitleVerb({ form: "gerund" }),
        new TitleNounPhrase(new LiteraryTitleObject()),
      ),
      spaced(new TitleVerb({ form: "gerund" }), new AbstractSubject()),
      spaced("cataloging", new LiteraryTitleObject({ isPlural: true })),
      spaced("repairing", new TitleNounPhrase(new LiteraryTitleObject())),
      spaced(
        "teaching",
        new TitleNounPhrase(new SentientLiteraryTitleObject()),
        "to",
        new TitleVerb({ form: "base" }),
      ),
    ).render(rng);
  }
}

class PlaceSuffix extends Component {
  render(rng: RandomSource): string {
    return choose(rng, PLACE_SUFFIXES);
  }
}

export class LiteraryTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [0.78, new SimpleLiteraryTitle()],
      [0.22, new UnusualLiteraryTitle()],
    ).render(rng);
  }
}

export class SimpleLiteraryTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [3, new TitleNounPhrase(new LiteraryTitleObject(), { requiresModifier: true })],
      [
        2.5,
        spaced(
          new TitleNounPhrase(new LiteraryTitleObject()),
          "of",
          new ResonantSubject(),
        ),
      ],
      [
        2.5,
        spaced(new TitleNounPhrase(new LiteraryTitleObject()), "at", new TownName()),
      ],
      [2, spaced(new AbstractSubject(), "and", new AbstractSubject())],
      [2, spaced(new AbstractSubject(), "in", new TownName())],
      [
        1.8,
        spaced(
          new TitleNounPhrase(new AuthoredArtifact()),
          "of",
          new ResonantSubject(),
        ),
      ],
      [
        1.5,
        spaced(
          new PersonName({
            culture: GivenNameCulture.englishSpeaking,
          }).possessiveForm(),
          new AuthoredArtifact(),
        ),
      ],
      [
        1.5,
        spaced(
          oneOf(
            "a field guide to",
            "a history of",
            "a map of",
            "a study of",
            "an atlas of",
            "notes on",
            "the book of",
            "the grammar of",
          ),
          new ResonantSubject(),
        ),
      ],
      [1.2, spaced(new TimeOfDay(), "with", new ResonantSubject())],
      [
        1.2,
        oneOf(
          spaced("passage through", new LiteraryTitleObject({ isPlural: true })),
          spaced("the road to", new AbstractSubject()),
          spaced("the road to", new TownName()),
          spaced("the voyage into", new AbstractSubject()),
          spaced("the voyage to", new TownName()),
        ),
      ],
      [1, spaced(new TownName(), new PlaceSuffix())],
    )
      .titleCase()
      .render(rng);
  }
}

export class UnusualLiteraryTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        2.4,
        spaced(
          oneOf(
            "a manual for",
            "a recipe for",
            "instructions for",
            "rules for",
            "the practice of",
          ),
          new ImpossibleAction(),
        ),
      ],
      [
        2.2,
        spaced(
          new TitleNounPhrase(new SentientLiteraryTitleObject()),
          "that",
          new TitleVerb(),
        ),
      ],
      [
        2,
        spaced(
          new TitleNounPhrase(new LiteraryTitleObject()),
          "between",
          new LiteraryTitleObject({ isPlural: true }),
        ),
      ],
      [
        1.8,
        spaced(
          oneOf("after", "before", "if", "until", "when", "while"),
          new TitleNounPhrase(new SentientLiteraryTitleObject()),
          new TitleVerb(),
        ),
      ],
      [
        1.6,
        spaced(
          oneOf("how", "why"),
          new TitleNounPhrase(new SentientLiteraryTitleObject()),
          new TitleVerb(),
        ),
      ],
      [1.5, spaced(new AbstractSubject(), "after", new AbstractSubject())],
      [1.4, spaced(new PlaceSuffix(), "for", new ResonantSubject())],
      [
        1.2,
        spaced(
          new TitleNounPhrase(new AuthoredArtifact()),
          "against",
          new AbstractSubject(),
        ),
      ],
      [
        1,
        spaced(
          new TitleNounPhrase(new LiteraryTitleObject()),
          "inside",
          new TitleNounPhrase(new LiteraryTitleObject()),
        ),
      ],
    )
      .titleCase()
      .render(rng);
  }
}

class ShortAlbumTitle extends Component {
  render(rng: RandomSource): string {
    const form = choose(rng, [NounForm.singular, NounForm.plural] as const);
    return weightedOneOf(
      [2, new Noun({ form: NounForm.plural })],
      [2, spaced(new Adjective(), new Noun({ form }))],
      [1.4, spaced(new TimeOfDay(), new Noun({ form: NounForm.plural }))],
      [1.2, new UCBerkeleyEmotion()],
      [1.2, new MartialSocialConcept()],
      [1, new AuthoredArtifact()],
    )
      .titleCase()
      .render(rng);
  }
}

class FragmentAlbumTitle extends Component {
  render(rng: RandomSource): string {
    const form = choose(rng, [NounForm.singular, NounForm.plural] as const);
    return weightedOneOf(
      [1.8, spaced(oneOf("no", "new", "old", "last", "first"), new Noun({ form }))],
      [1.6, spaced(new TimeOfDay(), "with", new Noun({ form: NounForm.plural }))],
      [1.4, spaced(new Noun(), "for", new Noun({ form: NounForm.plural }))],
      [
        1.2,
        spaced(
          new UCBerkeleyEmotion(),
          "for",
          new PersonName({ culture: GivenNameCulture.englishSpeaking }),
        ),
      ],
      [1, spaced(new Verb({ tense: VerbTense.base }), "the", new Noun())],
    )
      .titleCase()
      .render(rng);
  }
}

class DocumentaryAlbumTitle extends Component {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [2, spaced(new TownName(), oneOf("sessions", "recordings"))],
      [
        1.6,
        spaced(
          new PersonName({
            culture: GivenNameCulture.englishSpeaking,
          }).possessiveForm(),
          new AuthoredArtifact(),
        ),
      ],
      [1.4, spaced(new AuthoredArtifact(), "from", new TownName())],
      [
        1.4,
        spaced(
          oneOf("songs for", "music for"),
          oneOf(
            new Noun({ form: NounForm.plural }),
            new UCBerkeleyEmotion(),
            new MartialSocialConcept(),
          ),
        ),
      ],
      [1, spaced(new TimeOfDay(), oneOf("sessions", "recordings"))],
    )
      .titleCase()
      .render(rng);
  }
}

class CollisionAlbumTitle extends Component {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [1.8, concat(new Noun(), " / ", new Noun())],
      [1.6, spaced(new Noun(), "and", new Noun({ form: NounForm.plural }))],
      [1.4, spaced(new Adjective(), "and", new Adjective())],
      [
        1.2,
        spaced(new UCBerkeleyEmotion(), "and", new Noun({ form: NounForm.plural })),
      ],
      [1, spaced(new MartialSocialConcept(), "/", new UCBerkeleyEmotion())],
    )
      .titleCase()
      .render(rng);
  }
}

export class AlbumTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [0.35, new ShortAlbumTitle()],
      [0.25, new FragmentAlbumTitle()],
      [0.22, new DocumentaryAlbumTitle()],
      [0.18, new CollisionAlbumTitle()],
    ).render(rng);
  }
}

export class SimpleMovieTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [2, new PersonName({ culture: GivenNameCulture.englishSpeaking })],
      [1.8, new TownName()],
      [1.7, spaced("the", new Adjective(), new Noun())],
      [1.7, spaced("the", new Noun(), "of", new TownName())],
      [1.5, spaced(new TimeOfDay(), "in", new TownName())],
      [1.4, spaced(new MartialSocialConcept(), "at", new TownName())],
      [1.3, spaced(new UCBerkeleyEmotion(), "and", new MartialSocialConcept())],
      [
        1.2,
        spaced(
          new PersonName({
            culture: GivenNameCulture.englishSpeaking,
          }).possessiveForm(),
          new AuthoredArtifact(),
        ),
      ],
      [
        1,
        spaced(
          "the",
          new AuthoredArtifact(),
          "of",
          new PersonName({ culture: GivenNameCulture.englishSpeaking }),
        ),
      ],
    )
      .titleCase()
      .render(rng);
  }
}

export class HighConceptMovieTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        2.2,
        spaced(
          oneOf("escape from", "return to", "the fall of", "the last days of"),
          new TownName(),
        ),
      ],
      [
        1.8,
        spaced(
          oneOf("before", "after", "when"),
          new Noun().prefixedByArticle(),
          new Verb({ tense: VerbTense.present }),
        ),
      ],
      [
        1.6,
        spaced(
          oneOf("before", "after", "when"),
          new PersonName({ culture: GivenNameCulture.englishSpeaking }),
          new Verb({ tense: VerbTense.present }),
        ),
      ],
      [
        1.4,
        spaced("the", oneOf("case", "secret", "trial", "shadow"), "of", new TownName()),
      ],
      [
        1.2,
        spaced(
          "the",
          oneOf("first", "last", "final"),
          oneOf(new AuthoredArtifact(), new Noun()),
        ),
      ],
      [1, spaced("the", new Noun(), "that", new Verb({ tense: VerbTense.past }))],
    )
      .titleCase()
      .render(rng);
  }
}

export class MovieTitle extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [0.55, new SimpleMovieTitle()],
      [0.3, new HighConceptMovieTitle()],
      [0.15, new LiteraryTitle()],
    ).render(rng);
  }
}
