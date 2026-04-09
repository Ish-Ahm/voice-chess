# ---- IMPORTS -----------------------------------------------------

from Chess_Config import *
from Chess_Cursor import Cursor
from Chess_Pieces_Temp import ChessPieces, KING, WHITE, BLACK
from Chess_Network import Network


# ---- CHESS BOARD -------------------------------------------------

def draw_board(screen):
    """Draw the 8x8 chess board inside the border offset."""
    
    for row in range(BOARD_SQUARES):
        for column in range(BOARD_SQUARES):
            color = Colours.BOARD_LIGHT if (row + column) % 2 == 0 else Colours.BOARD_DARK
            x = BORDER + column * SQUARE_SIZE
            y = BORDER + row    * SQUARE_SIZE
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))


def draw_sidebar(screen):
    """Draw the right sidebar panel for turn/winner display."""
    
    x = BOARD_PX + (BORDER * 2)
    y = 0
    width  = RIGHT_PANEL_WIDTH
    height = WINDOW_H
    
    pygame.draw.rect(screen, Colours.GREY, pygame.Rect(x, y, width, height))


def draw_border_labels(screen, font, game_mode):
    """Draw rank numbers and file letters centered in the border strips."""

    letters = "ABCDEFGH"

    for i in range(BOARD_SQUARES):
        center_offset = i * SQUARE_SIZE + SQUARE_SIZE // 2

        # --- File letters (A-H) on top and bottom border ---
        letters_surf = font.render(letters[i], True, Colours.LABEL)
        lx = BORDER + center_offset - letters_surf.get_width() // 2

        # Bottom border (normal)
        ly_bottom = BOARD_PX + BORDER + BORDER // 2 - letters_surf.get_height() // 2
        screen.blit(letters_surf, (lx, ly_bottom))

        # Top border
        letters_surf_top = font.render(letters[i], True, Colours.LABEL)

        if game_mode == "LOCAL":
            letters_surf_top = pygame.transform.rotate(letters_surf_top, 180)

        lx_top = BORDER + center_offset - letters_surf_top.get_width() // 2
        ly_top = BORDER // 2 - letters_surf_top.get_height() // 2
        screen.blit(letters_surf_top, (lx_top, ly_top))

        # --- Rank numbers (8-1) on left and right border ---
        numbers_surf = font.render(str(BOARD_SQUARES - i), True, Colours.LABEL)
        ny = BORDER + center_offset - numbers_surf.get_height() // 2

        # Left border (normal)
        nx_left = BORDER // 2 - numbers_surf.get_width() // 2
        screen.blit(numbers_surf, (nx_left, ny))

        # Right border
        numbers_surf_right = font.render(str(8 - i), True, Colours.LABEL)

        if game_mode == "LOCAL":
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


