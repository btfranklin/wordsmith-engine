import { choose, type RandomSource } from "./random.js";

const ARTICLES = ["a", "the"] as const;
const DETERMINERS = ["a", "the", "my", "your", "our", "her", "his"] as const;

export function selectArticle(
  rng: RandomSource,
  { isBeforeVowel }: { readonly isBeforeVowel: boolean },
): string {
  const article = choose(rng, ARTICLES);
  return article === "a" && isBeforeVowel ? "an" : article;
}

export function selectDeterminer(
  rng: RandomSource,
  { isBeforeVowel }: { readonly isBeforeVowel: boolean },
): string {
  const determiner = choose(rng, DETERMINERS);
  return determiner === "a" && isBeforeVowel ? "an" : determiner;
}
