import {
  concat,
  either,
  oneOf,
  type RandomSource,
  randomBoolean,
  weightedOneOf,
} from "../core.js";
import { GivenName, GivenNameCulture, Surname } from "../names.js";
import {
  Adjective,
  LocationAdjective,
  MartialSocialConcept,
  Noun,
  NounForm,
  PrimitiveWeapon,
  VillainousPersonNoun,
} from "../words.js";
import { StatelessComponent, spaced } from "./support.js";

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
