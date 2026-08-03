import assert from "node:assert/strict";
import { test } from "node:test";
import type { RandomSource } from "../dist/core.js";
import { ExoticCharacter, ReadableUniqueIdentifier } from "../dist/specials.js";

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

test("ExoticCharacter chooses from a requested set", () => {
  assert.equal(
    ExoticCharacter.randomCharacterFromSet("runic", fractionSource([0])),
    "ᚠ",
  );
});

test("ExoticCharacter preserves astral characters as one code point", () => {
  const character = ExoticCharacter.randomCharacter(fractionSource([0, 0]));
  assert.equal(character, "𐄚");
  assert.equal([...character].length, 1);
  assert.equal(character.length, 2);
});

test("ExoticCharacter rejects unknown set names", () => {
  assert.throws(
    () => ExoticCharacter.randomCharacterFromSet("invalid", fractionSource([0])),
    /Invalid character set requested/,
  );
});

test("ReadableUniqueIdentifier combines a seeded prefix with clock time", () => {
  const originalNow = Date.now;
  Date.now = () => Date.UTC(2001, 0, 1) + 1;
  try {
    assert.equal(
      ReadableUniqueIdentifier.makeIdentifier(fractionSource([0, 0, 0])),
      "abrupt_aardvark_RS",
    );
    assert.equal(
      ReadableUniqueIdentifier.makeIdentifier(fractionSource([0.9, 0, 0])),
      "abnormally_abashing_RS",
    );
  } finally {
    Date.now = originalNow;
  }
});
