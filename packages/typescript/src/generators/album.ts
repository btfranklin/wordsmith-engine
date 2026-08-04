import {
  Component,
  choose,
  concat,
  oneOf,
  type RandomSource,
  weightedOneOf,
} from "../core.js";
import { GivenNameCulture, PersonName } from "../names.js";
import {
  Adjective,
  AuthoredArtifact,
  MartialSocialConcept,
  Noun,
  NounForm,
  TimeOfDay,
  UCBerkeleyEmotion,
  Verb,
  VerbTense,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

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
