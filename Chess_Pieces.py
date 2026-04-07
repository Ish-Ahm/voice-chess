from Chess_Config import *


# --- Piece type constants ---
PAWN   = "PAWN"
ROOK   = "ROOK"
KNIGHT = "KNIGHT"
BISHOP = "BISHOP"
KING   = "KING"
QUEEN  = "QUEEN"

# --- Colour constants ---
WHITE = "White"
BLACK = "Black"


# Maps piece type to its file number(s) in the image folder
# Each entry is a list because some pieces have multiple images (one per piece)
PIECE_FILE_NUMBERS = {
    PAWN:   [1, 2, 3, 4, 5, 6, 7, 8],
    ROOK:   [9, 10],
    KNIGHT: [11, 12],
    BISHOP: [13, 14],
    KING:   [15],
    QUEEN:  [16],
}

# Starting board layout for white (bottom, row 7 and 6)
# Each entry is (piece_type, file_index) where file_index picks from PIECE_FILE_NUMBERS list
# Row 7 = back rank, Row 6 = pawns
WHITE_BACK_RANK = [
    (ROOK,   0),   # col 0 - A1
    (KNIGHT, 0),   # col 1 - B1
    (BISHOP, 0),   # col 2 - C1
    (QUEEN,  0),   # col 3 - D1
    (KING,   0),   # col 4 - E1
    (BISHOP, 1),   # col 5 - F1
    (KNIGHT, 1),   # col 6 - G1
    (ROOK,   1),   # col 7 - H1
]

BLACK_BACK_RANK = [
    (ROOK,   0),   # col 0 - A8
    (KNIGHT, 0),   # col 1 - B8
    (BISHOP, 0),   # col 2 - C8
    (QUEEN,  0),   # col 3 - D8
    (KING,   0),   # col 4 - E8
    (BISHOP, 1),   # col 5 - F8
    (KNIGHT, 1),   # col 6 - G8
    (ROOK,   1),   # col 7 - H8
]


class ChessPieces:
    def __init__(self, square_size, piece_size):
        self.square_size = square_size
        self.piece_size = piece_size
        self.images = {WHITE: {}, BLACK: {}}  # images[colour][piece_type][index] = surface
        self._load_images()
        self.board = self._init_board()


    # -------------------------------------------------------------------------
    # Image loading
    # -------------------------------------------------------------------------

    def _load_images(self):
        """Load and scale all piece images for both colours."""
        for colour in [WHITE, BLACK]:
            folder = f"Chess Pieces_{colour}"
            for piece_type, numbers in PIECE_FILE_NUMBERS.items():
                self.images[colour][piece_type] = []
                for num in numbers:
                    filename = f"Chess Pieces_{colour}_{num:03d}.png"
                    path = os.path.join(folder, filename)
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.smoothscale(image, (self.piece_size, self.piece_size))
                    self.images[colour][piece_type].append(image)

    def _get_image(self, colour, piece_type, index=0, flipped=False):
        """Return the image surface for a piece, optionally rotated 180 degrees."""
        surf = self.images[colour][piece_type][index]
        if flipped:
            surf = pygame.transform.rotate(surf, 180)
        return surf


    # -------------------------------------------------------------------------
    # Board initialisation
    # -------------------------------------------------------------------------

    def _init_board(self):
        """
        Create an 8x8 board array.
        Each cell is either None or a dict:
            { "colour": WHITE/BLACK, "piece": PIECE_TYPE, "img_index": int, "flipped": bool }
        Row 7 = white back rank (bottom), Row 0 = black back rank (top).
        """
        board = [[None for _ in range(8)] for _ in range(8)]

        # White back rank - row 7 (bottom), not flipped
        for col, (piece_type, img_index) in enumerate(WHITE_BACK_RANK):
            board[7][col] = {
                "colour":    WHITE,
                "piece":     piece_type,
                "img_index": img_index,
                "flipped":   False
            }

        # White pawns - row 6, not flipped
        for col in range(8):
            board[6][col] = {
                "colour":    WHITE,
                "piece":     PAWN,
                "img_index": col,
                "flipped":   False
            }

        # Black pawns - row 1, flipped 180 for other player's view
        for col in range(8):
            board[1][col] = {
                "colour":    BLACK,
                "piece":     PAWN,
                "img_index": col,
                "flipped":   True
            }

        # Black back rank - row 0 (top), flipped 180 for other player's view
        for col, (piece_type, img_index) in enumerate(BLACK_BACK_RANK):
            board[0][col] = {
                "colour":    BLACK,
                "piece":     piece_type,
                "img_index": img_index,
                "flipped":   True
            }

        return board


    # -------------------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------------------

    def draw(self, screen, border):
        """Draw all pieces on the board."""
        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell is None:
                    continue

                image = self._get_image(
                    cell["colour"],
                    cell["piece"],
                    cell["img_index"],
                    cell["flipped"]
                )

                # get piece size dynamically
                piece_width = image.get_width()
                piece_height = image.get_height()

                # center inside square
                # calculate centered position inside square
                x = border + col * self.square_size + (self.square_size - self.piece_size) // 2
                y = border + row * self.square_size + (self.square_size - self.piece_size) // 2

                screen.blit(image, (x, y))