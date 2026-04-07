# --- Imports ---
from Chess_Config import *
from Chess_Cursor import Cursor
from Chess_Pieces_Temp import ChessPieces, KING, WHITE, BLACK


def draw_board(screen):
    """Draw the 8x8 chess board inside the border offset."""
    for row in range(BOARD_SQUARES):
        for col in range(BOARD_SQUARES):
            color = Colours.BOARD_LIGHT if (row + col) % 2 == 0 else Colours.BOARD_DARK
            x = BORDER + col * SQUARE_SIZE
            y = BORDER + row * SQUARE_SIZE
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))


def draw_border_labels(screen, font):
    """Draw rank numbers and file letters centered in the border strips."""
    letters = "ABCDEFGH"

    for i in range(BOARD_SQUARES):
        center_offset = i * SQUARE_SIZE + SQUARE_SIZE // 2

        # --- File letters (A-H) on top and bottom border ---
        letters_surf = font.render(letters[i], True, Colours.LABEL)
        lx = BORDER + center_offset - letters_surf.get_width() // 2

        # Bottom border (normal)
        fy_bot = BOARD_PX + BORDER + BORDER // 2 - letters_surf.get_height() // 2
        screen.blit(letters_surf, (lx, fy_bot))

        # Top border (180 rotation, reversed order)
        letters_surf_top = font.render(letters[BOARD_SQUARES - 1 - i], True, Colours.LABEL)
        letters_surf_top = pygame.transform.rotate(letters_surf_top, 180)
        fx_top = BORDER + center_offset - letters_surf_top.get_width() // 2
        fy_top = BORDER // 2 - letters_surf_top.get_height() // 2
        screen.blit(letters_surf_top, (fx_top, fy_top))

        # --- Rank numbers (8-1) on left and right border ---
        numbers_surf = font.render(str(BOARD_SQUARES - i), True, Colours.LABEL)
        ny = BORDER + center_offset - numbers_surf.get_height() // 2

        # Left border (normal)
        nx_left = BORDER // 2 - numbers_surf.get_width() // 2
        screen.blit(numbers_surf, (nx_left, ny))

        # Right border (180 rotation, reversed order)
        numbers_surf_right = font.render(str(i + 1), True, Colours.LABEL)
        numbers_surf_right = pygame.transform.rotate(numbers_surf_right, 180)
        ny_right = BORDER + center_offset - numbers_surf_right.get_height() // 2
        nx_right = BOARD_PX + BORDER + BORDER // 2 - numbers_surf_right.get_width() // 2
        screen.blit(numbers_surf_right, (nx_right, ny_right))


def check_winner(board):
    """Return WHITE or BLACK if the opposing king has been captured, else None."""
    kings_alive = {WHITE: False, BLACK: False}
    for row in range(8):
        for col in range(8):
            cell = board[row][col]
            if cell is not None and cell["piece"] == KING:
                kings_alive[cell["colour"]] = True

    if not kings_alive[BLACK]:
        return WHITE
    if not kings_alive[WHITE]:
        return BLACK
    return None


def winner_screen(screen, font, winner):
    """Display the winner on the screen."""
    text = f"{winner} wins!"
    surf = font.render(text, True, Colours.LABEL)
    x = (WINDOW_W - surf.get_width()) // 2
    y = (WINDOW_H - surf.get_height()) // 2
    
    # Draw black box with white outline behind text
    v_padding = 20  # vertical padding (top/bottom)
    h_padding = 60  # horizontal padding (left/right)
    outline_thickness = 15

    box_rect = pygame.Rect(
        x - h_padding,
        y - v_padding,
        surf.get_width()  + h_padding * 2,
        surf.get_height() + v_padding * 2
    )
    pygame.draw.rect(screen, Colours.BLACK, box_rect)  # Black box
    pygame.draw.rect(screen, Colours.CURSOR_NORMAL, box_rect, outline_thickness)  # White outline
    
    screen.blit(surf, (x, y))
    pygame.display.flip()
    pygame.time.wait(5000)  # Wait 5 seconds before closing


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H + 80))
    pygame.display.set_caption("Chess Board")

    label_font  = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", NORMAL_LABEL_SIZE)
    winner_font = pygame.font.Font("assets/fonts/chinese-rocks-rg.ttf", WINNER_LABEL_SIZE)
    clock = pygame.time.Clock()

    pieces = ChessPieces(SQUARE_SIZE, PIECE_SIZE)  # Class object for each piece
    cursor = Cursor()  # Main cursor used by player

    current_turn = WHITE  # Game starts with white
    winner       = None

    test = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Test button for winner test
                if event.key == pygame.K_p:
                    print("test", flush=True)
                    test = True

                # Movement keys (arrow keys and WASD)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:   # Left arrow  / A key
                    cursor.move(-1, 0, BOARD_SQUARES)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Right arrow / D key
                    cursor.move(1, 0, BOARD_SQUARES)
                if event.key == pygame.K_UP or event.key == pygame.K_w:     # Up arrow    / W key
                    cursor.move(0, -1, BOARD_SQUARES)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:   # Down arrow  / S key
                    cursor.move(0, 1, BOARD_SQUARES)
                
                # Pick up or Drop
                if event.key == pygame.K_SPACE:
                    if cursor.holding is None:
                        cell = pieces.board[cursor.row][cursor.column]
                        if cell is not None and cell["colour"] == current_turn:
                            cursor.pickup(pieces.board)
                    else:
                        drop_successful = cursor.drop(pieces.board)
                        if drop_successful:   # Only switch turn if drop was actually successful
                            current_turn = BLACK if current_turn == WHITE else WHITE
                            winner = check_winner(pieces.board)

                # Cancel
                if event.key == pygame.K_RETURN:
                    if cursor.holding is not None:
                        cursor.cancel(pieces.board)   # Put piece back to original square
                


        # Fill entire window with border color first
        screen.fill(Colours.BOARD_BORDER)

        # draw everything once
        draw_board(screen)
        draw_border_labels(screen, label_font)
        cursor.draw_valid_moves(screen, BORDER, SQUARE_SIZE)  # Grey dots under pieces
        pieces.draw(screen, BORDER, cursor.holding, cursor.holding_from)

        # Draw cursor
        cursor.draw(screen, BORDER, SQUARE_SIZE)

        # Draw current turn label
        turn_text = f"{current_turn}'s Turn"
        turn_surf = label_font.render(turn_text, True, Colours.LABEL)
        screen.blit(turn_surf, (BORDER, WINDOW_H + 20))

        pygame.display.flip()
        clock.tick(60)

        if winner is not None or test:
            winner_screen(screen, winner_font, winner)
            pygame.quit()
            sys.exit()



if __name__ == "__main__":
    main()