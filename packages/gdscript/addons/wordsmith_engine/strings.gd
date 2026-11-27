extends RefCounted

const SMALL_WORDS := ["a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "per", "so", "the", "to", "up", "via", "vs", "with", "yet"]
const PUNCTUATION := "\"'“”‘’()[]{}.,;:!?/"
const VOWEL_PREFIXES := ["heir", "honest", "honor", "honour", "hour", "onei", "oner"]
const CONSONANT_PREFIXES := ["euro", "once", "one", "ufo", "unicorn", "unicycl", "uniform", "unilateral", "union", "unique", "unisex", "unison", "unit", "univ", "use", "user", "usual"]
static var _letters := RegEx.create_from_string("\\p{L}+")
static var _cased := RegEx.create_from_string("[\\p{Ll}\\p{Lu}\\p{Lt}]")


static func starts_with_vowel(value: String) -> bool:
	var first_word := _letters.search(value)
	if first_word == null:
		return false
	var word := first_word.get_string().to_lower()
	if word in ["herb", "herbs"]:
		return true
	for prefix in VOWEL_PREFIXES:
		if word.begins_with(prefix):
			return true
	for prefix in CONSONANT_PREFIXES:
		if word.begins_with(prefix):
			return false
	return word[0] in "aeiou"


static func _upper(character: String) -> String:
	# Godot uses simple Unicode case mappings. English text can contain sharp S.
	return "SS" if character == "ß" else character.to_upper()


static func first_upper(value: String) -> String:
	var found := _letters.search(value)
	if found == null:
		return value
	var index := found.get_start()
	return value.left(index) + _upper(value[index]) + value.substr(index + 1)


static func capitalized(value: String) -> String:
	var result := ""
	var start := true
	for character in value:
		if _cased.search(character) == null:
			result += character
			start = true
		else:
			result += _upper(character) if start else character.to_lower()
			start = false
	return result


static func _title_word(value: String) -> String:
	var found := _letters.search(value)
	if found != null and found.get_string().begins_with("mc") and found.get_string().length() >= 3:
		var start := found.get_start()
		return value.left(start) + "Mc" + _upper(value[start + 2]) + value.substr(start + 3)
	return first_upper(value)


static func title_case(value: String) -> String:
	var words := value.split(" ")
	var result := PackedStringArray()
	for index in words.size():
		var word := words[index]
		if word.is_empty():
			continue
		var start := 0
		var end := word.length()
		while start < end and word[start] in PUNCTUATION:
			start += 1
		while end > start and word[end - 1] in PUNCTUATION:
			end -= 1
		var middle := word.substr(start, end - start).to_lower()
		if index == 0 or index == words.size() - 1 or middle not in SMALL_WORDS:
			middle = _title_word(middle)
		result.append(word.left(start) + middle + word.substr(end))
	return " ".join(result)
