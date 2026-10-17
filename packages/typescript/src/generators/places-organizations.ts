import placeAndOrganizationPartsJson from "../assets/Place and Organization Parts.json" with {
  type: "json",
};

import { Component, concat, oneOf, type RandomSource, weightedOneOf } from "../core.js";
import { GivenName, GivenNameCulture, Surname } from "../names.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

interface PlaceAndOrganizationParts {
  readonly tavernAdjectives: readonly string[];
  readonly animals: readonly string[];
  readonly tavernObjects: readonly string[];
  readonly tavernEndings: readonly string[];
  readonly landmarkAdjectives: readonly string[];
  readonly landmarkFeatures: readonly string[];
  readonly landmarkRoots: readonly string[];
  readonly landmarkSuffixes: readonly string[];
  readonly landmarkPluralFeatures: readonly string[];
  readonly organizationAdjectives: readonly string[];
  readonly organizationSymbols: readonly string[];
  readonly organizationConcepts: readonly string[];
  readonly tradesPlural: readonly string[];
  readonly organizationTypes: readonly string[];
}

const parts = placeAndOrganizationPartsJson as unknown as PlaceAndOrganizationParts;

class PlacePart extends Component {
  readonly key: keyof PlaceAndOrganizationParts;

  constructor(key: keyof PlaceAndOrganizationParts) {
    super();
    this.key = key;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    return oneOf(...parts[this.key]).render(rng);
  }
}

export class TavernName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        4,
        spaced(
          "The",
          new PlacePart("tavernAdjectives"),
          oneOf(new PlacePart("animals"), new PlacePart("tavernObjects")),
        ),
      ],
      [
        3,
        spaced("The", new PlacePart("animals"), "and", new PlacePart("tavernObjects")),
      ],
      [
        2,
        spaced(
          new GivenName({ culture: GivenNameCulture.englishSpeaking }).possessiveForm(),
          new PlacePart("tavernEndings"),
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
      [
        4,
        spaced(new PlacePart("landmarkAdjectives"), new PlacePart("landmarkFeatures")),
      ],
      [3, concat(new PlacePart("landmarkRoots"), new PlacePart("landmarkSuffixes"))],
      [2, spaced(new Surname().possessiveForm(), new PlacePart("landmarkFeatures"))],
      [
        1,
        spaced(
          "The",
          new PlacePart("landmarkAdjectives"),
          new PlacePart("landmarkPluralFeatures"),
        ),
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
          new PlacePart("organizationAdjectives"),
          new PlacePart("organizationSymbols"),
        ),
      ],
      [
        3,
        spaced(new TownName(), new PlacePart("tradesPlural").possessiveForm(), "Guild"),
      ],
      [
        2,
        spaced(
          "The",
          new PlacePart("organizationAdjectives"),
          new PlacePart("organizationTypes"),
        ),
      ],
      [1, spaced("The Society of", new PlacePart("organizationConcepts"))],
    )
      .titleCase()
      .render(rng);
  }
}
