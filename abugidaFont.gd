extends RichTextLabel

var use_sprite_font = false
var font_texture : Texture2D
var character_map : Dictionary
var parent_node : Node
var textBox : Node

func _ready():
	parent_node = get_node("/root/main/character")
	textBox = get_node("/root/main/UI/dialogueBox/textBox")
	var panelOpacity = 0.5
	modulate.a = panelOpacity  # Set Panel to 50% opacity
	textBox.self_modulate.a = 1 / panelOpacity  # Set RichTextLabel to full opacity
	# Load the sprite sheet and character map
	font_texture = load("res://assets/fonts/Abugida/sprites/spriteSheet.png")
	load_character_map()

func load_character_map():
	var file = FileAccess.open("res://assets/fonts/Abugida/sprites/metadata.json", FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		var json = JSON.new()
		var error = json.parse(json_string)
		if error == OK:
			character_map = json.get_data().get("characters", {})

func _on_text_updated(new_text: String):
	if use_sprite_font:
		queue_redraw()
	else:
		text = new_text  # Changed from bbcode_text

func _draw():
	if use_sprite_font and parent_node:
		var display_text = parent_node.text
		var x_offset = 0
		var y_offset = 0
		
		for i in range(display_text.length()):
			var character = display_text[i]
			
			if character_map.has(character):
				var character_data = character_map[character]
				var rect = Rect2(character_data["x"], character_data["y"], character_data["width"], character_data["height"])
				
				# Adjust diacritic placement
				if character_data.get("overlay", false) and i > 0:
					var prev_char = display_text[i - 1]
					if character_map.has(prev_char):
						y_offset -= character_data["height"] / 2  # Move diacritic above previous letter
				
				# Draw character sprite
				draw_texture_rect_region(font_texture, Rect2(x_offset, y_offset, character_data["width"], character_data["height"]), rect)

				# Reset diacritic offset
				y_offset = 0  

				# Move x_offset for the next character
				x_offset += character_data["width"] + 2

func switch_font():
	use_sprite_font = !use_sprite_font
	if use_sprite_font:
		queue_redraw()  # Force custom drawing
	else:
		_on_text_updated(self.text)  # Restore standard font rendering
