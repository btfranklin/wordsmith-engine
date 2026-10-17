import celestialPartsJson from "../assets/Celestial Name Parts.json" with {
  type: "json",
};
import creaturePartsJson from "../assets/Creature Name Parts.json" with {
  type: "json",
};

import { concat, oneOf, type RandomSource, weightedOneOf } from "../core.js";
import { FantasyName, Surname } from "../names.js";
import {
  BodyPart,
  BusinessAnimal,
  BusinessColor,
  BusinessTrade,
  CelestialObjectType,
  CreatureType,
  Habitat,
  IndustrialTrade,
  NaturalNameRoot,
  ShopType,
  WildAnimal,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

interface CelestialNameParts {
  readonly celestialConcepts: readonly string[];
}

interface CreatureNameParts {
  readonly descriptors: readonly string[];
  readonly behaviorAdjectives: readonly string[];
}

const celestialParts = celestialPartsJson as unknown as CelestialNameParts;
const creatureParts = creaturePartsJson as unknown as CreatureNameParts;

export class CompoundCreatureName extends StatelessComponent {
  render(rng: RandomSource): string {
    return concat(new NaturalNameRoot({ context: "creature" }), new BodyPart())
      .titleCase()
      .render(rng);
  }
}

export class BusinessName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced(new Surname(), "& Sons")],
      [3, spaced(new BusinessColor(), new BusinessAnimal(), new BusinessTrade())],
      [2, spaced(new TownName(), new IndustrialTrade())],
      [1, spaced(new Surname().possessiveForm(), new ShopType())],
    )
      .titleCase()
      .render(rng);
  }
}

export class CelestialBodyName extends StatelessComponent {
  render(rng: RandomSource): string {
    const syntheticName = new FantasyName({
      syllableCount: 3,
      allowHyphen: false,
      allowApostrophe: false,
    }).titleCase();

    return weightedOneOf(
      [4, syntheticName],
      [
        3,
        spaced(
          syntheticName,
          oneOf("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),
        ),
      ],
      [
        2,
        spaced(new Surname().possessiveForm(), new CelestialObjectType()).titleCase(),
      ],
      [
        1,
        spaced(
          "The",
          new CelestialObjectType(),
          "of",
          oneOf(...celestialParts.celestialConcepts),
        ).titleCase(),
      ],
    ).render(rng);
  }
}

export class CreatureName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced(new CompoundCreatureName(), new CreatureType())],
      [3, spaced(oneOf(...creatureParts.descriptors), new Habitat(), new WildAnimal())],
      [2, spaced(oneOf(...creatureParts.behaviorAdjectives), new CreatureType())],
      [1, new CompoundCreatureName()],
    )
      .titleCase()
      .render(rng);
  }
}
