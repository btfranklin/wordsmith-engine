import assert from "node:assert/strict";
import { test } from "node:test";
import {
  choose,
  type RandomSource,
  randomBoolean,
  randomFraction,
  seededRandom,
} from "../dist/random.js";

test("seededRandom has stable golden sequences", () => {
  const rng = seededRandom("5343");
  assert.deepEqual(
    Array.from({ length: 5 }, () => rng.random()),
    [
      0.7544748149812222, 0.6677223918959498, 0.16107654059305787, 0.6574176042340696,
      0.4643204091116786,
    ],
  );
});

test("numeric seeds normalize to decimal strings", () => {
  const numberSource = seededRandom(5343);
  const stringSource = seededRandom("5343");
  assert.deepEqual(
    Array.from({ length: 20 }, () => numberSource.random()),
    Array.from({ length: 20 }, () => stringSource.random()),
  );
});

test("seededRandom accepts opaque strings and rejects unsafe numbers", () => {
  assert.doesNotThrow(() => seededRandom(""));
  assert.doesNotThrow(() => seededRandom("world/ship"));
  for (const seed of [
    Number.NaN,
    Number.POSITIVE_INFINITY,
    1.5,
    Number.MAX_SAFE_INTEGER + 1,
  ]) {
    assert.throws(() => seededRandom(seed), /finite safe integers/);
  }
});

test("random helpers validate custom sources", () => {
  for (const value of [-0.1, 1, Number.NaN, Number.POSITIVE_INFINITY]) {
    assert.throws(() => randomFraction({ random: () => value }), /\[0, 1\)/);
  }
  assert.throws(() => choose({ random: () => 0 }, []), /empty/);
});

test("probability extremes consume one draw", () => {
  let draws = 0;
  const rng: RandomSource = {
    random: () => {
      draws += 1;
      return 0.25;
    },
  };
  assert.equal(randomBoolean(rng, 0), false);
  assert.equal(randomBoolean(rng, 1), true);
  assert.equal(draws, 2);
});
