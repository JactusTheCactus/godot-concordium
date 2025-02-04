extends CharacterBody2D

@export var playerSpeed: float = 200.0
@export var character_name: String = "Player"

var player_nearby = false
var player : CharacterBody2D = null
var text_box : RichTextLabel = null
var promptBox : Control = null
var windowSize: Vector2
var playerPosition: Vector2

func set_sprite_size(target_size: Vector2):
	var sprite = $Sprite2D
	
	if sprite and sprite.texture:
		var original_size = sprite.texture.get_size()
		if original_size != Vector2.ZERO:
			sprite.scale = target_size / original_size  # Scale body to target size

func smallerDimension():
	if get_viewport().size.x > get_viewport().size.y:
		return get_viewport().size.y
	else: return get_viewport().size.x

# In the player's script
@warning_ignore("unused_signal")
signal player_interact

func _input(event):
	if event.is_action_pressed("interact"):  # Assuming "interact" is mapped to 'E' or another key
		emit_signal("player_interact")

@warning_ignore("unused_parameter")
func _physics_process(delta):
	windowSize = get_viewport().size
	playerSpeed = windowSize.y / 2
	var playerDirection = Vector2.ZERO
	if Input.is_action_pressed("moveRight"):
		playerDirection.x += 1
	if Input.is_action_pressed("moveLeft"):
		playerDirection.x -= 1
	if Input.is_action_pressed("moveDown"):
		playerDirection.y += 1
	if Input.is_action_pressed("moveUp"):
		playerDirection.y -= 1

	velocity = playerDirection.normalized() * playerSpeed
	move_and_slide()

func set_collision_size(target_size: Vector2):
	var collision = $CollisionShape2D  # Get the CollisionShape2D node
	
	if collision and collision.shape is RectangleShape2D:
		collision.shape.size = target_size  # Directly set the size for RectangleShape2D

	elif collision and collision.shape is CircleShape2D:
		collision.shape.radius = target_size.x / 2  # Use the X size for radius

# Temporarily force an interaction for testing
func _ready():
	var new_collision_size = Vector2(smallerDimension()/10,smallerDimension()/5) # Example target size
	set_collision_size(new_collision_size)
	
	var new_size = Vector2(new_collision_size.x*2,new_collision_size.y)
	set_sprite_size(new_size)
	
	playerPosition.x = get_viewport().size.x / 2
	playerPosition.y = get_viewport().size.y / 8
	set_position(playerPosition)
	add_to_group("player")  # Make sure the player is in the "player" group
	promptBox = get_node("Sprite2D/text")
	text_box = promptBox.get_node("dialogueBox/textBox")
	promptBox.visible = false

func _on_body_entered(body):
	print('_on_body_entered')
	if body.is_in_group("player"):
		player_nearby = true

func _on_body_exited(body):
	if body.is_in_group("player"):
		player_nearby = false
