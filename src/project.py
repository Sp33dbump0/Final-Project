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


# resize image to fit within Minecraft world constraints and build it block by block
