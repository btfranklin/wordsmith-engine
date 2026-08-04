import literaryTitlePartsJson from "../assets/Literary Title Parts.json" with {
  type: "json",
};

import {
  Component,
  choose,
  maybe,
  oneOf,
  type RandomSource,
  weightedOneOf,
} from "../core.js";
import { GivenNameCulture, PersonName } from "../names.js";
import {
  AuthoredArtifact,
  MartialSocialConcept,
  TimeOfDay,
  UCBerkeleyEmotion,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

interface LiteraryTitleParts {
  readonly objects: readonly string[];
  readonly pluralObjects: readonly string[];
  readonly sentientObjects: readonly string[];
  readonly qualities: readonly string[];
  readonly abstractions: readonly string[];
  readonly placeSuffixes: readonly string[];
  readonly verbs: readonly (readonly [string, string, string])[];
}

const LITERARY_TITLE_PARTS = literaryTitlePartsJson as unknown as LiteraryTitleParts;

class LiteraryTitleObject extends Component {
  readonly isPlural: boolean;

  constructor({ isPlural = false }: { isPlural?: boolean } = {}) {
    super();
    this.isPlural = isPlural;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return choose(
      rng,
      this.isPlural ? LITERARY_TITLE_PARTS.pluralObjects : LITERARY_TITLE_PARTS.objects,
    );
  }
}

class SentientLiteraryTitleObject extends Component {
  render(rng: RandomSource): string {
    return choose(rng, LITERARY_TITLE_PARTS.sentientObjects);
  }
}

class TitleQuality extends Component {
  render(rng: RandomSource): string {
    return choose(rng, LITERARY_TITLE_PARTS.qualities);
  }
}

class TitleAbstraction extends Component {
  render(rng: RandomSource): string {
    return choose(rng, LITERARY_TITLE_PARTS.abstractions);
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
    const row = choose(rng, LITERARY_TITLE_PARTS.verbs);
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
    return choose(rng, LITERARY_TITLE_PARTS.placeSuffixes);
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
