extends RefCounted

const Core = preload("../core.gd")
const Names = preload("../names.gd")
const NAME_OPTIONS = {"syllable_count": 2, "allow_hyphen": false, "allow_apostrophe": false}


class MaterialRoot:
	static var _consonants := RegEx.create_from_string("[bcdfghjklmnpqrstvwxz]{5,}")
	static var _non_letters := RegEx.create_from_string("[^a-z]")

	static func draw(rng, source: Core.Component, fallback: String) -> String:
		var text_server := TextServerManager.get_primary_interface()
		for attempt in 24:
			var ascii := text_server.strip_diacritics(source.render(rng)).to_lower()
			var root := _non_letters.sub(ascii, "", true)
			if root.length() < 3 or root.length() > 10:
				continue
			if "ii" in root or "yy" in root or _consonants.search(root) != null:
				continue
			for vowel in "aeiou":
				if vowel in root:
					return root
		return fallback


	static func joined_element(root: String, suffix: String) -> String:
		if suffix == "ium":
			root = root.trim_suffix("on")
			while root.length() > 2 and root[-1] in "aeiy":
				root = root.left(-1)
			return root + suffix
		if suffix == "gen":
			return root + ("gen" if root[-1] in "aeiou" else "ogen")
		root = root.trim_suffix("e")
		return root if root.ends_with(suffix) else root + suffix


class FictionalElementName extends Core.Component:
	func render(rng) -> String:
		var data = Core.asset("Material Name Parts")
		var base = Core.concat([Core.one_of(data.elementPrefixes), Core.one_of(data.elementMiddles)])
		var source = Core.weighted_one_of([
			[5, base],
			[1, Names.AlienName.new(NAME_OPTIONS)],
			[1, Names.FantasyName.new(NAME_OPTIONS)],
			[1, Names.Surname.new()],
		])
		var suffixes = Core.weighted_one_of(data.elementSuffixes)
		for attempt in 16:
			var root = MaterialRoot.draw(rng, source, "lumin")
			var result = MaterialRoot.joined_element(root, suffixes.render(rng))
			if result not in data.realElements:
				return result
		return "luminum"


class FictionalMineralName extends Core.Component:
	func render(rng) -> String:
		var data = Core.asset("Material Name Parts")
		var base = Core.concat([Core.one_of(data.mineralPrefixes), Core.one_of(data.mineralMiddles)])
		var source = Core.weighted_one_of(
			[[4, base], [2, Names.FantasyName.new(NAME_OPTIONS)], [1, Names.Surname.new()]]
		)
		var root = MaterialRoot.draw(rng, source, "aurel")
		var suffix = Core.weighted_one_of(data.mineralSuffixes).render(rng)
		if suffix in ["ite", "ine"] and root[-1] in "eiy":
			root = root.left(-1)
		if root.ends_with(suffix):
			return root
		if root[-1] == suffix[0]:
			suffix = suffix.substr(1)
		return root + suffix
