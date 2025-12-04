from mcpi.minecraft import Minecraft
from mcpi import block
from PIL import Image
import math, os, time

mc = Minecraft.create(address="localhost", port=4711)

ORIGIN_X = 0
ORIGIN_Z = 0

COLOR_MAP = {
    (255, 255, 255): (block.WOOL.id, 0),  
    (255, 165, 0): (block.WOOL.id, 1),    
    (255, 0, 255): (block.WOOL.id, 2),
    (173, 216, 230): (block.WOOL.id, 3),
    (255, 255, 0): (block.WOOL.id, 4),
    (0, 255, 0): (block.WOOL.id, 5),
    (255, 192, 203): (block.WOOL.id, 6),
    (128, 128, 128): (block.WOOL.id, 7),
    (211, 211, 211): (block.WOOL.id, 8),
    (0, 255, 255): (block.WOOL.id, 9),
    (128, 0, 128): (block.WOOL.id, 10),
    (0, 0, 255): (block.WOOL.id, 11),
    (165, 42, 42): (block.WOOL.id, 12),
    (0, 128, 0): (block.WOOL.id, 13),
    (255, 0, 0): (block.WOOL.id, 14),
    (0, 0, 0): (block.WOOL.id, 15),

    (125, 125, 125): (block.STONE.id, 0),
    (139, 69, 19): (block.DIRT.id, 0),
    (34, 139, 34): (block.GRASS.id, 0),
    (169, 169, 169): (block.COBBLESTONE.id, 0),
    (210, 180, 140): (block.SANDSTONE.id, 0),
    (255, 248, 220): (block.SAND.id, 0),
    (218, 165, 32): (block.GLOWSTONE_BLOCK.id, 0),
    (255, 215, 0): (block.GOLD_BLOCK.id, 0),
    (192, 192, 192): (block.IRON_BLOCK.id, 0),
    (47, 79, 79): (block.OBSIDIAN.id, 0),
    (46, 139, 87): (block.EMERALD_ORE.id, 0),
    (210, 105, 30): (block.BRICK_BLOCK.id, 0),
    (173, 216, 230): (block.ICE.id, 0),
    (160, 82, 45): (block.WOOD.id, 0)
}

def closest_block(rgb):
    r, g, b = rgb
    best_distance = math.inf
    best_block = (block.STONE.id, 0)

    for color, block_info in COLOR_MAP.items():
        dr = r - color[0]
        dg = g - color[1]
        db = b - color[2]
        dist = dr*dr + dg*dg + db*db
        if dist < best_distance:
            best_distance = dist
            best_block = block_info

    return best_block

def resize_image(img, width):
    scale = width / img.width
    height = max(1, int(img.height * scale))
    return img.resize((width, height)), height

def draw_frame(img, width, start_y, previous_frame=None):
    """ Optimized: Only place blocks if the pixel changed """

    img, height = resize_image(img, width)
    img_data = img.convert("RGB")

    for y in range(height):
        for x in range(width):
            rgb = img_data.getpixel((x, y))
            block_id, block_data = closest_block(rgb)

            # Skip if pixel is identical to previous frame
            if previous_frame and previous_frame[y][x] == (block_id, block_data):
                continue

            mc.setBlock(ORIGIN_X + x, start_y + (height - y - 1), ORIGIN_Z,
                        block_id, block_data)

    return [[closest_block(img_data.getpixel((x, y)))
             for x in range(width)] for y in range(height)]

def play_animation(folder_path, width, start_y, delay):
    frames = sorted(os.listdir(folder_path))
    previous = None

    for file in frames:
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img = Image.open(os.path.join(folder_path, file))
        previous = draw_frame(img, width, start_y, previous_frame=previous)
        time.sleep(delay)

    mc.postToChat("Animation Finished!")

def build_single_image(image_path, width, start_y):
    img = Image.open(image_path)
    draw_frame(img, width, start_y)
    mc.postToChat("Pixel Art Complete!")

if __name__ == "__main__":
    mode = input("Mode (image / animation): ").strip().lower()
    width = int(input("Width in blocks: "))
    start_y = int(input("Starting Y height: "))

    if mode == "image":
        path = input("Image path: ")
        build_single_image(path, width, start_y)

    elif mode == "animation":
        folder = input("Folder path containing frames: ")
        delay = float(input("Frame delay (seconds, e.g., 0.05): "))
        play_animation(folder, width, start_y, delay)

    print("Done.")
