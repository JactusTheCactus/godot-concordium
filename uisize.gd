extends Control

# Set the size of the parent Control node
func _ready():
	size = get_viewport().size # Set the minimum size of the parent control to the viewport size
