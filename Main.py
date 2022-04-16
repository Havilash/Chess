import imp
import os
import numpy
import pygame

pygame.init()

WIDTH = 700
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption ("Chess")
MAX_FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)

FIELD_SPACING = ((WIDTH + HEIGHT)/2)/8


# --------------------------------Images--------------------------------------
#Figures
B_BISHOP_IMAGE = pygame.image.load(os.path.join('Assets','B_Bishop.png'))
B_KING_IMAGE = pygame.image.load(os.path.join('Assets','B_King.png'))
B_KNIGHT_IMAGE = pygame.image.load(os.path.join('Assets','B_Knight.png'))
B_PAWN_IMAGE = pygame.image.load(os.path.join('Assets','B_Pawn.png'))
B_QUEEN_IMAGE = pygame.image.load(os.path.join('Assets','B_Queen.png'))
B_ROOK_IMAGE = pygame.image.load(os.path.join('Assets','B_Rook.png'))
    
W_BISHOP_IMAGE = pygame.image.load(os.path.join('Assets','W_Bishop.png'))
W_KING_IMAGE = pygame.image.load(os.path.join('Assets','W_King.png'))
W_KNIGHT_IMAGE = pygame.image.load(os.path.join('Assets','W_Knight.png'))
W_PAWN_IMAGE = pygame.image.load(os.path.join('Assets','W_Pawn.png'))
W_QUEEN_IMAGE = pygame.image.load(os.path.join('Assets','W_Queen.png'))
W_ROOK_IMAGE = pygame.image.load(os.path.join('Assets','W_Rook.png'))

#Setup Figures
BB = pygame.transform.scale(B_BISHOP_IMAGE, (FIELD_SPACING, FIELD_SPACING))
BK = pygame.transform.scale(B_KING_IMAGE, (FIELD_SPACING, FIELD_SPACING))
BN = pygame.transform.scale(B_KNIGHT_IMAGE, (FIELD_SPACING, FIELD_SPACING))
BP = pygame.transform.scale(B_PAWN_IMAGE, (FIELD_SPACING, FIELD_SPACING))
BQ = pygame.transform.scale(B_QUEEN_IMAGE, (FIELD_SPACING, FIELD_SPACING))
BR = pygame.transform.scale(B_ROOK_IMAGE, (FIELD_SPACING, FIELD_SPACING))

WB = pygame.transform.scale(W_BISHOP_IMAGE, (FIELD_SPACING, FIELD_SPACING))
WK = pygame.transform.scale(W_KING_IMAGE, (FIELD_SPACING, FIELD_SPACING))
WN = pygame.transform.scale(W_KNIGHT_IMAGE, (FIELD_SPACING, FIELD_SPACING))
WP = pygame.transform.scale(W_PAWN_IMAGE, (FIELD_SPACING, FIELD_SPACING))
WQ = pygame.transform.scale(W_QUEEN_IMAGE, (FIELD_SPACING, FIELD_SPACING))
WR = pygame.transform.scale(W_ROOK_IMAGE, (FIELD_SPACING, FIELD_SPACING))

BLACK_FIGURES = [BB, BK, BN, BP, BQ, BR]
WHITE_FIGURES = [WB, WK, WN, WP, WQ, WR]

# -----------------------------------------------------------------------------


w_is_playing = True
white_short_castle_allowed = True
white_long_castle_allowed = True
black_short_castle_allowed = True
black_long_castle_allowed = True
pawn_is_transformating = False
white_en_passant_allowed = False
black_en_passant_allowed = False

wk_column = 7
wk_row = 4
bk_column = 0
bk_row = 4

temp_moveable = None
figure_is_chosen = False
temp_column = None
temp_row = None
white_is_playing = True


pygame.display.set_icon(BK)
field_array = (
    [BR, BN, BB, BQ, BK, BB, BN, BR],
    [BP, BP, BP, BP, BP, BP, BP, BP],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [WP, WP, WP, WP, WP, WP, WP, WP],
    [WR, WN, WB, WQ, WK, WB, WN, WR])

