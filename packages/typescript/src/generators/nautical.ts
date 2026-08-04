import { either, type RandomSource, weightedOneOf } from "../core.js";
import {
  AncientGivenName,
  BinaryGender,
  FantasyName,
  GivenName,
  GivenNameCulture,
} from "../names.js";
import {
  MartialSocialConcept,
  NauticalShipNameColor,
  NauticalShipNameObject,
  PrimitiveWeapon,
  ShipNameAdjective,
  TimeOfDay,
} from "../words.js";
import { TownName } from "./groups-places.js";
import { StatelessComponent, spaced } from "./support.js";

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
