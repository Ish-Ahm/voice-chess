import pygame 
import sys 

pygame.init()
pygame.display.set_mode((100,100),pygame.HIDDEN)
font = pygame.font.SysFont('segoeuisymbol, arialunicodems, applesymbols, menlo', 150)

TILE_SIZE = 200
pieces = ['♚', '♛', '♜', '♝', '♞', '♟']

spritesheet = pygame.Surface((TILE_SIZE * len(pieces), TILE_SIZE * 2), pygame.SRCALPHA)

def draw_piece_to_sheet(surface, symbol, center_x, center_y, fill_color, outline_color):
    outline_width = 3
    outline_text = font.render(symbol, True, outline_color)
    outline_rect = outline_text.get_rect(center=(center_x, center_y))

    for dx in [-outline_width, 0, outline_width]:
        for dy in [outline_width, 0, -outline_width]:
            if dx != 0 or dy != 0:
                surface.blit(outline_text, outline_rect.move(dx, dy))

    fill_text = font.render(symbol, True, fill_color)
    fill_rect = fill_text.get_rect(center=(center_x, center_y))
    surface.blit(fill_text, fill_rect)

print('Generating chess piece spritesheet...')

for i, symbol in enumerate(pieces):
    x_pos = (i * TILE_SIZE) + (TILE_SIZE // 2)
    y_pos = TILE_SIZE//2
    
    draw_piece_to_sheet(spritesheet, symbol, x_pos, y_pos, fill_color=(255, 255, 255), outline_color=(0, 0, 0))

for i, symbol in enumerate(pieces):
    x_pos = (i * TILE_SIZE) + (TILE_SIZE // 2)
    y_pos = TILE_SIZE + (TILE_SIZE//2)
    
    draw_piece_to_sheet(spritesheet, symbol, x_pos, y_pos, fill_color=(0,0,0), outline_color=(255,255,255))
output_filename = 'chess_pieces_spritesheet.png'
pygame.image.save(spritesheet, output_filename)

print(f"Success! Saved all pieces to '{output_filename}'.")

pygame.quit()
sys.exit()