def moveable(figure, column, row):
    moveable_array = numpy.full((8, 8), False)
    global white_en_passant_allowed
    global black_en_passant_allowed
    if figure == BR or figure == WR:
        for i in range(4):
            # print(i)
            x, y = 0, 0
            while column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and (field_array[column + y][row + x] == None or (x == 0 and y == 0)):
                if i == 0:
                    moveable_array[column + y][row + x] = True
                    x += 1
                if i == 1:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                if i == 2:
                    moveable_array[column + y][row + x] = True
                    y += 1
                if i == 3:
                    moveable_array[column + y][row + x] = True
                    y -= 1
                if figure in WHITE_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in BLACK_FIGURES:
                    moveable_array[column + y][row + x] = True
                if figure in BLACK_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in WHITE_FIGURES:
                    moveable_array[column + y][row + x] = True

    if figure == BN or figure == WN:
        for x in [-1, 1]:
            for y in [-2, 2]:
                if column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0:
                    moveable_array[column + y][row + x] = True
        for x in [-2, 2]:
            for y in [-1, 1]:
                if column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0:
                    moveable_array[column + y][row + x] = True


    if figure == BB or figure == WB:
        for i in range(4):
            # print(i)
            x, y = 0, 0
            while column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and (field_array[column + y][row + x] == None or (x == 0 and y == 0)):
                if i == 0:
                    moveable_array[column + y][row + x] = True
                    x += 1
                    y += 1
                if i == 1:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                    y += 1
                if i == 2:
                    moveable_array[column + y][row + x] = True
                    x += 1
                    y -= 1
                if i == 3:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                    y -= 1
                if figure in WHITE_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in BLACK_FIGURES:
                    moveable_array[column + y][row + x] = True
                if figure in BLACK_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in WHITE_FIGURES:
                    moveable_array[column + y][row + x] = True


    if figure == BQ or figure == WQ:
        for i in range(8):
            # print(i)
            x, y = 0, 0
            while column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and (field_array[column + y][row + x] == None or (x == 0 and y == 0)):
                if i == 0:
                    moveable_array[column + y][row + x] = True
                    x += 1
                if i == 1:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                if i == 2:
                    moveable_array[column + y][row + x] = True
                    y += 1
                if i == 3:
                    moveable_array[column + y][row + x] = True
                    y -= 1

                if i == 4:
                    moveable_array[column + y][row + x] = True
                    x += 1
                    y += 1
                if i == 5:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                    y += 1
                if i == 6:
                    moveable_array[column + y][row + x] = True
                    x += 1
                    y -= 1
                if i == 7:
                    moveable_array[column + y][row + x] = True
                    x -= 1
                    y -= 1
                if figure in WHITE_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in BLACK_FIGURES:
                    moveable_array[column + y][row + x] = True
                if figure in BLACK_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in WHITE_FIGURES:
                    moveable_array[column + y][row + x] = True   


    if figure == BK or figure == WK:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if column + i < 8 and column + i >= 0 and row + j < 8 and row + j >= 0: 
                    moveable_array[column + i][row + j] = True

        #Castle
        if figure == WK:
            if white_short_castle_allowed and field_array[column][row + 1] == None and field_array[column][row + 2] == None:
                moveable_array[column][row + 2] = True
            if white_long_castle_allowed and field_array[column][row - 1] == None and field_array[column][row - 2] == None and field_array[column][row - 3] == None:
                moveable_array[column][row - 2] = True
        if figure == BK:
            if black_short_castle_allowed and field_array[column][row + 1] == None and field_array[column][row + 2] == None:
                moveable_array[column][row + 2] = True
            if black_long_castle_allowed and field_array[column][row - 1] == None and field_array[column][row - 2] == None and field_array[column][row - 3] == None:
                moveable_array[column][row - 2] = True

    if figure == BP or figure == WP:
        if figure == WP:
            if field_array[column - 1][row] == None:
                if column == 6:
                    moveable_array[column - 1][row] = True
                    if field_array[column - 2][row] == None:
                        moveable_array[column - 2][row] = True
                        # black_en_passant_allowed = True
                else:
                    moveable_array[column - 1][row] = True
            if column - 1 < 8 and column - 1 >= 0 and row + 1 < 8 and row + 1 >= 0 and field_array[column - 1][row + 1] in BLACK_FIGURES:
                moveable_array[column - 1][row + 1] = True
            if column - 1 < 8 and column - 1 >= 0 and row - 1 < 8 and row - 1 >= 0 and field_array[column - 1][row - 1] in BLACK_FIGURES:
                moveable_array[column - 1][row - 1] = True
            if white_en_passant_allowed and column - 1 < 8 and column - 1 >= 0 and row + 1 < 8 and row - 1 >= 0 and field_array[column][row + 1] in BLACK_FIGURES:
                moveable_array[column - 1][row + 1] = True
                # field_array[column][row + 1] = None
            if white_en_passant_allowed and column - 1 < 8 and column - 1 >= 0 and row - 1 < 8 and row - 1 >= 0 and field_array[column][row - 1] in BLACK_FIGURES:
                moveable_array[column - 1][row - 1] = True


        elif figure == BP:
            if field_array[column + 1][row] == None:
                if  column == 1:
                    moveable_array[column + 1][row] = True
                    if field_array[column + 2][row] == None:
                        moveable_array[column + 2][row] = True
                        # white_en_passant_allowed = True
                else:
                    moveable_array[column + 1][row] = True
            if column + 1 < 8 and column + 1 >= 0 and row + 1 < 8 and row + 1 >= 0 and field_array[column + 1][row + 1] in WHITE_FIGURES:
                moveable_array[column + 1][row + 1] = True
            if column + 1 < 8 and column + 1 >= 0 and row - 1 < 8 and row - 1 >= 0 and field_array[column + 1][row - 1] in WHITE_FIGURES:
                moveable_array[column + 1][row - 1] = True

    for x in range(8):
        for y in range(8):
            if figure in WHITE_FIGURES and moveable_array[y][x] and field_array[y][x] in WHITE_FIGURES:
                moveable_array[y][x] = False
            if figure in BLACK_FIGURES and moveable_array[y][x] and field_array[y][x] in BLACK_FIGURES:
                moveable_array[y][x] = False
    return moveable_array



