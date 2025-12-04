from minecraftstuff import Minecraft
from PIL import Image
import math

# connecting to the Minecraft server
mc = Minecraft.create(address="localhost", port=4711)

# set where the image will start in the Minecraft world
ORIGIN_X = 0
ORIGIN_Y = 64    
ORIGIN_Z = 0

# function to color match the image pixel to the closest Minecraft block color
COLOR_MAP = {
    (255, 255, 255): block.QUARTZ_BLOCK.id,
    (0, 0, 0): block.COAL_BLOCK.id,
    (128, 128, 128): block.STONE.id,
    (139, 69, 19): block.DIRT.id,
    (34, 139, 34): block.GRASS.id,
    (255, 0, 0):block.RED_WOOL.id,
    (0, 255, 0): block.LIME_WOOL.id,
    (0, 0, 255): block.BLUE_WOOL.id,
    (255, 255, 0): block.YELLOW_WOOL.id,
    (255, 165, 0): block.ORANGE_WOOL.id,
    (192, 192, 192): block.LIGHT_GRAY_WOOL.id,
    (128, 128, 128): block.GRAY_WOOL.id,
    (128, 0, 128): block.PURPLE_WOOL.id,
    (0, 255, 255): block.CYAN_WOOL.id,
    (255, 192, 203): block.PINK_WOOL.id,
    (0, 255, 255): block.LIGHT_BLUE_WOOL.id,
    (165, 42, 42): block.BROWN_WOOL.id,
    (255, 105, 180): block.MAGENTA_WOOL.id,
    (0, 128, 0): block.GREEN_WOOL.id,
    (255, 215, 0): block.GOLD_BLOCK.id
}

# resize image to fit within Minecraft world constraints and build it block by block
