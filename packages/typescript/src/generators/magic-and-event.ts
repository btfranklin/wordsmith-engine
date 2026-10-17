import festivalParts from "../assets/Festival Name Parts.json" with { type: "json" };
import operationParts from "../assets/Operation Name Parts.json" with { type: "json" };
import spellParts from "../assets/Spell Name Parts.json" with { type: "json" };

import { concat, oneOf, type RandomSource, weightedOneOf } from "../core.js";
import { Surname } from "../names.js";
import {
  ArtifactObject,
  MagicalConcept,
  OperationColor,
  OrganizationSymbol,
  PrimitiveWeapon,
  Season,
  SpellEffect,
  TimeOfDay,
  WildAnimal,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { FictionalMineralName } from "./materials.js";
import {
  CompoundLandmarkName,
  HeraldicSymbol,
  LandmarkName,
} from "./places-organizations.js";
import { StatelessComponent, spaced } from "./support.js";

export class ArtifactName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced("The", new ArtifactObject(), "of", new MagicalConcept())],
      [3, spaced(new Surname().possessiveForm(), new ArtifactObject())],
      [2, spaced(new FictionalMineralName(), new PrimitiveWeapon())],
      [1, spaced("The", new ArtifactObject(), "of", new LandmarkName())],
    )
      .titleCase()
      .render(rng);
  }
}

export class SpellName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [4, spaced(new SpellEffect(), "of", new MagicalConcept())],
      [
        3,
        spaced(
          new Surname().possessiveForm(),
          oneOf(...spellParts.spellModifiers),
          new SpellEffect(),
        ),
      ],
      [
        2,
        spaced(
          oneOf(...spellParts.spellCommands),
          "the",
          oneOf(...spellParts.spellTargets),
        ),
      ],
      [1, spaced(new SpellEffect(), "of", new TimeOfDay())],
    )
      .titleCase()
      .render(rng);
  }
}

export class OperationName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        4,
        spaced(
          "Operation",
          oneOf(...operationParts.operationAdjectives),
          new HeraldicSymbol(),
        ),
      ],
      [3, spaced("Project", new OperationColor(), new WildAnimal())],
      [2, spaced("Operation", new CompoundLandmarkName())],
      [1, spaced(new LandmarkName(), "Expedition")],
    )
      .titleCase()
      .render(rng);
  }
}

export class FestivalName extends StatelessComponent {
  render(rng: RandomSource): string {
    return weightedOneOf(
      [
        4,
        spaced(
          "The",
          oneOf(...festivalParts.festivalTypes),
          "of",
          oneOf(...festivalParts.festivalThemes),
        ),
      ],
      [3, spaced(new TownName(), new Season(), oneOf(...festivalParts.festivalTypes))],
      [2, spaced(new TimeOfDay(), oneOf(...festivalParts.festivalTypes))],
      [1, concat(new OrganizationSymbol(), oneOf(...festivalParts.festivalSuffixes))],
    )
      .titleCase()
      .render(rng);
  }
}
