# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# BRIGHT_RED = (255, 0, 0)
# BRIGHT_GREEN = (0, 255, 0)
# GREEN = (0, 128, 0)
# MAROON = (128, 0, 0)
# BRIGHT_BLUE = (0, 0, 255)
# BLUE = (0, 0, 128)
#
# ASSETS_DIR = "../assets/"
# BACKGROUND_IMG_PATH = ASSETS_DIR + "background.png"
# SPACESHIP_IMG_PATH = ASSETS_DIR + "spaceship.png"
# ASTEROID_IMG_PATH = [ASSETS_DIR + "asteroid0%d.png" % i for i in range(2)]
# BULLET_IMG_PATH = ASSETS_DIR + "bullet.png"
# EXPLOSION_IMG_PATHS = [ASSETS_DIR+"explosions/regularExplosion0%d.png" % i for i in range(9)]
#
# scale_of_player_image = [0.1, 0.1667]
# scale_of_asteroid_image = [0.1428, 0.1428]
# scale_of_bullet_image = [0.0125, 0.02]
# lam_of_generating_asteroid = 1000
# lam_of_generating_bullet = 400
# scale_of_asteroid_vel = 0.00588
# scale_of_bullet_vel = 0.00667
# angle_variance_of_asteroid = 0.01
# player_relative_position = [0.5, 0.9]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
GREEN = (0, 128, 0)
MAROON = (128, 0, 0)
BRIGHT_BLUE = (0, 0, 255)
BLUE = (0, 0, 128)

ASSETS_DIR = "../assets/"
BACKGROUND_IMG_PATH = ASSETS_DIR + "background.png"
SPACESHIP_IMG_PATH = ASSETS_DIR + "spaceship.png"
ASTEROID_IMG_PATH = [ASSETS_DIR + "asteroid0%d.png" % i for i in range(2)]
BULLET_IMG_PATH = ASSETS_DIR + "bullet.png"
EXPLOSION_IMG_PATHS = [ASSETS_DIR+"explosions/regularExplosion0%d.png" % i for i in range(9)]

list_of_difficulty = [0.00188, 0.00288, 0.00388, 0.00488, 0.00588, 0.00688, 0.00788, 0.00888, 0.00988, 0.01088]

scale_of_player_image = [0.1, 0.1667]
scale_of_asteroid_image = [0.1428, 0.1428]
scale_of_bullet_image = [0.0125, 0.02]
lam_of_generating_asteroid = 1000
lam_of_generating_bullet = 400

f = open("difficulty.txt", "r")
nums = []
if f.mode == 'r':
    nums = f.readlines()
    nums = [int(i) for i in nums]

if nums:
    scale_of_asteroid_vel = list_of_difficulty[nums[0]-1]
else:
    scale_of_asteroid_vel = 0.00588

scale_of_bullet_vel = 0.00667
angle_variance_of_asteroid = 0.01
player_relative_position = [0.5, 0.9]