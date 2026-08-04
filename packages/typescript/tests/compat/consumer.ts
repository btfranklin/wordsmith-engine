import {
  Adjective,
  type AlienNameOptions,
  type AncientGivenNameOptions,
  type Component,
  type ComponentLike,
  component,
  concat,
  type FantasyNameOptions,
  type GivenNameOptions,
  join,
  type MaybeOptions,
  Noun,
  NounForm,
  type PersonNameOptions,
  type RandomSource,
  type RenderFunction,
  type Seed,
  seededRandom,
  type WeightedOption,
  ws,
} from "wordsmith-engine";

const seed: Seed = "compatibility";
const rng: RandomSource = seededRandom(seed);
const custom: Component = component(() => "custom");
const componentLike: ComponentLike = custom;
const renderFunction: RenderFunction = () => "typed";
const weightedOption: WeightedOption = [1, componentLike];
const maybeOptions: MaybeOptions = { probability: 0.5 };
const alienOptions: AlienNameOptions = { syllableCount: 3 };
const ancientOptions: AncientGivenNameOptions = {};
const fantasyOptions: FantasyNameOptions = { syllableCount: 3 };
const givenOptions: GivenNameOptions = {};
const personOptions: PersonNameOptions = {};
const noun = new Noun({ form: NounForm.plural });
const outputs: string[] = [
  new Adjective().render(rng),
  join([custom, noun], " ").titleCase().render(rng),
  concat("prefix-", noun).render(rng),
  ws`The ${noun}`.render(rng),
];

void [
  outputs,
  renderFunction,
  weightedOption,
  maybeOptions,
  alienOptions,
  ancientOptions,
  fantasyOptions,
  givenOptions,
  personOptions,
];