pawn_transformation_figures = [None, None, None, None]
pawn_window_spacing = (WIDTH - 40)/8
pawn_column, pawn_row = None, None
def pawn_transformation_window(figures, column, row):
    x = 0
    global pawn_transformation_figures, pawn_is_transformating, pawn_column, pawn_row
    pawn_column = column
    pawn_row = row
    pawn_is_transformating = True
    pygame.draw.rect(WIN, (120, 120, 120), pygame.Rect(WIDTH/2-pawn_window_spacing*2, HEIGHT/2 - 60, pawn_window_spacing*4, FIELD_SPACING + 40))
    for i in figures:
        # print(i, " : ", pawn_transformation_figures)
        pawn_transformation_figures[x] = i
        WIN.blit(
            pygame.transform.scale(i, (pawn_window_spacing, pawn_window_spacing)),
            (x * pawn_window_spacing + WIDTH/2-pawn_window_spacing*2, HEIGHT/2 - 40))
        x += 1
    pygame.display.update()

def check_king():
    global probably_attacker
    attacker_x = [None]
    attacker_y = [None]
    is_nearest_attacker = True
    moveable_array = numpy.full((8, 8), False)
    for i in range(8):
        # print(i)
        x, y = 0, 0
        while wk_column + y < 8 and wk_column + y >= 0 and wk_row + x < 8 and wk_row + x >= 0 and field_array[wk_column + y][wk_row + x] in BLACK_FIGURES:
            if i == 0:
                x += 1
            if i == 1:
                x -= 1
            if i == 2:
                y += 1
            if i == 3:
                y -= 1
            if i == 4:
                x += 1
                y += 1

            if i == 5:
                x -= 1
                y += 1
            if i == 6:
                x += 1
                y -= 1
            if i == 7:
                x -= 1
                y -= 1

            if i >= 0 and i <= 4 and (field_array[y][x] == BQ or field_array[y][x] == BR):
                attacker_x[i] = x
                attacker_y[i] = y
            if i >= 5 and i <= 7 and (field_array[y][x] == BQ or field_array[y][x] == BB):
                attacker_x[i] = x
                attacker_y[i] = y

            if WK in WHITE_FIGURES and wk_column + y < 8 and wk_column + y >= 0 and wk_row + x < 8 and wk_row + x >= 0 and field_array[wk_column + y][wk_row + x] in BLACK_FIGURES:
                moveable_array[wk_column + y][wk_row + x] = True
            # if figure in BLACK_FIGURES and column + y < 8 and column + y >= 0 and row + x < 8 and row + x >= 0 and field_array[column + y][row + x] in WHITE_FIGURES:
            #     moveable_array[column + y][row + x] = True   


    for x in [-1, 1]:
        for y in [-2, 2]:
            if wk_column + y < 8 and wk_column + y >= 0 and wk_row + x < 8 and wk_row + x >= 0:
                pass
    for x in [-2, 2]:
        for y in [-1, 1]:
            if wk_column + y < 8 and wk_column + y >= 0 and wk_row + x < 8 and wk_row + x >= 0:
                pass
    print(moveable_array)


def draw_window():
    WIN.fill(GRAY)
    i = 0
    #Field
    for y in range(8):
        for x in range(i, 9, 2):
            pygame.draw.rect(WIN, WHITE, pygame.Rect(x * FIELD_SPACING, y * FIELD_SPACING, FIELD_SPACING, FIELD_SPACING))
        if i == 0:
            i = 1
        elif i == 1:
            i = 0
    #Figures
    for y in range(8):
        for x in range(8):
            if field_array[y][x] != None:
                WIN.blit(field_array[y][x], (x*FIELD_SPACING, y*FIELD_SPACING))
    # pawn_transformation_window([WR, WN, WB, WQ])
    # pawn_tranformation_window([BR, BN, BB, BQ])
    
    
    
    pygame.display.update()

