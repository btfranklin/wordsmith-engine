extends RefCounted

static var _assets := {}
static var _asset_mutex := Mutex.new()


static func _valid_fraction(value: float) -> bool:
	return is_finite(value) and value >= 0 and value < 1


static func random_fraction(rng) -> float:
	var value = rng.random()
	if not (value is int or value is float) or not _valid_fraction(value):
		push_error("Random sources must return a number in [0, 1).")
		return NAN
	return value


static func choose(rng, values: Array) -> Variant:
	if values.is_empty():
		push_error("Cannot choose from an empty collection.")
		return null
	var fraction := random_fraction(rng)
	if is_nan(fraction):
		return null
	return values[floori(fraction * values.size())]


static func _valid_probability(probability: float) -> bool:
	return is_finite(probability) and probability >= 0 and probability <= 1


static func random_boolean(rng, probability: float = 0.5) -> bool:
	if not _valid_probability(probability):
		push_error("Probability must be between zero and one.")
		return false
	return random_fraction(rng) < probability


static func asset(asset_name: String) -> Variant:
	_asset_mutex.lock()
	if not _assets.has(asset_name):
		var path := "res://addons/wordsmith_engine/assets/%s.json" % asset_name
		var resource := load(path) as JSON
		if resource == null or resource.data == null:
			_asset_mutex.unlock()
			push_error("Failed to load Wordsmith asset " + path)
			return null
		_freeze_data(resource.data)
		_assets[asset_name] = resource.data
	var data: Variant = _assets[asset_name]
	_asset_mutex.unlock()
	return data


static func _freeze_data(value: Variant) -> void:
	if value is Dictionary:
		for child in value.values():
			_freeze_data(child)
		value.make_read_only()
	elif value is Array:
		for child in value:
			_freeze_data(child)
		value.make_read_only()


static func select_article(rng, is_before_vowel: bool) -> String:
	var value: String = choose(rng, ["a", "the"])
	return "an" if value == "a" and is_before_vowel else value


static func select_determiner(rng, is_before_vowel: bool) -> String:
	var value: String = choose(rng, ["a", "the", "my", "your", "our", "her", "his"])
	return "an" if value == "a" and is_before_vowel else value
