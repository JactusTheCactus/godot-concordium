numDict = {
    "consonants":25,
    "vowels":9,
    "symbols":4
}
iconSize = 16
grid = {
    "width":0,
    "height":0
}
spacing = 2
# grid["width"] = numDict["consonants"] * (iconSize + spacing) + spacing
# for item in numDict:
#     grid["height"] += iconSize + spacing
# grid["height"] += spacing
# gridSize = f"""
# {grid['width']}px X {grid['height']}px
# """
# print(gridSize)

coord = 0
for i in range(numDict["symbols"]):
    print(coord)
    coord += iconSize + spacing