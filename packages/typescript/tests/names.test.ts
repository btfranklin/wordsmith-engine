import assert from "node:assert/strict";
import { test } from "node:test";
import type { RandomSource } from "../dist/core.js";
import {
  AlienName,
  AncientGivenName,
  BinaryGender,
  FantasyName,
  GivenName,
  GivenNameCulture,
  PersonName,
  Surname,
} from "../dist/names.js";

function fractionSource(fractions: readonly number[]): RandomSource {
  let index = 0;
  return {
    random() {
      const fraction = fractions[index];
      assert.notEqual(fraction, undefined, "random fixture was exhausted");
      index += 1;
      return fraction as number;
    },
  };
}

test("name enums are frozen string-value objects", () => {
  assert.deepEqual(BinaryGender, { male: "male", female: "female" });
  assert.deepEqual(GivenNameCulture, {
    englishSpeaking: "english_speaking",
    latinAmerican: "latin_american",
    eastern: "eastern",
  });
  assert.ok(Object.isFrozen(BinaryGender));
  assert.ok(Object.isFrozen(GivenNameCulture));
});

test("GivenName respects requested gender and culture", () => {
  const component = new GivenName({
    gender: BinaryGender.male,
    culture: GivenNameCulture.englishSpeaking,
  });
  assert.equal(component.render(fractionSource([0])), "Aaquil");
  assert.ok(Object.isFrozen(component));
});

test("GivenName resolves omitted options through the caller RNG", () => {
  assert.equal(new GivenName().render(fractionSource([0, 0, 0])), "Aaquil");
});

test("GivenName validates enum values at the JavaScript boundary", () => {
  assert.throws(
    () =>
      new GivenName({
        gender: "other" as BinaryGender,
      }),
    /Unsupported binary gender/,
  );
  assert.throws(
    () =>
      new GivenName({
        culture: "unknown" as GivenNameCulture,
      }),
    /Unsupported given-name culture/,
  );
});

test("AncientGivenName and Surname render from packaged assets", () => {
  assert.equal(
    new AncientGivenName({ gender: BinaryGender.male }).render(fractionSource([0])),
    "Abundius",
  );
  assert.equal(new Surname().render(fractionSource([0])), "Smith");
});

test("PersonName forwards configuration and RNG to both components", () => {
  const component = new PersonName({
    gender: BinaryGender.male,
    culture: GivenNameCulture.englishSpeaking,
  });
  assert.equal(component.render(fractionSource([0, 0])), "Aaquil Smith");
  assert.ok(Object.isFrozen(component));
});

test("AlienName is deterministic and preserves separator precedence", () => {
  const plain = new AlienName({
    syllableCount: 3,
    allowHyphen: false,
    allowApostrophe: false,
  });
  assert.equal(plain.render(fractionSource([0, 0, 0, 0.9])), "Aaa");

  const punctuated = new AlienName({
    syllableCount: 3,
    allowHyphen: true,
    allowApostrophe: true,
  });
  assert.equal(punctuated.render(fractionSource([0.1, 0.9, 0, 0, 0, 0, 0.9])), "A-aa");
});

test("FantasyName follows the classical prefix, middle, and ending model", () => {
  const component = new FantasyName({
    syllableCount: 4,
    allowHyphen: false,
    allowApostrophe: false,
  });
  assert.equal(component.render(fractionSource([0, 0, 0, 0.1, 0])), "Aelaaadon");
  assert.ok(Object.isFrozen(component));
});

test("synthetic names require a positive integer syllable count", () => {
  assert.throws(() => new AlienName({ syllableCount: 0 }), /greater than 0/);
  assert.throws(() => new FantasyName({ syllableCount: 1.5 }), /greater than 0/);
});

test("name components reject invalid custom RNG fractions", () => {
  assert.throws(
    () =>
      new Surname().render({
        random: () => 1,
      }),
    /\[0, 1\)/,
  );
});
