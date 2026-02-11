import os


"""
Global configuration and constants for the Breakout game.
Includes screen settings, colors, brick rules, item settings, and asset paths.
"""

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650

BREAK_WIDTH = 50
BREAK_HEIGHT = 20
BRICK_RULES = {
    'weak': {
        'name': 'weak',
        'base_color': '#1565C0',
        'resistance': 1,
        'score': 1
    },
    'ordinary': {
        'name': 'ordinary',
        'base_color': '#FDD835',
        'damaged_color': '#FFF59D',
        'resistance': 2,
        'score': 2
    },
    'hard': {
        'name': 'hard',
        'base_color': '#C62828',
        'cracked_color': '#EF5350',
        'damaged_color': '#EF9A9A',
        'resistance': 3,
        'score': 2
    }
}

PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
PADDLE_SPEED = 8
PADDLE_COLOR = '#64DD17'

BALL_RADIUS = 15
BALL_SPEED = 5
BALL_ACCELERATION = 0.5
BALL_COLOR = '#FAFAFA'
SIMULATED_BALL_COLOR = '#616161'

ITEM_WIDTH = 12
ITEM_HEIGHT = 12
ITEM_SPEED = 4
ITEM_COLOR = '#FB8C00'
BIG_PADDLE_TIME = 12  # seconds

BASIC_ITEMS = ['triple', 'double', 'big_paddle']

# Text Colors
FONT_COLOR = '#B3E5FC'
WAITING_TEXT_COLOR = '#CFD8DC'
WIN_TEXT_COLOR = '#43A047'
GAME_OVER_TEXT_COLOR = '#B71C1C'


# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

hit_path = os.path.join(ASSETS_DIR, "brick-hit.wav")
break_path = os.path.join(ASSETS_DIR, "brick-breaking(1).wav")