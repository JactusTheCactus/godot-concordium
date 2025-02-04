shader_type canvas_item;

uniform vec4 armor_color : hint_color;

void fragment() {
    COLOR = texture(TEXTURE, FRAGCOORD.xy / TEXTURE_PIXEL_SIZE) * armor_color;
}
