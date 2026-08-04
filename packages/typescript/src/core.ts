import { selectArticle, selectDeterminer } from "./core-grammar.js";
import { choose, type RandomSource, randomBoolean, randomFraction } from "./random.js";
import { capitalized, firstUpper, startsWithVowel, titleCase } from "./strings.js";

export type { RandomSource } from "./random.js";
export { choose, randomBoolean } from "./random.js";

export type ComponentLike = Component | string;
export type RenderFunction = (rng: RandomSource) => string;

export abstract class Component {
  abstract render(rng: RandomSource): string;

  capitalized(): Component {
    return component((rng) => capitalized(this.render(rng)));
  }

  firstUpper(): Component {
    return component((rng) => firstUpper(this.render(rng)));
  }

  titleCase(): Component {
    return component((rng) => titleCase(this.render(rng)));
  }

  prefixedByArticle(): Component {
    return component((rng) => {
      const rendered = this.render(rng);
      const article = selectArticle(rng, {
        isBeforeVowel: startsWithVowel(rendered),
      });
      return `${article} ${rendered}`;
    });
  }

  prefixedByDeterminer(): Component {
    return component((rng) => {
      const rendered = this.render(rng);
      const determiner = selectDeterminer(rng, {
        isBeforeVowel: startsWithVowel(rendered),
      });
      return `${determiner} ${rendered}`;
    });
  }

  possessiveForm(): Component {
    return component((rng) => {
      const rendered = this.render(rng);
      return rendered.endsWith("s") ? `${rendered}'` : `${rendered}'s`;
    });
  }
}

class FunctionComponent extends Component {
  readonly #renderFunction: RenderFunction;

  constructor(renderFunction: RenderFunction) {
    super();
    this.#renderFunction = renderFunction;
    Object.freeze(this);
  }

  render(rng: RandomSource): string {
    const rendered = this.#renderFunction(rng);
    if (typeof rendered !== "string") {
      throw new TypeError("Components must render strings.");
    }
    return rendered;
  }
}

export function component(renderFunction: RenderFunction): Component {
  if (typeof renderFunction !== "function") {
    throw new TypeError("component requires a render function.");
  }
  return new FunctionComponent(renderFunction);
}

export function literal(value: string): Component {
  if (typeof value !== "string") {
    throw new TypeError("Literal values must be strings.");
  }
  return component(() => value);
}

export function empty(): Component {
  return literal("");
}

function coerce(value: ComponentLike): Component {
  if (value instanceof Component) {
    return value;
  }
  if (typeof value === "string") {
    return literal(value);
  }
  throw new TypeError("Component values must be strings or Components.");
}

export function join(parts: readonly ComponentLike[], separator: string): Component {
  if (!Array.isArray(parts)) {
    throw new TypeError("join requires an array of parts.");
  }
  if (typeof separator !== "string") {
    throw new TypeError("join requires a string separator.");
  }
  const snapshot = parts.map(coerce);
  return component((rng) => {
    const rendered: string[] = [];
    for (const part of snapshot) {
      const value = part.render(rng);
      if (value !== "") {
        rendered.push(value);
      }
    }
    return rendered.join(separator);
  });
}

export function concat(...parts: readonly ComponentLike[]): Component {
  return join(parts, "");
}

export function ws(
  strings: TemplateStringsArray,
  ...values: readonly ComponentLike[]
): Component {
  const parts: ComponentLike[] = [];
  for (let index = 0; index < strings.length; index += 1) {
    parts.push(strings[index] as string);
    if (index < values.length) {
      parts.push(values[index] as ComponentLike);
    }
  }
  return concat(...parts);
}

export function oneOf(...options: readonly ComponentLike[]): Component {
  if (options.length === 0) {
    throw new RangeError("oneOf requires at least one option.");
  }
  const snapshot = options.map(coerce);
  return component((rng) => choose(rng, snapshot).render(rng));
}

export type WeightedOption = readonly [weight: number, option: ComponentLike];

export function weightedOneOf(...pairs: readonly WeightedOption[]): Component {
  if (pairs.length === 0) {
    throw new RangeError("weightedOneOf requires at least one option.");
  }
  const snapshot = pairs.map(([weight, option]) => {
    if (!Number.isFinite(weight) || weight < 0) {
      throw new RangeError("Weights must be finite and non-negative.");
    }
    return [weight, coerce(option)] as const;
  });
  const total = snapshot.reduce((sum, [weight]) => sum + weight, 0);
  if (!(total > 0) || !Number.isFinite(total)) {
    throw new RangeError("weightedOneOf requires a finite positive total weight.");
  }

  return component((rng) => {
    const target = randomFraction(rng) * total;
    let cumulative = 0;
    for (const [weight, option] of snapshot) {
      cumulative += weight;
      if (target < cumulative) {
        return option.render(rng);
      }
    }
    return (snapshot.at(-1) as readonly [number, Component])[1].render(rng);
  });
}

export function either(
  first: ComponentLike,
  second: ComponentLike,
  firstProbability = 0.5,
): Component {
  if (
    !Number.isFinite(firstProbability) ||
    firstProbability < 0 ||
    firstProbability > 1
  ) {
    throw new RangeError("First option probability must be in the range 0 to 1.");
  }
  const firstComponent = coerce(first);
  const secondComponent = coerce(second);
  return component((rng) =>
    (randomBoolean(rng, firstProbability) ? firstComponent : secondComponent).render(
      rng,
    ),
  );
}

export interface MaybeOptions {
  readonly probability?: number;
}

function isMaybeOptions(value: unknown): value is MaybeOptions {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    Object.getPrototypeOf(value) !== Object.prototype
  ) {
    return false;
  }
  return Object.keys(value).every((key) => key === "probability");
}

export function maybe(
  ...partsAndOptions: readonly [ComponentLike, ...(ComponentLike | MaybeOptions)[]]
): Component {
  const values: (ComponentLike | MaybeOptions)[] = [...partsAndOptions];
  const possibleOptions = values.at(-1);
  const hasOptions = isMaybeOptions(possibleOptions);
  const options = hasOptions ? (values.pop() as MaybeOptions) : undefined;
  const probability = options?.probability ?? 0.5;
  if (!Number.isFinite(probability) || probability < 0 || probability > 1) {
    throw new RangeError("Probability must be in the range 0 to 1.");
  }
  const normalized = concat(...(values as ComponentLike[]));
  return component((rng) =>
    randomBoolean(rng, probability) ? normalized.render(rng) : "",
  );
}
