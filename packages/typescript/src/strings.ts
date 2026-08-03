const LETTER = /\p{L}/u;
const CASED_LETTER = /[\p{Ll}\p{Lu}\p{Lt}]/u;
const VOWELS = new Set(["a", "e", "i", "o", "u"]);

export function startsWithVowel(text: string): boolean {
  const letters: string[] = [];
  for (const character of text.trim()) {
    if (LETTER.test(character)) {
      letters.push(character);
    } else if (letters.length > 0) {
      break;
    }
  }
  if (letters.length === 0) {
    return false;
  }

  const word = letters.join("").toLowerCase();
  if (
    ["honest", "honor", "honour", "hour", "heir", "herb"].some((prefix) =>
      word.startsWith(prefix),
    )
  ) {
    return true;
  }
  if (
    ["uni", "use", "user", "ufo", "euro", "one", "once"].some((prefix) =>
      word.startsWith(prefix),
    )
  ) {
    return false;
  }
  return VOWELS.has(word[0] ?? "");
}

export function firstUpper(text: string): string {
  const match = LETTER.exec(text);
  if (match?.index === undefined) {
    return text;
  }
  const character = match[0];
  return `${text.slice(0, match.index)}${character.toUpperCase()}${text.slice(match.index + character.length)}`;
}

export function capitalized(text: string): string {
  let afterUncased = true;
  let result = "";
  for (const character of text) {
    if (CASED_LETTER.test(character)) {
      result += afterUncased ? character.toUpperCase() : character.toLowerCase();
      afterUncased = false;
    } else {
      result += character;
      afterUncased = true;
    }
  }
  return result;
}

const SMALL_WORDS = new Set([
  "a",
  "an",
  "and",
  "as",
  "at",
  "but",
  "by",
  "for",
  "in",
  "nor",
  "of",
  "on",
  "or",
  "per",
  "so",
  "the",
  "to",
  "up",
  "via",
  "vs",
  "with",
  "yet",
]);
const PUNCTUATION = new Set([...`"'“”‘’()[]{}.,;:!?/`]);

export function titleCase(text: string): string {
  const words = text.split(" ");
  const lastIndex = words.length - 1;
  const result: string[] = [];

  for (const [index, word] of words.entries()) {
    if (word === "") {
      continue;
    }
    let core = word;
    let leading = "";
    let trailing = "";
    while (core.length > 0 && PUNCTUATION.has(core[0] as string)) {
      leading += core[0];
      core = core.slice(1);
    }
    while (core.length > 0 && PUNCTUATION.has(core.at(-1) as string)) {
      trailing = `${core.at(-1)}${trailing}`;
      core = core.slice(0, -1);
    }
    if (core === "") {
      result.push(word);
      continue;
    }

    const lower = core.toLowerCase();
    const transformed =
      index !== 0 && index !== lastIndex && SMALL_WORDS.has(lower)
        ? lower
        : firstUpper(lower);
    result.push(`${leading}${transformed}${trailing}`);
  }
  return result.join(" ");
}