def handle_castle(column, row):
    global white_long_castle_allowed, white_short_castle_allowed, black_long_castle_allowed, black_short_castle_allowed

    if white_short_castle_allowed and temp_row + 2 == row and field_array[column][row] == WK:
        field_array[7][7] = None
        field_array[7][5] = WR
    if white_long_castle_allowed and temp_row - 2 == row and field_array[column][row] == WK:
        field_array[7][0] = None
        field_array[7][3] = WR
    if black_short_castle_allowed and temp_row + 2 == row and field_array[column][row] == BK:
        field_array[0][7] = None
        field_array[0][5] = BR
    if black_long_castle_allowed and temp_row - 2 == row and field_array[column][row] == BK:
        field_array[0][0] = None
        field_array[0][3] = BR


    if temp_column == 7 and temp_row == 7:
        white_short_castle_allowed = False
    if temp_column == 7 and temp_row == 0:
        white_long_castle_allowed = False
    if temp_column == 0 and temp_row == 7:
        black_short_castle_allowed = False
    if temp_column == 0 and temp_row == 0:
        black_long_castle_allowed = False
    if field_array[temp_column][temp_row] == WK:
        white_short_castle_allowed = False
        white_long_castle_allowed = False
    if field_array[temp_column][temp_row] == BK:
        black_short_castle_allowed = False
        black_long_castle_allowed = False


def handle_mouseclick(column, row, figure_color):
    global temp_moveable, figure_is_chosen, temp_column, temp_row, white_is_playing, wk_column, wk_row, bk_column, bk_row, white_en_passant_allowed
    if figure_is_chosen and moveable(field_array[temp_column][temp_row], temp_column, temp_row)[column][row]:        
        if field_array[temp_column][temp_row] == WK:
            wk_column = column
            wk_row = row
        if field_array[temp_column][temp_row] == BK:
            bk_column = column
            bk_row = row
        if field_array[column][row] == BP and temp_column == 1 and column == 3:
            white_en_passant_allowed = True
        else:
            white_en_passant_allowed = False
        print(white_en_passant_allowed)
        
        field_array[column][row] = field_array[temp_column][temp_row]
        field_array[temp_column][temp_row] = None
        figure_is_chosen = False
        if(white_is_playing):
            white_is_playing = False
        else:
            white_is_playing = True
        handle_castle(column, row)
        draw_window()
        if field_array[column][row] == WP and column == 0:
            pawn_transformation_window([WR, WN, WB, WQ], column, row)
        elif field_array[column][row] == BP and column == 7:
            pawn_transformation_window([BR, BN, BB, BQ], column, row)
        # check_king()
        # print(white_long_castle_allowed, white_short_castle_allowed, black_long_castle_allowed, black_short_castle_allowed)
        # print(field_array)

    elif field_array[column][row] in figure_color:
        temp_column = column
        temp_row = row
        figure_is_chosen = True
        temp_moveable = moveable(field_array[temp_column][temp_row], temp_column, temp_row)
        draw_window()
        for y in range(8):
            for x in range(8):
                if temp_moveable[y][x] and figure_is_chosen:
                    # print(temp_moveable) 
                    pygame.draw.circle(WIN, (100, 100, 100), (x * FIELD_SPACING + FIELD_SPACING/2, y * FIELD_SPACING + FIELD_SPACING/2), 10)
        pygame.display.update()
    # print(temp_moveable) 

def main():
    is_running = True
    clock = pygame.time.Clock()
    global pawn_is_transformating
    pawn_is_transformating = False
    draw_window()
    while is_running:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                row = int(mouse_pos[0]/WIDTH*8)
                column = int(mouse_pos[1]/HEIGHT*8)
                # print(column, row)
                if white_is_playing and pawn_is_transformating == False:
                    handle_mouseclick(column, row, WHITE_FIGURES)
                elif white_is_playing == False and pawn_is_transformating == False:
                    handle_mouseclick(column, row, BLACK_FIGURES)
                if pawn_is_transformating:
                    for i in range(4):
                        if(mouse_pos[0] > i * pawn_window_spacing + WIDTH/2-pawn_window_spacing*2 and mouse_pos[0] < (i+1) * pawn_window_spacing + WIDTH/2-pawn_window_spacing*2 and mouse_pos[1] > HEIGHT/2 - 40 and mouse_pos[1] < HEIGHT/2 + 40):
                            field_array[pawn_column][pawn_row] = pawn_transformation_figures[i]
                            pawn_is_transformating = False
                            draw_window()


    pygame.quit()


if __name__ == "__main__":
    main()
