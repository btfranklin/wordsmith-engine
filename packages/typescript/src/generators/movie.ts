import { oneOf, type RandomSource, weightedOneOf } from "../core.js";
import { GivenNameCulture, PersonName } from "../names.js";
import {
  Adjective,
  AuthoredArtifact,
  MartialSocialConcept,
  Noun,
  TimeOfDay,
  UCBerkeleyEmotion,
  Verb,
  VerbTense,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { LiteraryTitle } from "./literary.js";
import { StatelessComponent, spaced } from "./support.js";

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
