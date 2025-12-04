from mcpi.minecraft import Minecraft
from mcpi import block
from PIL import Image
import math

# Connect to Minecraft
mc = Minecraft.create(address="localhost", port=4711)

# Set starting coordinates
ORIGIN_X = 0
ORIGIN_Z = 0

# Minecraft build limits
MAX_HEIGHT = 255

COLOR_MAP = {
    # Wool
    (255, 255, 255): (block.WOOL.id, 0),   # White
    (255, 165, 0): (block.WOOL.id, 1),     # Orange
    (255, 0, 255): (block.WOOL.id, 2),     # Magenta
    (173, 216, 230): (block.WOOL.id, 3),   # Light Blue
    (255, 255, 0): (block.WOOL.id, 4),     # Yellow
    (0, 255, 0): (block.WOOL.id, 5),       # Lime
    (255, 192, 203): (block.WOOL.id, 6),   # Pink
    (128, 128, 128): (block.WOOL.id, 7),   # Gray
    (211, 211, 211): (block.WOOL.id, 8),   # Light Gray
    (0, 255, 255): (block.WOOL.id, 9),     # Cyan
    (128, 0, 128): (block.WOOL.id, 10),    # Purple
    (0, 0, 255): (block.WOOL.id, 11),      # Blue
    (165, 42, 42): (block.WOOL.id, 12),    # Brown
    (0, 128, 0): (block.WOOL.id, 13),      # Green
    (255, 0, 0): (block.WOOL.id, 14),      # Red
    (0, 0, 0): (block.WOOL.id, 15),        # Black


    # Natural / Stone / Ore
    (125, 125, 125): (block.STONE.id, 0),
    (139, 69, 19): (block.DIRT.id, 0),
    (34, 139, 34): (block.GRASS.id, 0),
    (169, 169, 169): (block.COBBLESTONE.id, 0),
    (210, 180, 140): (block.SANDSTONE.id, 0),
    (105, 105, 105): (block.STONE.id, 0),
    (255, 248, 220): (block.SAND.id, 0),
    (0, 0, 255): (block.WOOL.id, 11),       # Blue wool as water substitute
    (218, 165, 32): (block.GLOWSTONE_BLOCK.id, 0),
    (255, 215, 0): (block.GOLD_BLOCK.id, 0),
    (192, 192, 192): (block.IRON_BLOCK.id, 0),
    (47, 79, 79): (block.OBSIDIAN.id, 0),
    (46, 139, 87): (block.EMERALD_ORE.id, 0), # Use EMERALD_ORE instead of EMERALD_BLOCK
    (210, 105, 30): (block.BRICK_BLOCK.id, 0),
    (173, 216, 230): (block.ICE.id, 0),
    (160, 82, 45): (block.WOOD.id, 0),
}

def closest_block(rgb):
    r, g, b = rgb
    best_distance = math.inf
    best_block = (block.STONE.id, 0)
    for color, block_id in COLOR_MAP.items():
        dr, dg, db = r - color[0], g - color[1], b - color[2]
        distance = dr*dr + dg*dg + db*db
        if distance < best_distance:
            best_distance = distance
            best_block = block_id
    return best_block

def build_image_in_minecraft(image_path, start_y=64, max_width=None, max_height=None):
    img = Image.open(image_path).convert("RGB")
    orig_width, orig_height = img.size

    # Auto-scaling
    scale_x = scale_y = 1.0
    if max_width:
        scale_x = max_width / orig_width
    if max_height:
        scale_y = max_height / orig_height

    # Choose the smaller scale to fit both width and height limits
    scale_factor = min(scale_x, scale_y)
    new_width = int(orig_width * scale_factor)
    new_height = int(orig_height * scale_factor)
    img = img.resize((new_width, new_height))

    # Build the image in Minecraft
    for y in range(new_height):
        for x in range(new_width):
            pixel = img.getpixel((x, y))
            block_id, block_data = closest_block(pixel)
            mc.setBlock(ORIGIN_X + x, start_y + (new_height - y - 1), ORIGIN_Z, block_id, block_data)

if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    start_y = int(input("Enter starting height (Y coordinate, e.g., 64): "))
    max_width = int(input("Enter max width in blocks (or 0 for auto): "))
    max_height = int(input("Enter max height in blocks (or 0 for auto): "))
    max_width = None if max_width == 0 else max_width
    max_height = None if max_height == 0 else max_height

    build_image_in_minecraft(image_path, start_y, max_width, max_height)
    mc.postToChat("Your Pixel Art Is Now Complete!")
    print("Your Pixel Art Is Now Complete!")
