from Chess_Config import *
from Chess_Rules import get_valid_moves


class Cursor:
    def __init__(self):
        self.column = 0
        self.row = 7
        self.holding = None       # the cell dict of the picked up piece
        self.holding_from = None  # (row, col) of where it was picked up from
        self.valid_moves = []     # list of (row, col) tuples for valid moves of held piece


    def move(self, move_col, move_row, board_size):
        """Move the cursor by (move_col, move_row), clamped within the board."""
        self.column = max(0, min(board_size - 1, self.column + move_col))
        self.row = max(0, min(board_size - 1, self.row + move_row))


    def pickup(self, board):
        """Pick up piece on current square if one exists."""
        cell = board[self.row][self.column]
        if cell is not None:
            self.holding      = cell
            self.holding_from = (self.row, self.column)

            # Calculate valid moves before removing piece from board
            self.valid_moves = get_valid_moves(
                cell["piece"],
                cell["colour"],
                self.row,
                self.column,
                board
            )

            board[self.row][self.column] = None  # Remove after calculating moves


    def cancel(self, board):
        """Put the piece back where it came from."""
        if self.holding is not None:
            row, column = self.holding_from
            board[row][column] = self.holding
            self.holding = None
            self.holding_from = None
            self.valid_moves  = []

        
    def drop(self, board):
        """Drop the held piece only if the destination is a valid move."""
        if self.holding is not None:
            destination = (self.row, self.column)
            if destination in self.valid_moves:
                # Valid move, place piece and capture any enemy on that square
                board[self.row][self.column] = self.holding
                self.holding      = None
                self.holding_from = None
                self.valid_moves  = []
                return True   # Drop was successful
            else:
                # Invalid square, cancel and return piece
                self.cancel(board)
                return False  # Drop was unsuccessful
        return False

    
    def draw_valid_moves(self, screen, border, square_size):
        """Draw grey dots on all valid move squares."""
        for (row, col) in self.valid_moves:
            # Center of the square
            cx = border + col * square_size + square_size // 2
            cy = border + row * square_size + square_size // 2
            pygame.draw.circle(screen, Colours.DOT_COLOUR, (cx, cy), DOT_RADIUS)


    def draw(self, screen, border, square_size):
        """Draw the red cursor outline over the current square."""
        x = border + self.column * square_size
        y = border + self.row * square_size
        cursor_colour = Colours.CURSOR_SELECTED if self.holding else Colours.CURSOR_NORMAL
        pygame.draw.rect(
            screen,
            cursor_colour,  # colour of cursor
            pygame.Rect(x, y, square_size, square_size),
            CURSOR_THICKNESS
        )