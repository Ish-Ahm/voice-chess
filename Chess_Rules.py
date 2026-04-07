from Chess_Pieces_Temp import PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN, WHITE, BLACK


def get_valid_moves(piece_type, colour, row, col, board):
    """Return a list of valid (row, col) positions for a given piece."""

    if piece_type == PAWN:
        return _pawn_moves(colour, row, col, board)
    elif piece_type == ROOK:
        return _sliding_moves(row, col, board, colour, directions=[(0, 1), (0, -1), (1, 0), (-1, 0)])
    elif piece_type == BISHOP:
        return _sliding_moves(row, col, board, colour, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])
    elif piece_type == QUEEN:
        return _sliding_moves(row, col, board, colour, directions=[(0, 1), (0, -1), (1, 0), (-1, 0),
                                                                    (1, 1), (1, -1), (-1, 1), (-1, -1)])
    elif piece_type == KING:
        return _king_moves(row, col, board, colour)
    elif piece_type == KNIGHT:
        return _knight_moves(row, col, board, colour)
    return []


def _in_bounds(row, col):
    """Check if a position is within the 8x8 board."""
    return 0 <= row <= 7 and 0 <= col <= 7


def _is_enemy(board, row, col, colour):
    """Check if a square has an enemy piece."""
    cell = board[row][col]
    return cell is not None and cell["colour"] != colour


def _is_empty(board, row, col):
    """Check if a square is empty."""
    return board[row][col] is None


def _sliding_moves(row, col, board, colour, directions):
    """Generate moves for sliding pieces (rook, bishop, queen)."""
    moves = []
    for drow, dcol in directions:
        r, c = row + drow, col + dcol
        while _in_bounds(r, c):
            if _is_empty(board, r, c):
                # Empty square, can move here and keep sliding
                moves.append((r, c))
            elif _is_enemy(board, r, c, colour):
                # Enemy piece, can capture but stop sliding
                moves.append((r, c))
                break
            else:
                # Friendly piece, stop sliding
                break
            r += drow
            c += dcol
    return moves


def _king_moves(row, col, board, colour):
    """Generate all valid king moves (1 step in any direction)."""
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for drow, dcol in directions:
        r, c = row + drow, col + dcol
        if _in_bounds(r, c):
            if _is_empty(board, r, c) or _is_enemy(board, r, c, colour):
                moves.append((r, c))
    return moves


def _knight_moves(row, col, board, colour):
    """Generate all valid knight moves (L-shapes)."""
    moves = []
    jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2),  (1, 2),  (2, -1),  (2, 1)]
    for drow, dcol in jumps:
        r, c = row + drow, col + dcol
        if _in_bounds(r, c):
            if _is_empty(board, r, c) or _is_enemy(board, r, c, colour):
                moves.append((r, c))
    return moves


def _pawn_moves(colour, row, col, board):
    """Generate all valid pawn moves including captures and double step."""
    moves = []

    # White moves up (row decreases), black moves down (row increases)
    direction = -1 if colour == WHITE else 1
    start_row = 6 if colour == WHITE else 1

    # One step forward
    r = row + direction
    if _in_bounds(r, col) and _is_empty(board, r, col):
        moves.append((r, col))

        # Two steps forward from starting row
        if row == start_row:
            r2 = row + 2 * direction
            if _in_bounds(r2, col) and _is_empty(board, r2, col):
                moves.append((r2, col))

    # Diagonal captures
    for dcol in [-1, 1]:
        r, c = row + direction, col + dcol
        if _in_bounds(r, c) and _is_enemy(board, r, c, colour):
            moves.append((r, c))

    return moves