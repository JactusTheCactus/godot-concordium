extends Area2D

@export var character_name: String
@export var aspect: String
@export var abugida_name: String
@export var abugida_aspect: String
@export var description: String
@export var colour: String
@export var animal: String
@export var weapon: String
@export var power: String
@export var species: String
@export var alignment: String
@export var rank: String
@export var epithet: String
@export var edictDef: String

@onready var abugida: Dictionary = {
	"name": abugida_name,
	"aspect": abugida_aspect
}

@onready var textBox = get_node('/root/main/player/Sprite2D/text/dialogueBox/textBox')

var player_nearby = false
var ui : Control = null
var text_box : RichTextLabel = null

@warning_ignore("shadowed_variable")
func set_child_texture(alignment,head):
	var head_sprite = $headSprite as Sprite2D
	var weapon_sprite = $weaponSprite as Sprite2D
	if alignment and head:
		if head_sprite:
			var texturePath = "res://assets/heads/%s/%s.png" % [alignment,head]
			var new_texture = load(texturePath)
			head_sprite.texture = new_texture
		if weapon_sprite:
			var texturePath = "res://assets/weapons/%s/%s.png" % [alignment,head]
			var new_texture = load(texturePath)
			weapon_sprite.texture = new_texture

func getColour(armour):
	var colours = {
		"Pink":"#f0f",
		"Red":"#f00",
		"Orange":"#f80",
		"Yellow":"#ff0",
		"Green":"#0f0",
		"Blue" : "#00f",
		"Purple":"#80f"
	}
	if armour in colours:
		return colours[armour]
	else:
		return "#fff"

func set_sprite_size(target_size: Vector2):
	var body_sprite = $bodySprite
	var head_sprite = $headSprite
	var weapon_sprite = $weaponSprite
	
	if body_sprite and body_sprite.texture:
		var body_original_size = body_sprite.texture.get_size()
		if body_original_size != Vector2.ZERO:
			body_sprite.scale = target_size / body_original_size  # Scale body to target size

	if head_sprite and head_sprite.texture:
		var head_original_size = head_sprite.texture.get_size()
		if head_original_size != Vector2.ZERO:
			head_sprite.scale = target_size / head_original_size  # Scale head proportionally

	if weapon_sprite and weapon_sprite.texture:
		var weapon_original_size = weapon_sprite.texture.get_size()
		if weapon_original_size != Vector2.ZERO:
			weapon_sprite.scale = target_size / weapon_original_size  # Scale head proportionally

func smallerDimension():
	if get_viewport().size.x > get_viewport().size.y:
		return get_viewport().size.y
	else: return get_viewport().size.x

func set_collision_size(target_size: Vector2):
	var collision = $CollisionShape2D  # Get the CollisionShape2D node
	
	if collision and collision.shape is RectangleShape2D:
		collision.shape.size = target_size  # Directly set the size for RectangleShape2D

	elif collision and collision.shape is CircleShape2D:
		collision.shape.radius = target_size.x / 2  # Use the X size for radius

# In the character's script
func _ready():
	var newSize = 5
	var new_collision_size = Vector2(smallerDimension()/newSize/2,smallerDimension()/newSize) # Example target size
	set_collision_size(new_collision_size)
	
	var new_size = Vector2(new_collision_size.x*2,new_collision_size.y)
	set_sprite_size(new_size)
	
	var player = get_node("/root/main/player")  # Change this to the correct path where your player is
	player.connect("player_interact", _on_player_interact)
	# Do something like showing the text box here
	$bodySprite.modulate = getColour(colour)  # Apply color dynamically
	set_child_texture(alignment,aspect)
	# Connect signals for the character's Area2D
	connect("body_entered", _on_body_entered)
	connect("body_exited", _on_body_exited)

	# Get references to the UI and TextBox
	ui = get_node("/root/main/UI")  # Make sure this is correct based on your scene structure
	text_box = ui.get_node("dialogueBox/textBox")
	ui.visible = false  # Initially hide the UI

func _on_player_interact():
	if player_nearby:
		show_character_info()

func _on_body_entered(body):
	if body.is_in_group("player"):  
		player_nearby = true

func _on_body_exited(body):
	if body.is_in_group("player"):
		player_nearby = false
		ui.visible = false

@warning_ignore("unused_parameter")
func _process(delta):
	pass
	if ui.visible and Input.is_action_just_pressed("ui_cancel"):  # Press Esc or a Cancel key
		ui.visible = false

func textFormatting(input,prefix='',suffix=''):
	return prefix + input + suffix

func getRole(input_string: String) -> String:
	var lookup_dict := {
		"I": "Captain",
		"V": "Hunter",
		"F": "Smith",
		"D": "Warden",
		"L": "Seer",
		"E": "Champion",
		"B": "Warlord"
	}
	if input_string.length() > 0:
		var first_letter := input_string.substr(0, 1).to_upper()
		return lookup_dict.get(first_letter, "Unknown") # Default to "Unknown" if the letter isn't in the dictionary
	return "Invalid Input"

func getTeam(input_string: String) -> String:
	var lookup_dict := {
		"S": "Deadly",
		"V": "Heavenly"
	}
	if input_string.length() > 0:
		var first_letter := input_string.substr(0, 1).to_upper()
		return lookup_dict.get(first_letter, "Unknown") # Default to "Unknown" if the letter isn't in the dictionary
	return "Invalid Input"

func formatAbugida(text: String) -> String:
	var characterList : Dictionary = {
		"a_":"á",
		"e_":"é",
		"o_":"ó",
		"u_":"ú",
		"d_":"ð",
		"n_":"ŋ",
		"s_":"ś",
		"t_":"þ",
		"z_":"ź"
	}
	for i in characterList:
		text = text.replace(i,characterList[i])
	return text
	
func show_character_info():
	ui.visible = true  # Show the dialogue box
	for i in abugida:
		abugida[i] = formatAbugida(abugida[i])
	var formatted_text = "%s %s" % [character_name, rank]
	if abugida["name"] != "":
		for i in abugida:
			formatted_text += "\n[code]/%s.[/code]" % [abugida[i]]
	if epithet != "":
		formatted_text += "\n\"%s\"" % [epithet]
	formatted_text += "\nThe %s of The Seven %s %ss\n" % [getRole(rank), getTeam(alignment), alignment]
	formatted_text += "\nThe %s %s of %s" % [animal, alignment, aspect]
	if edictDef != "":
		formatted_text += "\n%s" % [edictDef]
	formatted_text += "\nWeapon: %s" % [weapon]
	formatted_text += "\nPower: %s" % [power]
	formatted_text += "\nSpecies: %s" % [species]
	formatted_text += "\n%s" % [description]

	text_box.bbcode_text = textFormatting(formatted_text)
	text_box.queue_redraw()  # Force the RichTextLabel to update
