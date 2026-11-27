extends Node


class Harbor extends Wordsmith.Component:
	func render(_rng) -> String:
		return "Phoenix Harbor"


func _ready() -> void:
	var rng = Wordsmith.seeded_random(5343)
	var ship = Wordsmith.NauticalShipName.new()
	var name: String = ship.render(rng)
	if name.is_empty() or name != ship.render(Wordsmith.seeded_random(5343)):
		get_tree().quit(1)
		return
	print(Wordsmith.join([name, Harbor.new()], " of ").render(rng))
	get_tree().quit()
