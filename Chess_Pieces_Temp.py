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


class ChessPieces:
    def __init__(self, square_size, piece_size):
        self.square_size = square_size
        self.piece_size = piece_size
        self.images = {WHITE: {}, BLACK: {}}
        self._load_images()
        self.board = self._init_board()


    # -------------------------------------------------------------------------
    # Image loading
    # -------------------------------------------------------------------------

    def _load_images(self):
        """Load and scale all piece images using explicit filenames."""

        FILE_MAP = {
            WHITE: {
                PAWN:   ["images/white-pawn.png"],
                ROOK:   ["images/white-rook.png"],
                KNIGHT: ["images/white-knight.png"],
                BISHOP: ["images/white-bishop.png"],
                KING:   ["images/white-king.png"],
                QUEEN:  ["images/white-queen.png"],
            },
            BLACK: {
                PAWN:   ["images/black-pawn.png"],
                ROOK:   ["images/black-rook.png"],
                KNIGHT: ["images/black-knight.png"],
                BISHOP: ["images/black-bishop.png"],
                KING:   ["images/black-king.png"],
                QUEEN:  ["images/black-queen.png"],
            }
        }

        for colour in [WHITE, BLACK]:
            for piece_type, filenames in FILE_MAP[colour].items():
                self.images[colour][piece_type] = []

                for filename in filenames:
                    path = os.path.join("assets", filename)  # make sure folder matches
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.smoothscale(
                        image,
                        (self.piece_size, self.piece_size)
                    )
                    self.images[colour][piece_type].append(image)


    def _get_image(self, colour, piece_type, index=0, flipped=False):
        """Return the image surface for a piece, optionally rotated."""

        surf = self.images[colour][piece_type][index]
        if flipped:
            surf = pygame.transform.rotate(surf, 180)
        return surf


    # -------------------------------------------------------------------------
    # Board initialisation
    # -------------------------------------------------------------------------

    def _init_board(self):
        """Create and return the starting chess board."""

        board = [[None for _ in range(8)] for _ in range(8)]

        # white back rank (row 7)
        back_rank = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        for col, piece in enumerate(back_rank):
            board[7][col] = {
                "colour": WHITE,
                "piece": piece,
                "img_index": 0,
                "flipped": False
            }

        # white pawns (row 6)
        for col in range(8):
            board[6][col] = {
                "colour": WHITE,
                "piece": PAWN,
                "img_index": 0,
                "flipped": False
            }

        # black pawns (row 1)
        for col in range(8):
            board[1][col] = {
                "colour": BLACK,
                "piece": PAWN,
                "img_index": 0,
                "flipped": True
            }

        # black back rank (row 0)
        for col, piece in enumerate(back_rank):
            board[0][col] = {
                "colour": BLACK,
                "piece": piece,
                "img_index": 0,
                "flipped": True
            }

        return board


    # -------------------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------------------

    def draw(self, screen, border, held_piece=None, held_from=None):
        """Draw all pieces on the board, including the held piece in its original square."""
        
        for row in range(8):
            for column in range(8):
                cell = self.board[row][column]

                # If this square is where the held piece came from, draw it there still
                if cell is None and held_piece is not None and held_from == (row, column):
                    cell = held_piece

                if cell is None:
                    continue

                image = self._get_image(
                    cell["colour"],
                    cell["piece"],
                    cell["img_index"],
                    cell["flipped"]
                )

                x = border + column * self.square_size + (self.square_size - self.piece_size) // 2
                y = border + row    * self.square_size + (self.square_size - self.piece_size) // 2

                screen.blit(image, (x, y))