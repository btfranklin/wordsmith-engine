extends "support.gd"

const Strings := preload("strings.gd")
const Support := preload("support.gd")


@abstract class RandomSource extends RefCounted:
	@abstract func random() -> float


class SeededSource extends RandomSource:
	var _rng := RandomNumberGenerator.new()

	func _init(value: int):
		_rng.seed = value

	func random() -> float:
		return _rng.randi() / 4294967296.0


@abstract class Component extends RefCounted:
	@abstract func render(rng) -> String

	func capitalized() -> Component:
		return Transformed.new(self, Strings.capitalized)

	func first_upper() -> Component:
		return Transformed.new(self, Strings.first_upper)

	func title_case() -> Component:
		return Transformed.new(self, Strings.title_case)

	func possessive_form() -> Component:
		return Transformed.new(self, func(value): return value + ("'" if value.ends_with("s") else "'s"))

	func prefixed_by_article() -> Component:
		return Prefixed.new(self, Support.select_article)

	func prefixed_by_determiner() -> Component:
		return Prefixed.new(self, Support.select_determiner)


class Transformed extends Component:
	var _part: Component
	var _transform: Callable

	func _init(part: Component, transform: Callable):
		_part = part
		_transform = transform

	func render(rng) -> String:
		return _transform.call(_part.render(rng))


class Prefixed extends Component:
	var _part: Component
	var _select_prefix: Callable

	func _init(part: Component, select_prefix: Callable):
		_part = part
		_select_prefix = select_prefix

	func render(rng) -> String:
		var value := _part.render(rng)
		var vowel := Strings.starts_with_vowel(value)
		var prefix: String = _select_prefix.call(rng, vowel)
		return prefix + " " + value


class Callback extends Component:
	var _callback: Callable

	func _init(callback: Callable):
		_callback = callback

	func render(rng) -> String:
		return _callback.call(rng)


class WeightedTable extends RefCounted:
	var _weights: Array[float] = []
	var _values: Array = []
	var _total := 0.0

	static func create(pairs: Array) -> WeightedTable:
		var table := WeightedTable.new()
		for pair in pairs:
			if not (pair is Array and pair.size() == 2 and (pair[0] is int or pair[0] is float)):
				push_error("Each weighted choice requires a numeric weight and a value.")
				return null
			var weight := float(pair[0])
			if not is_finite(weight) or weight < 0:
				push_error("Weights must be finite and non-negative.")
				return null
			if weight > 0:
				table._weights.append(weight)
				table._values.append(pair[1])
				table._total += weight
		if not is_finite(table._total) or table._total <= 0:
			push_error("Weighted choices require a finite positive total.")
			return null
		if table._total <= 2.2250738585072014e-308:
			var scale: float = table._weights.max()
			table._total = 0.0
			for index in table._weights.size():
				table._weights[index] /= scale
				table._total += table._weights[index]
		return table

	func pick(fraction: float) -> Variant:
		if not is_finite(fraction) or fraction < 0 or fraction >= 1:
			push_error("Expected a fraction in [0, 1).")
			return null
		var target := fraction * _total
		var cumulative := 0.0
		for index in _weights.size():
			cumulative += _weights[index]
			if target < cumulative:
				return _values[index]
		return _values.back()


static func seeded_random(value: int) -> RandomSource:
	return SeededSource.new(value)


static func component(callback: Callable) -> Component:
	if not callback.is_valid():
		push_error("A component needs a valid render function.")
		return null
	return Callback.new(callback)


static func literal(value: String) -> Component:
	return Callback.new(func(_rng): return value)


static func empty() -> Component:
	return literal("")


static func _parts(values: Array) -> Array[Component]:
	var parts: Array[Component] = []
	for value in values:
		if value is Component:
			parts.append(value)
		elif value is String:
			parts.append(literal(value))
		else:
			push_error("A component part must be a string or Component.")
			return []
	return parts


static func join(values: Array, separator: String) -> Component:
	var parts := _parts(values)
	if parts.size() != values.size():
		return null
	return Callback.new(func(rng):
		var rendered := PackedStringArray()
		for part in parts:
			var value := part.render(rng)
			if value != "":
				rendered.append(value)
		return separator.join(rendered)
	)


static func concat(parts: Array) -> Component:
	return join(parts, "")


static func one_of(values: Array) -> Component:
	if values.is_empty():
		push_error("one_of requires choices.")
		return null
	var parts := _parts(values)
	if parts.is_empty():
		return null
	return Callback.new(func(rng): return choose(rng, parts).render(rng))


static func weighted_one_of(pairs: Array) -> Component:
	var options := []
	for pair in pairs:
		if not (pair is Array and pair.size() == 2):
			push_error("Each weighted choice needs a weight and a part.")
			return null
		var parts := _parts([pair[1]])
		if parts.is_empty():
			return null
		options.append([pair[0], parts[0]])
	var table := WeightedTable.create(options)
	if table == null:
		return null
	return Callback.new(func(rng): return table.pick(random_fraction(rng)).render(rng))


static func either(first: Variant, second: Variant, probability: float = 0.5) -> Component:
	if not _valid_probability(probability):
		push_error("Probability must be between zero and one.")
		return null
	var parts := _parts([first, second])
	if parts.is_empty():
		return null
	return Callback.new(func(rng):
		return parts[0 if random_boolean(rng, probability) else 1].render(rng)
	)


static func maybe(parts: Array, probability: float = 0.5) -> Component:
	var part := concat(parts)
	if part == null:
		return null
	return either(part, "", probability)
