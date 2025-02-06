extends Node2D

@export var character_scene: PackedScene
var character_data = []
var windowSize: Vector2

func _ready():
	load_character_data()
	windowSize = get_viewport().size
	spawn_characters()

func load_character_data():
	var file = FileAccess.open("res://data/characters.json", FileAccess.READ)
	if file:
		var json_text = file.get_as_text()
		character_data = JSON.parse_string(json_text)
		file.close()

func spawn_characters():
	for i in range(character_data.size()):
		@warning_ignore("integer_division")
		var characterSpace = windowSize.x / 8
		var data = character_data[i]
		if data["alignment"] == "Sin":
			var character_instance = spawn_character(Vector2(characterSpace + i * characterSpace, windowSize.y / 3), data)
			add_child(character_instance)
		if data["alignment"] == "Virtue":
			var character_instance = spawn_character(Vector2(characterSpace + (i - 7) * characterSpace, windowSize.y / 3 * 2), data)
			add_child(character_instance)

func spawn_character(spawn_position: Vector2, data: Dictionary):
	var character_instance = character_scene.instantiate()
	character_instance.position = spawn_position  # Use the renamed parameter
	character_instance.character_name = data["name"]
	character_instance.aspect = data["aspect"]
	character_instance.abugida_name = data["abugida_name"]
	character_instance.abugida_aspect = data["abugida_aspect"]
	character_instance.description = data["description"]
	character_instance.colour = data["colour"]
	character_instance.animal = data["animal"]
	character_instance.weapon = data["weapon"]
	character_instance.power = data["power"]
	character_instance.species = data["species"]
	character_instance.alignment = data["alignment"]
	character_instance.rank = data["rank"]
	character_instance.epithet = data["epithet"]
	character_instance.edictDef = data["edictDef"]
	#character_instance. = data[""]
	
	return character_instance
