from mcpi.minecraft import Minecraft
from mcpi import block
from PIL import Image
import math
import time
import os

# Connect to Minecraft
mc = Minecraft.create(address="localhost", port=4711)

ORIGIN_X = 0
ORIGIN_Y = 64
ORIGIN_Z = 0

# Color map
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

def draw_frame(image_path, start_y, width_in_blocks):
    img = Image.open(image_path).convert("RGB")
    orig_width, orig_height = img.size
    scale_factor = width_in_blocks / orig_width
    new_height = int(orig_height * scale_factor)
    img = img.resize((width_in_blocks, new_height))

    for y in range(new_height):
        for x in range(width_in_blocks):
            pixel = img.getpixel((x, y))
            block_id, block_data = closest_block(pixel)
            mc.setBlock(ORIGIN_X + x, start_y + (new_height - y - 1), ORIGIN_Z, block_id, block_data)

def animate(folder_path, width_in_blocks, start_y=64, delay=0.2):
    frames = sorted(os.listdir(folder_path))
    while True:
        for frame in frames:
            if frame.lower().endswith(('.png', '.jpg', '.jpeg')):
                draw_frame(os.path.join(folder_path, frame), start_y, width_in_blocks)
                time.sleep(delay)

def build_static(image_path, width_in_blocks, start_y):
    draw_frame(image_path, start_y, width_in_blocks)

if __name__ == "__main__":
    mode = input("Do you want a static image or an animation? (s/a): ").lower()
    start_y = int(input("Enter the starting height (Y coordinate, e.g., 64): "))
    width_in_blocks = int(input("Enter the desired width in blocks: "))

    if mode == 's':
        image_path = input("Enter the path to the image file: ")
        build_static(image_path, width_in_blocks, start_y)
        mc.postToChat("Your Pixel Art Is Now Complete!")
        print("Your Pixel Art Is Now Complete!")
    elif mode == 'a':
        folder_path = input("Enter the folder path containing animation frames: ")
        delay = float(input("Enter delay between frames in seconds (e.g., 0.2): "))
        animate(folder_path, width_in_blocks, start_y, delay)
    else:
        print("Invalid option! Please choose 's' for static or 'a' for animation.")
