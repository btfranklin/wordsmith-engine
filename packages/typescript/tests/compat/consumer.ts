import {
  Adjective,
  type Component,
  component,
  concat,
  join,
  Noun,
  NounForm,
  type RandomSource,
  type Seed,
  seededRandom,
  ws,
} from "wordsmith-engine";

const seed: Seed = "compatibility";
const rng: RandomSource = seededRandom(seed);
const custom: Component = component(() => "custom");
const noun = new Noun({ form: NounForm.plural });
const outputs: string[] = [
  new Adjective().render(rng),
  join([custom, noun], " ").titleCase().render(rng),
  concat("prefix-", noun).render(rng),
  ws`The ${noun}`.render(rng),
];

void outputs;
