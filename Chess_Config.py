import pygame
import sys
import os


# --- Configuration ---
BOARD_SQUARES     = 8
SQUARE_SIZE       = 150
PIECE_SIZE        = SQUARE_SIZE - 20
BORDER            = 50                # Width of the label border around the board
NORMAL_LABEL_SIZE = 40                # Size of labels (A-H, 1-8) on board border
WINNER_LABEL_SIZE = 150               # Size of winner label
CURSOR_THICKNESS  = 8                 # Thickness of the red cursor outline
DOT_RADIUS        = 14                # Radius of the valid move dot

BOARD_PX          = BOARD_SQUARES * SQUARE_SIZE
WINDOW_W          = BOARD_PX + BORDER * 2
WINDOW_H          = BOARD_PX + BORDER * 2


class Colours:
    WHITE           = (255, 255, 255)
    BLACK           = (0,   0,   0)
    BOARD_LIGHT     = (255, 218, 185)   # Peach
    BOARD_DARK      = (100, 149, 100)   # Green
    BOARD_BORDER    = (40,  40,  40)    # Dark border background
    LABEL           = (220, 220, 220)   # Label text colour
    CURSOR_NORMAL   = (238, 0,   0)     # Cursor red colour
    CURSOR_SELECTED = (255, 165, 0)     # Orange when holding piece
    DOT_COLOUR      = (180, 180, 180)   # Light grey for valid move dots
