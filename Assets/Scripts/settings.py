# Standard screen resolutions
SCREEN_SIZE = {
    'VGA-h'   : (640, 480),
    'VGA-v'   : (480, 640),
    'VGA-x2'  : (640, 640),

    'SVGA-h'  : (800, 600),
    'SVGA-v'  : (600, 800),
    'SVGA-x2' : (800, 800),

    'XGA'     : (1024, 768),
    'XVGA'    : (1280, 1024),

    'FULL'    : 'Fullscreen',
}

# Define caption
CAPTION = ('T h e   Q u e s t   -   ',
('M a i n', 'M e n u', 'L o a d', 'G a m e', 'R e c o r d'))

# Set framerate
FPS = 60

MUSIC_VOL = 0.5
SOUND_VOL = 0.5
LOGO = 500
STARS = 50

# Define game variables
SCENE = 0
LEVEL = 10
LIVES = 3
ENEMY_SCALE = 1
METEOR_SCALE = 3
SURGE_NUM = 1

player_dict = {
    'ammo'   : (200, 100, 50),
    'health' : (100, 200, 150),
    'speed'  : (2.5, 2.0, 3.0),
}

enemy_dict = {
    'scale' : (1, 1, 1),
    'ammo'  : (100, 0, 10),
    'load'  : (0, 1, 0),
    'exp'   : (20, 30, 10),
}

# Define colours (R, G, B)
def COLOR(color_key):
    color_dict = {
        'BLACK'  : (0, 0, 0),
        'DARK'   : (64, 64, 64),
        'GRAY'   : (128, 128, 128),
        'SILVER' : (192, 192, 192),
        'WHITE'  : (255, 255, 255),

        'BROWN'  : (255, 192, 192),
        'MAROON' : (128, 0, 0),
        'RED'    : (255, 0, 0),
        'ORANGE' : (255, 128, 0),
        'GREEN'  : (0, 128, 0),
        'LIME'   : (0, 255, 0),
        'OLIVE'  : (128, 128, 0),
        'YELLOW' : (255, 255, 0),
        'CYAN'   : (0, 255, 255),
        'SKY'    : (0, 128, 255),
        'TEAL'   : (0, 128, 128),
        'BLUE'   : (0, 0, 255),
        'NAVY'   : (0, 0, 128),
        'PINK'   : (255, 0, 255),
        'PURPLE' : (128, 0, 128),

        'ARCADE' : (8, 8, 8),
    }
    return color_dict[color_key.upper()]
