import pygame
import sys
import os


# --- Configuration ---

BOARD_SQUARES = 8  # 8x8 chess board


# ---- GLOBAL VARIABLES --------------------------------------------

pygame.init()
screen_info = pygame.display.Info()
scale       = min(screen_info.current_w / 2560, screen_info.current_h / 1600)

# Board
SQUARE_SIZE       = int(140  * scale)
PIECE_SIZE        = SQUARE_SIZE
BORDER            = int(50   * scale)
DOT_RADIUS        = int(14   * scale)
CURSOR_THICKNESS  = max(2, int(8   * scale))

# Right panel
RIGHT_PANEL_WIDTH         = int(400  * scale)
GAMEMODE_OPTION_BOXSIZE_W = int(500  * scale)
V_PADDING                 = max(1, int(10  * scale))
H_PADDING                 = int(60   * scale)
OUTLINE_THICKNESS         = max(1, int(5   * scale))

# Font sizes
LABEL_FONT_SIZE           = int(40   * scale)
WINNER_FONT_SIZE          = int(50   * scale)
GAMEMODE_TITLE_FONT_SIZE  = int(120  * scale)
GAMEMODE_OPTION_FONT_SIZE = int(80   * scale)

# Derived window dimensions (keep at bottom, depend on values above)
BOARD_PX       = BOARD_SQUARES * SQUARE_SIZE
WINDOW_W       = BOARD_PX + BORDER * 2
WINDOW_H       = BOARD_PX + BORDER * 2
WHOLE_WINDOW_W = WINDOW_W + RIGHT_PANEL_WIDTH


# Colours used in the game
class Colours:
    WHITE           = (255, 255, 255)
    BLACK           = (0,   0,   0)
    GREY            = (75,  75,  75)
    BOARD_LIGHT     = (255, 218, 185)   # Peach
    BOARD_DARK      = (100, 149, 100)   # Green
    BOARD_BORDER    = (40,  40,  40)    # Dark border background
    LABEL           = (220, 220, 220)   # Label text colour
    CURSOR_NORMAL   = (238, 0,   0)     # Cursor red colour
    CURSOR_SELECTED = (255, 165, 0)     # Orange when holding piece
    DOT_COLOUR      = (180, 180, 180)   # Light grey for valid move dots


# Fonts used in the game
def initialize_fonts():
    """Initialize all game fonts inside main loop"""
    
    chinese_rocks_path = "assets/fonts/chinese-rocks-rg.ttf"
    if not os.path.isfile(chinese_rocks_path):
        print(f"Error: Font file '{chinese_rocks_path}' not found.")
        sys.exit(1)

    label_font           = pygame.font.Font(chinese_rocks_path, LABEL_FONT_SIZE)
    winner_font          = pygame.font.Font(chinese_rocks_path, WINNER_FONT_SIZE)
    gamemode_title_font  = pygame.font.Font(chinese_rocks_path, GAMEMODE_TITLE_FONT_SIZE)
    gamemode_option_font = pygame.font.Font(chinese_rocks_path, GAMEMODE_OPTION_FONT_SIZE)

    return label_font, winner_font, gamemode_title_font, gamemode_option_font
