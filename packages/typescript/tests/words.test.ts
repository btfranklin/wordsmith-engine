import assert from "node:assert/strict";
import { test } from "node:test";
import type { RandomSource } from "../dist/random.js";
import {
  Adjective,
  Adverb,
  Article,
  ChemicalCompoundName,
  Determiner,
  Noun,
  NounForm,
  PrimitiveWeapon,
  Pronoun,
  Verb,
  VerbTense,
  VillainousPersonNoun,
} from "../dist/words.js";

const source = (fraction: number): RandomSource => ({ random: () => fraction });

test("asset-backed words select canonical rows", () => {
  assert.equal(new Adjective().render(source(0)), "abrupt");
  assert.equal(new Adverb().render(source(0)), "abnormally");
  assert.equal(new ChemicalCompoundName().render(source(0)), "actinium(III) chloride");
  assert.equal(new Noun().render(source(0)), "aardvark");
  assert.equal(new Noun({ form: NounForm.plural }).render(source(0)), "aardvarks");
  assert.equal(new Verb({ tense: VerbTense.present }).render(source(0)), "abashes");
});

test("word enums and components are immutable", () => {
  assert.ok(Object.isFrozen(NounForm));
  assert.ok(Object.isFrozen(VerbTense));
  assert.ok(Object.isFrozen(new Noun()));
  assert.throws(() => new Noun({ form: "dual" as NounForm }), /Invalid noun form/);
  assert.throws(() => new Verb({ tense: "future" as VerbTense }), /Invalid verb tense/);
});

test("pronouns preserve the person and number matrix", () => {
  assert.equal(
    new Pronoun({ isSingular: true, isThirdPerson: true }).render(source(0)),
    "he",
  );
  assert.equal(
    new Pronoun({ isSingular: false, isThirdPerson: true }).render(source(0)),
    "they",
  );
  assert.equal(
    new Pronoun({ isSingular: true, isThirdPerson: false }).render(source(0)),
    "I",
  );
  assert.equal(
    new Pronoun({ isSingular: false, isThirdPerson: false }).render(source(0)),
    "we",
  );
});

test("articles and determiners apply vowel context after selection", () => {
  assert.equal(new Article({ isBeforeVowel: true }).render(source(0)), "an");
  assert.equal(new Article().render(source(0)), "a");
  assert.equal(new Determiner({ isBeforeVowel: true }).render(source(0)), "an");
});

test("handwritten pluralization rules match Python", () => {
  assert.equal(
    new VillainousPersonNoun({ isPlural: true }).render(source(0.4945)),
    "lowlifes",
  );
  assert.equal(
    new VillainousPersonNoun({ isPlural: true }).render(source(0.9054)),
    "thieves",
  );
  assert.equal(
    new VillainousPersonNoun({ isPlural: true }).render(source(0.3849)),
    "highwaymen",
  );
  assert.equal(
    new PrimitiveWeapon({ isPlural: true }).render(source(0.2928)),
    "knives",
  );
  assert.equal(new PrimitiveWeapon({ isPlural: true }).render(source(0.65)), "spears");
});

test("public word boolean options are validated at runtime", () => {
  const invalidFactories = [
    () =>
      new Pronoun({
        isSingular: 1 as unknown as boolean,
        isThirdPerson: false,
      }),
    () =>
      new Pronoun({
        isSingular: true,
        isThirdPerson: "no" as unknown as boolean,
      }),
    () => new Article({ isBeforeVowel: 1 as unknown as boolean }),
    () => new Determiner({ isBeforeVowel: "yes" as unknown as boolean }),
    () => new VillainousPersonNoun({ isPlural: 1 as unknown as boolean }),
    () => new PrimitiveWeapon({ isPlural: "yes" as unknown as boolean }),
    () => new Pronoun({} as { isSingular: boolean; isThirdPerson: boolean }),
    () => new VillainousPersonNoun({} as { isPlural: boolean }),
  ] as const;

  for (const makeComponent of invalidFactories) {
    assert.throws(makeComponent, /must be a boolean/);
  }
});
