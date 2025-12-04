from mcpi.minecraft import Minecraft
from mcpi import block
from PIL import Image
import math
from minecraftstuff import MinecraftShape

# connecting to the Minecraft server
mc = Minecraft.create(address="localhost", port=4711)

# set where the image will start in the Minecraft world
ORIGIN_X = 0
ORIGIN_Y = 64    
ORIGIN_Z = 0

# function to color match the image pixel to the closest Minecraft block color
COLOR_MAP = {
    # Wool (all 16 colors)
    (255, 255, 255): (block.WOOL.id, 0),     # White
    (255, 165, 0): (block.WOOL.id, 1),       # Orange
    (255, 0, 255): (block.WOOL.id, 2),       # Magenta
    (173, 216, 230): (block.WOOL.id, 3),     # Light Blue
    (255, 255, 0): (block.WOOL.id, 4),       # Yellow
    (0, 255, 0): (block.WOOL.id, 5),         # Lime
    (255, 192, 203): (block.WOOL.id, 6),     # Pink
    (128, 128, 128): (block.WOOL.id, 7),     # Gray
    (211, 211, 211): (block.WOOL.id, 8),     # Light Gray
    (0, 255, 255): (block.WOOL.id, 9),       # Cyan
    (128, 0, 128): (block.WOOL.id, 10),      # Purple
    (0, 0, 255): (block.WOOL.id, 11),        # Blue
    (165, 42, 42): (block.WOOL.id, 12),      # Brown
    (0, 128, 0): (block.WOOL.id, 13),        # Green
    (255, 0, 0): (block.WOOL.id, 14),        # Red
    (0, 0, 0): (block.WOOL.id, 15),          # Black

    # Natural / Stone / Ore
    (125, 125, 125): (block.STONE.id, 0),        # Stone
    (139, 69, 19): (block.DIRT.id, 0),          # Dirt
    (34, 139, 34): (block.GRASS.id, 0),         # Grass
    (169, 169, 169): (block.COBBLESTONE.id, 0), # Cobblestone
    (210, 180, 140): (block.SANDSTONE.id, 0),   # Sandstone
    (255, 248, 220): (block.SAND.id, 0),        # Sand
    (0, 0, 255): (block.WOOL.id, 11),           # Blue wool as water
    (218, 165, 32): (block.GLOWSTONE_BLOCK.id, 0), # Glowstone
    (255, 215, 0): (block.GOLD_BLOCK.id, 0),        # Gold block
    (192, 192, 192): (block.IRON_BLOCK.id, 0),      # Iron block
    (47, 79, 79): (block.OBSIDIAN.id, 0),           # Obsidian
    (46, 139, 87): (block.WOOL.id, 5),             # Green wool as substitute for Emerald
    (210, 105, 30): (block.BRICK_BLOCK.id, 0),     # Brick
    (173, 216, 230): (block.ICE.id, 0),           # Ice
    (189, 183, 107): (block.HAY_BLOCK.id, 0),      # Hay
    (160, 82, 45): (block.WOOD.id, 0),            # Oak logs as wood
}



def closest_block(rgb):
    r, g, b = rgb
    best_distance = math.inf
    best_block = (block.STONE.id, 0) # default block
    for color, block_id in COLOR_MAP.items():
        dr = r - color[0]
        dg = g - color[1]
        db = b - color[2]
        distance = dr*dr + dg*dg + db*db
        if distance < best_distance:
            best_distance = distance
            best_block = block_id
    return best_block

def build_image_in_minecraft(image_path, width_in_blocks):
    img = Image.open(image_path).convert("RGB")
    orig_width, orig_height = img.size
    scale_factor = width_in_blocks / orig_width
    new_height = int(orig_height * scale_factor)
    img = img.resize((width_in_blocks, new_height))

    for y in range(new_height):
        for x in range(width_in_blocks):
            pixel = img.getpixel((x, y))
            block_id, block_data = closest_block(pixel)
            mc.setBlock(ORIGIN_X + x, ORIGIN_Y + (new_height - y - 1), ORIGIN_Z, block_id, block_data)


if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    width_in_blocks = int(input("Enter the desired width in blocks: "))
    build_image_in_minecraft(image_path, width_in_blocks)
    mc.postToChat("Your Pixel Atr Is Now Complete!")