def draw_current_turn(screen, font, current_turn):
    """Display the current turn label on the right side - both player orientations."""

    turn_text = f"{current_turn}'s Turn"
    turn_surf = font.render(turn_text, True, Colours.LABEL)
    panel_center_x = BOARD_PX + BORDER + RIGHT_PANEL_WIDTH // 2
    
    # White player (bottom half - normal orientation)
    turn_x_white = WINDOW_W + (RIGHT_PANEL_WIDTH // 2) - turn_surf.get_width() // 2
    turn_y_white = int(WINDOW_H * 0.75) - turn_surf.get_height() // 2
    
    box_rect_white = pygame.Rect(
        turn_x_white - (V_PADDING + 10),
        turn_y_white - V_PADDING,
        turn_surf.get_width() + (V_PADDING + 10) * 2,
        turn_surf.get_height() + V_PADDING * 2
    )
    pygame.draw.rect(screen, Colours.BLACK, box_rect_white)
    screen.blit(turn_surf, (turn_x_white, turn_y_white))
    
    # Black player (top half - rotated 180 degrees)
    turn_surf_rotated = pygame.transform.rotate(turn_surf, 180)
    turn_x_black = WINDOW_W + (RIGHT_PANEL_WIDTH // 2) - turn_surf.get_width() // 2
    turn_y_black = int(WINDOW_H * 0.25) - turn_surf.get_height() // 2
    
    box_rect_black = pygame.Rect(
        turn_x_black - (V_PADDING + 10),
        turn_y_black - V_PADDING,
        turn_surf_rotated.get_width()  + (V_PADDING + 10) * 2,
        turn_surf_rotated.get_height() + (V_PADDING * 2)
    )
    pygame.draw.rect(screen, Colours.BLACK, box_rect_black)
    screen.blit(turn_surf_rotated, (turn_x_black, turn_y_black))


def winner_screen(screen, font, winner):
    """Display the winner on the right side - both player orientations. Press ESC to close."""
    
    text = f"{winner} wins!"
    winner_surf = font.render(text, True, Colours.LABEL)
    panel_center_x = BOARD_PX + BORDER + RIGHT_PANEL_WIDTH // 2
    
    # Wait for ESC key to close
    waiting_for_esc = True
    clock = pygame.time.Clock()
    while waiting_for_esc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_esc = False
        
        # White player (bottom half - normal orientation)
        x_white = WINDOW_W + (RIGHT_PANEL_WIDTH // 2) - winner_surf.get_width() // 2
        y_white = int(WINDOW_H * 0.75) - winner_surf.get_height() // 2
        
        box_rect_white = pygame.Rect(
            x_white - H_PADDING,
            y_white - V_PADDING,
            winner_surf.get_width()  + H_PADDING * 2,
            winner_surf.get_height() + V_PADDING * 2
        )
        pygame.draw.rect(screen, Colours.BLACK, box_rect_white)
        pygame.draw.rect(screen, Colours.CURSOR_NORMAL, box_rect_white, OUTLINE_THICKNESS)
        screen.blit(winner_surf, (x_white, y_white))
        
        # Black player (top half - rotated 180 degrees)
        winner_surf_rotated = pygame.transform.rotate(winner_surf, 180)
        x_black = WINDOW_W + (RIGHT_PANEL_WIDTH // 2) - winner_surf.get_width() // 2
        y_black = int(WINDOW_H * 0.25) - winner_surf.get_height() // 2
        
        box_rect_black = pygame.Rect(
            x_black - H_PADDING,
            y_black - V_PADDING,
            winner_surf_rotated.get_width()  + H_PADDING * 2,
            winner_surf_rotated.get_height() + V_PADDING * 2
        )
        pygame.draw.rect(screen, Colours.BLACK, box_rect_black)
        pygame.draw.rect(screen, Colours.CURSOR_NORMAL, box_rect_black, OUTLINE_THICKNESS)
        screen.blit(winner_surf_rotated, (x_black, y_black))
        
        pygame.display.flip()
        clock.tick(60)



# ---- GAME LOGIC AND INPUT HANDLING -------------------------------

def select_game_mode(screen, title_font, option_font, whole_window_w):
    """Display a simple menu to allow the player to choose between local and online play."""

    selecting = True
    selected = 0  # 0 = local, 1 = online

    options = ["Local Play", "Online Play"]

    while selecting:
        # Clear screen
        screen.fill(Colours.BOARD_BORDER)

        # Draw title
        title = title_font.render("- Select Game Mode -", True, Colours.LABEL)
        title_rect = title.get_rect(center = (whole_window_w // 2, (WINDOW_H // 2) - 200))
        screen.blit(title, title_rect)

        # Draw options
        for i, text in enumerate(options):
            colour = Colours.LABEL
            surf = option_font.render(text, True, colour)
            option_rect = surf.get_rect(center = (whole_window_w // 2, (WINDOW_H // 2) + (1.5 * i * option_font.get_height())))
            screen.blit(surf, option_rect)

            # Draw outline box around the selected option
            padding = 10
            box_rect = pygame.Rect(
                (whole_window_w // 2) - (GAMEMODE_OPTION_BOXSIZE_W // 2),
                option_rect.top - padding,
                GAMEMODE_OPTION_BOXSIZE_W,
                option_rect.height + padding * 2
            )
            box_colour = Colours.LABEL if i == selected else Colours.GREY
            box_outline = 10 if i == selected else 5
            pygame.draw.rect(screen, box_colour, box_rect, box_outline)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Move selection up
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2

                # Move selection down
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2

                # Confirm selection
                if event.key == pygame.K_RETURN:
                    return "LOCAL" if selected == 0 else "ONLINE"


def select_host_or_client(screen, font, whole_window_w):
    selecting = True
    selected = 0  # 0 = host, 1 = client

    options = ["Host Game", "Join Game"]

    while selecting:
        screen.fill(Colours.BOARD_BORDER)

        for i, text in enumerate(options):
            surf = font.render(text, True, Colours.LABEL)
            rect = surf.get_rect(center=(whole_window_w // 2, WINDOW_H // 2 + i * 100))
            screen.blit(surf, rect)

            box = pygame.Rect(rect.x - 20, rect.y - 10, rect.width + 40, rect.height + 20)
            pygame.draw.rect(screen, Colours.LABEL if i == selected else Colours.GREY, box, 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                if event.key == pygame.K_RETURN:
                    return "HOST" if selected == 0 else "CLIENT"


def handle_local_input(event, cursor, pieces, current_turn):
    """Handle all keyboard input for a local player controlling the cursor and making moves."""

    # Movement keys
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        cursor.move(-1, 0, BOARD_SQUARES)
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        cursor.move(1, 0, BOARD_SQUARES)
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        cursor.move(0, -1, BOARD_SQUARES)
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        cursor.move(0, 1, BOARD_SQUARES)

    # Pick up / Drop piece
    if event.key == pygame.K_SPACE:
        if cursor.holding is None:
            cell = pieces.board[cursor.row][cursor.column]

            # Only allow picking up current player's piece
            if cell is not None and cell["colour"] == current_turn:
                cursor.pickup(pieces.board)
        else:
            # Attempt to drop piece
            success, from_pos, to_pos = cursor.drop(pieces.board)
            return success, from_pos, to_pos

    # Cancel move
    if event.key == pygame.K_RETURN:
        if cursor.holding is not None:
            cursor.cancel(pieces.board)

    return False, None, None


def apply_move_of_piece(board, from_pos, to_pos):
    """Apply a move to the board by moving a piece from one position to another."""

    # Extract piece from original position
    piece = board[from_pos[0]][from_pos[1]]

    # Clear original square
    board[from_pos[0]][from_pos[1]] = None

    # Place piece at destination
    board[to_pos[0]][to_pos[1]] = piece



# ---- MAIN GAME LOOP ----------------------------------------------

def main():
    pygame.init()
    
    # Initialize fonts after pygame.init()
    label_font, winner_font, gamemode_title_font, gamemode_option_font = initialize_fonts()

    screen = pygame.display.set_mode((WHOLE_WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Chess Game")

    # Select game mode before starting
    game_mode = select_game_mode(screen, gamemode_title_font, gamemode_option_font, WHOLE_WINDOW_W)

    if game_mode == "ONLINE":
        role = select_host_or_client(screen, gamemode_option_font, WHOLE_WINDOW_W)

        if role == "HOST":
            net = Network(is_host=True)
            player_colour = WHITE
        else:
            ip = input("enter host ip: ")
            net = Network(is_host=False, ip=ip)
            player_colour = BLACK

    clock  = pygame.time.Clock()
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
                # Exit game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Test button
                if event.key == pygame.K_p:
                    test = True

                # handle movement and pickup/drop/cancel input based on game mode
                success, from_pos, to_pos = False, None, None

                if game_mode == "LOCAL":
                    success, from_pos, to_pos = handle_local_input(event, cursor, pieces, current_turn)

                elif game_mode == "ONLINE":

                    if current_turn == player_colour:
                        # your turn → allow input
                        success, from_pos, to_pos = handle_local_input(event, cursor, pieces, current_turn)

                        if success:
                            net.send({"from": from_pos, "to": to_pos})

                    else:
                        # opponent's turn → receive move
                        data = net.receive()
                        apply_move_of_piece(pieces.board, data["from"], data["to"])
                        success = True

                # Switch turn only if move succeeded
                if success:
                    current_turn = BLACK if current_turn == WHITE else WHITE
                    winner = check_winner(pieces.board)

        # Fill entire window with border color first
        screen.fill(Colours.BOARD_BORDER)

        # draw everything once
        draw_board(screen)
        draw_border_labels(screen, label_font, game_mode)
        draw_sidebar(screen)
        cursor.draw_valid_moves(screen, BORDER, SQUARE_SIZE, DOT_RADIUS)  # Grey dots under pieces
        pieces.draw(screen, BORDER, cursor.holding, cursor.holding_from)

        # Draw cursor
        cursor.draw(screen, BORDER, SQUARE_SIZE, CURSOR_THICKNESS)

        # Draw current turn label
        draw_current_turn(screen, label_font, current_turn)

        pygame.display.flip()
        clock.tick(60)

        if winner is not None or test:
            winner_screen(screen, winner_font, winner)
            pygame.quit()
            sys.exit()



# ---- RUN THE GAME ------------------------------------------------

if __name__ == "__main__":
    main()