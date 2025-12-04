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
    # Wool
    (255, 255, 255): block.WHITE_WOOL.id,
    (255, 165, 0): block.ORANGE_WOOL.id,
    (255, 0, 0): block.RED_WOOL.id,
    (255, 255, 0): block.YELLOW_WOOL.id,
    (0, 128, 0): block.GREEN_WOOL.id,
    (0, 255, 255): block.LIGHT_BLUE_WOOL.id,
    (0, 0, 255): block.BLUE_WOOL.id,
    (128, 0, 128): block.PURPLE_WOOL.id,
    (128, 128, 128): block.GRAY_WOOL.id,
    (192, 192, 192): block.LIGHT_GRAY_WOOL.id,
    (255, 192, 203): block.PINK_WOOL.id,
    (165, 42, 42): block.BROWN_WOOL.id,
    (0, 0, 0): block.BLACK_WOOL.id,
    # Concrete
    (0, 255, 0): block.LIME_CONCRETE.id,
    (0, 128, 128): block.CYAN_CONCRETE.id,
    (128, 0, 0): block.RED_CONCRETE.id,
    (0, 0, 128): block.BLUE_CONCRETE.id,
    (255, 255, 224): block.YELLOW_CONCRETE.id,
    (255, 20, 147): block.PINK_CONCRETE.id,
    (128, 128, 128): block.GRAY_CONCRETE.id,
    (169, 169, 169): block.LIGHT_GRAY_CONCRETE.id,
    (0, 255, 255): block.LIGHT_BLUE_CONCRETE.id,
    # Terracotta
    (210, 180, 140): block.BRICK_BLOCK.id,  # substitute for tan terracotta
    (222, 184, 135): block.TERRACOTTA.id,   # regular terracotta
    (255, 228, 196): block.SANDSTONE.id,   # light terracotta substitute
    # Natural / Other Blocks
    (34, 139, 34): block.GRASS.id,
    (139, 69, 19): block.DIRT.id,
    (255, 248, 220): block.SAND.id,
    (128, 128, 0): block.GOLD_BLOCK.id,
    (192, 192, 192): block.STONE.id,
    (105, 105, 105): block.COBBLESTONE.id,
    (0, 100, 0): block.LEAVES.id,
    (47, 79, 79): block.OBSIDIAN.id,
    (160, 82, 45): block.WOOD.id,
    (218, 165, 32): block.GLOWSTONE.id,
    (255, 215, 0): block.GOLD_BLOCK.id,
    (173, 216, 230): block.ICE.id,
    (135, 206, 250): block.LIGHT_BLUE_WOOL.id,
    (244, 164, 96): block.SANDSTONE.id,
    (255, 99, 71): block.REDSTONE_BLOCK.id,
    (189, 183, 107): block.HAY_BLOCK.id,
    (255, 250, 205): block.GLOWSTONE.id,
    (46, 139, 87): block.EMERALD_BLOCK.id,
    (0, 191, 255): block.WATER.id,
    (255, 105, 180): block.PINK_CONCRETE.id,
    (210, 105, 30): block.BRICK_BLOCK.id,
    (128, 0, 128): block.PURPLE_WOOL.id,
    (255, 69, 0): block.ORANGE_CONCRETE.id,
}

def closest_block(rgb):
    r, g, b = rgb
    best_distance = math.inf
    best_block = block.STONE.id
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

# resize image to fit within Minecraft world constraints and build it block by block

    img = Image.open(image_path).convert("RGB")

    #keep aspect ratio
    orig_width, orig_height = img.size
    scale_factor = width_in_blocks / orig_width
    new_height = int(orig_height * scale_factor)

    img = img.resize((width_in_blocks, new_height))

    for y in range(new_height):
        for x in range(width_in_blocks):
            pixel = img.getpixel((x, y))
            block_id = closest_block(pixel)
            mc.setBlock(ORIGIN_X + x, ORIGIN_Y + (new_height - y - 1), ORIGIN_Z, block_id)

if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    width_in_blocks = int(input("Enter the desired width in blocks: "))
    build_image_in_minecraft(image_path, width_in_blocks)
    mc.postToChat("Your Pixel Atr Is Now Complete!")