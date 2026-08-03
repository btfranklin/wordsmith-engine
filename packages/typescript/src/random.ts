export type Seed = string | number;

export interface RandomSource {
  random(): number;
}

const UINT32_RANGE = 0x1_0000_0000;

function normalizeSeed(seed: Seed): string {
  if (typeof seed === "string") {
    return seed;
  }
  if (!Number.isFinite(seed) || !Number.isSafeInteger(seed)) {
    throw new RangeError("Numeric seeds must be finite safe integers.");
  }
  return String(seed);
}

function cyrb128(value: string): [number, number, number, number] {
  let h1 = 1_779_033_703;
  let h2 = 3_144_134_277;
  let h3 = 1_013_904_242;
  let h4 = 2_773_480_662;

  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    h1 = h2 ^ Math.imul(h1 ^ code, 597_399_067);
    h2 = h3 ^ Math.imul(h2 ^ code, 2_869_860_233);
    h3 = h4 ^ Math.imul(h3 ^ code, 951_274_213);
    h4 = h1 ^ Math.imul(h4 ^ code, 2_716_044_179);
  }

  h1 = Math.imul(h3 ^ (h1 >>> 18), 597_399_067);
  h2 = Math.imul(h4 ^ (h2 >>> 22), 2_869_860_233);
  h3 = Math.imul(h1 ^ (h3 >>> 17), 951_274_213);
  h4 = Math.imul(h2 ^ (h4 >>> 19), 2_716_044_179);
  return [(h1 ^ h2 ^ h3 ^ h4) >>> 0, (h2 ^ h1) >>> 0, (h3 ^ h1) >>> 0, (h4 ^ h1) >>> 0];
}

function rotateLeft(value: number, count: number): number {
  return ((value << count) | (value >>> (32 - count))) >>> 0;
}

class Xoshiro128StarStar implements RandomSource {
  #state0: number;
  #state1: number;
  #state2: number;
  #state3: number;

  constructor(seed: string) {
    [this.#state0, this.#state1, this.#state2, this.#state3] = cyrb128(seed);
    if ((this.#state0 | this.#state1 | this.#state2 | this.#state3) === 0) {
      this.#state0 = 0x9e37_79b9;
    }
    Object.freeze(this);
  }

  random(): number {
    const result = Math.imul(rotateLeft(Math.imul(this.#state1, 5), 7), 9) >>> 0;
    const temporary = (this.#state1 << 9) >>> 0;

    this.#state2 = (this.#state2 ^ this.#state0) >>> 0;
    this.#state3 = (this.#state3 ^ this.#state1) >>> 0;
    this.#state1 = (this.#state1 ^ this.#state2) >>> 0;
    this.#state0 = (this.#state0 ^ this.#state3) >>> 0;
    this.#state2 = (this.#state2 ^ temporary) >>> 0;
    this.#state3 = rotateLeft(this.#state3, 11);

    return result / UINT32_RANGE;
  }
}

export function seededRandom(seed: Seed): RandomSource {
  return new Xoshiro128StarStar(normalizeSeed(seed));
}

export function randomFraction(rng: RandomSource): number {
  const fraction = rng.random();
  if (!Number.isFinite(fraction) || fraction < 0 || fraction >= 1) {
    throw new RangeError("Random sources must return finite values in [0, 1).");
  }
  return fraction;
}

export function choose<Value>(rng: RandomSource, values: readonly Value[]): Value {
  if (values.length === 0) {
    throw new RangeError("Cannot choose from an empty collection.");
  }
  return values[Math.floor(randomFraction(rng) * values.length)] as Value;
}

export function randomBoolean(rng: RandomSource, probability = 0.5): boolean {
  if (!Number.isFinite(probability) || probability < 0 || probability > 1) {
    throw new RangeError("Probability must be in the range 0 to 1.");
  }
  return randomFraction(rng) < probability;
}
