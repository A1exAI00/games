from os import path, getcwd

# Screen width and height
WIDTH, HEIGHT = 800, 700

# PyGame window background color
BG_COLOR = (255,255,255)

FPS = 60
WINDOW_NAME = 'Rock-Paper-Scissors Catch-Up'

# Miniman distance between player and window edge
FRAME_WIDTH = 5

# Mode of number of players ('random' - random number of players in teams)
SPAWN_MODE = 'notrandom'

# Number of players of different teams
R_NUM, P_NUM, S_NUM = 3, 3, 3

# Speed of players of different teams
R_SPEED, P_SPEED, S_SPEED = 1, 1, 1

# Width and height of players' textures
R_TEXTURE_WIDTH, P_TEXTURE_WIDTH, S_TEXTURE_WIDTH = 20, 20, 20
R_TEXTURE_HEIGHT, P_TEXTURE_HEIGHT, S_TEXTURE_HEIGHT = 20, 20, 20

# Coefficient in calculation of velocity vector
# ~1 - no preference -> players circle around each other infinitely
# >1 - player prefers to go to 'food' players
# <1 - player prefers to run from 'foe' players
SPEED_MULT = 0.5

# Path to players textures
TEXTURE_PATH = path.join(getcwd(), 'minecraft_textures', 'orig')

# Radius of players reach
DEATH_RADIUS = 5