import pygame
import sys
import os


# --- Configuration ---
BOARD_SQUARES             = 8
SQUARE_SIZE               = 140            # Size of each square in pixels
BORDER                    = 60            # Width of the label border around the board
CURSOR_THICKNESS          = 8             # Thickness of the red cursor outline
DOT_RADIUS                = 14            # Radius of the valid move dot
PIECE_SIZE                = SQUARE_SIZE   # Size of piece images (slightly smaller than square for padding)
GAMEMODE_OPTION_BOXSIZE_W = 500           # Width of the box around gamemode options (should be larger than option text width)

# Font sizes
LABEL_FONT_SIZE           = 40
WINNER_FONT_SIZE          = 50
GAMEMODE_TITLE_FONT_SIZE  = 120
GAMEMODE_OPTION_FONT_SIZE = 80

# Right side panel
RIGHT_PANEL_WIDTH   = 400   # Width of right side panel
V_PADDING           = 10    # Vertical padding (top/bottom)
H_PADDING           = 60    # Horizontal padding (left/right)
OUTLINE_THICKNESS   = 5     # Thickness of the outline around the winner text box

BOARD_PX       = BOARD_SQUARES * SQUARE_SIZE    # Total pixel size of the board (without border)
WINDOW_W       = BOARD_PX + BORDER * 2          # Total window width (board + left and right borders)
WINDOW_H       = BOARD_PX + BORDER * 2          # Total window height (board + top and bottom borders)
WHOLE_WINDOW_W = WINDOW_W + RIGHT_PANEL_WIDTH   # Total window width including right panel


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
 
    label_font           = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", LABEL_FONT_SIZE)
    winner_font          = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", WINNER_FONT_SIZE)
    gamemode_title_font  = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", GAMEMODE_TITLE_FONT_SIZE)
    gamemode_option_font = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", GAMEMODE_OPTION_FONT_SIZE)
    
    return label_font, winner_font, gamemode_title_font, gamemode_option_font
