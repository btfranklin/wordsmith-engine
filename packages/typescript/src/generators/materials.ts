import materialNamePartsJson from "../assets/Material Name Parts.json" with {
  type: "json",
};

import { Component, choose, type RandomSource, weightedOneOf } from "../core.js";
import { AlienName, FantasyName, Surname } from "../names.js";
import { StatelessComponent } from "./support.js";

interface MaterialNameParts {
  readonly elementPrefixes: readonly string[];
  readonly elementMiddles: readonly string[];
  readonly mineralPrefixes: readonly string[];
  readonly mineralMiddles: readonly string[];
  readonly realElements: readonly string[];
  readonly elementSuffixes: readonly (readonly [number, string])[];
  readonly mineralSuffixes: readonly (readonly [number, string])[];
}

const MATERIAL_NAME_PARTS = materialNamePartsJson as unknown as MaterialNameParts;
const REAL_ELEMENTS = new Set(MATERIAL_NAME_PARTS.realElements);

class ElementalRoot extends Component {
  render(rng: RandomSource): string {
    return (
      choose(rng, MATERIAL_NAME_PARTS.elementPrefixes) +
      choose(rng, MATERIAL_NAME_PARTS.elementMiddles)
    );
  }
}

class MineralRoot extends Component {
  render(rng: RandomSource): string {
    return (
      choose(rng, MATERIAL_NAME_PARTS.mineralPrefixes) +
      choose(rng, MATERIAL_NAME_PARTS.mineralMiddles)
    );
  }
}

function cleanMaterialRoot(value: string): string | undefined {
  const ascii = [...value.normalize("NFKD")]
    .filter((character) => (character.codePointAt(0) ?? 128) <= 127)
    .join("");
  const root = ascii.toLowerCase().replace(/[^a-z]/g, "");
  if (root.length < 3 || root.length > 10) return undefined;
  if (![..."aeiou"].some((vowel) => root.includes(vowel))) return undefined;
  if (root.includes("ii") || root.includes("yy")) return undefined;
  if (/[bcdfghjklmnpqrstvwxz]{5,}/.test(root)) return undefined;
  return root;
}

function makeMaterialRoot(
  rng: RandomSource,
  source: Component,
  fallback: string,
): string {
  for (let attempt = 0; attempt < 24; attempt += 1) {
    const root = cleanMaterialRoot(source.render(rng));
    if (root !== undefined) return root;
  }
  return fallback;
}

function elementRootSource(): Component {
  return weightedOneOf(
    [5, new ElementalRoot()],
    [
      1,
      new AlienName({ syllableCount: 2, allowHyphen: false, allowApostrophe: false }),
    ],
    [
      1,
      new FantasyName({
        syllableCount: 2,
        allowHyphen: false,
        allowApostrophe: false,
      }),
    ],
    [1, new Surname()],
  );
}

function mineralRootSource(): Component {
  return weightedOneOf(
    [4, new MineralRoot()],
    [
      2,
      new FantasyName({
        syllableCount: 2,
        allowHyphen: false,
        allowApostrophe: false,
      }),
    ],
    [1, new Surname()],
  );
}

function elementSuffix(): Component {
  return weightedOneOf(...MATERIAL_NAME_PARTS.elementSuffixes);
}

function joinElementSuffix(originalRoot: string, suffix: string): string {
  let root = originalRoot;
  if (suffix === "ium") {
    if (root.endsWith("on")) root = root.slice(0, -2);
    while (root.length > 2 && /[aeiy]$/.test(root)) root = root.slice(0, -1);
    return root + suffix;
  }
  if (suffix === "gen") return root + (/[aeiou]$/.test(root) ? "gen" : "ogen");
  if (root.endsWith("e")) root = root.slice(0, -1);
  return root.endsWith(suffix) ? root : root + suffix;
}

export class FictionalElementName extends StatelessComponent {
  render(rng: RandomSource): string {
    for (let attempt = 0; attempt < 16; attempt += 1) {
      const root = makeMaterialRoot(rng, elementRootSource(), "lumin");
      const result = joinElementSuffix(root, elementSuffix().render(rng));
      if (!REAL_ELEMENTS.has(result)) return result;
    }
    return "luminum";
  }
}

function mineralSuffix(): Component {
  return weightedOneOf(...MATERIAL_NAME_PARTS.mineralSuffixes);
}

function joinMineralSuffix(originalRoot: string, originalSuffix: string): string {
  let root = originalRoot;
  let suffix = originalSuffix;
  if ((suffix === "ite" || suffix === "ine") && /[eiy]$/.test(root)) {
    root = root.slice(0, -1);
  }
  if (root.endsWith(suffix)) return root;
  if (root.at(-1) === suffix[0]) suffix = suffix.slice(1);
  return root + suffix;
}

export class FictionalMineralName extends StatelessComponent {
  render(rng: RandomSource): string {
    const root = makeMaterialRoot(rng, mineralRootSource(), "aurel");
    return joinMineralSuffix(root, mineralSuffix().render(rng));
  }
}
