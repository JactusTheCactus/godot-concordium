extends CanvasLayer

@onready var info_panel = $infoPanel
@onready var character_info = $infoPanel/characterInfo

func _ready():
	info_panel.visible = false

func display_info(characterName, abugida_name):
	character_info.text = "[center][b]%s[/b]\n%s[/center]" % [characterName,abugida_name]
	info_panel.visible = true
