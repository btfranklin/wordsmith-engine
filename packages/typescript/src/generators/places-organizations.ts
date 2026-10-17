import placeAndOrganizationPartsJson from "../assets/Place and Organization Parts.json" with {
  type: "json",
};

import { concat, oneOf, type RandomSource, weightedOneOf } from "../core.js";
import { GivenName, GivenNameCulture, Surname } from "../names.js";
import {
  GuildTrade,
  LandmarkAdjective,
  LandmarkFeature,
  NaturalNameRoot,
  OrganizationSymbol,
  TavernAnimal,
  TavernObject,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

interface PlaceAndOrganizationParts {
  readonly tavernAdjectives: readonly string[];
  readonly animals: readonly string[];
  readonly tavernObjects: readonly string[];
  readonly tavernEndings: readonly string[];
  readonly landmarkAdjectives: readonly string[];
  readonly landmarkFeatures: readonly string[];
  readonly landmarkSuffixes: readonly string[];
  readonly landmarkPluralFeatures: readonly string[];
  readonly organizationAdjectives: readonly string[];
  readonly organizationConcepts: readonly string[];
  readonly organizationTypes: readonly string[];
}

const parts = placeAndOrganizationPartsJson as unknown as PlaceAndOrganizationParts;

export class HeraldicSymbol extends StatelessComponent {
  render(rng: RandomSource): string {
    return oneOf(new TavernAnimal(), new TavernObject()).render(rng);
  }
}

export class CompoundLandmarkName extends StatelessComponent {
  render(rng: RandomSource): string {
    return concat(
      new NaturalNameRoot({ context: "landmark" }),
      oneOf(...parts.landmarkSuffixes),
    )
      .titleCase()
      .render(rng);
  }
}

export class TavernName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced("The", oneOf(...parts.tavernAdjectives), new HeraldicSymbol())],
      [3, spaced("The", new TavernAnimal(), "and", new TavernObject())],
      [
        2,
        spaced(
          new GivenName({ culture: GivenNameCulture.englishSpeaking }).possessiveForm(),
          oneOf(...parts.tavernEndings),
        ),
      ],
      [1, spaced(new TownName(), oneOf("Inn", "Tavern", "Lodge"))],
    )
      .titleCase()
      .render(rng);
  }
}

export class LandmarkName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced(new LandmarkAdjective(), new LandmarkFeature())],
      [3, new CompoundLandmarkName()],
      [2, spaced(new Surname().possessiveForm(), new LandmarkFeature())],
      [
        1,
        spaced("The", new LandmarkAdjective(), oneOf(...parts.landmarkPluralFeatures)),
      ],
    )
      .titleCase()
      .render(rng);
  }
}

export class OrganizationName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        4,
        spaced(
          "The Order of the",
          oneOf(...parts.organizationAdjectives),
          new OrganizationSymbol(),
        ),
      ],
      [3, spaced(new TownName(), new GuildTrade().possessiveForm(), "Guild")],
      [
        2,
        spaced(
          "The",
          oneOf(...parts.organizationAdjectives),
          oneOf(...parts.organizationTypes),
        ),
      ],
      [1, spaced("The Society of", oneOf(...parts.organizationConcepts))],
    )
      .titleCase()
      .render(rng);
  }
}
