import pygame

import button
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from checkers.board import Board

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

game_paused = False
menu_state = 'main'

one_player_img = pygame.image.load("assets/1player.png").convert_alpha()
two_players_img = pygame.image.load("assets/2players.png").convert_alpha()
quit_img = pygame.image.load("assets/quit.png").convert_alpha()

one_player_button = button.Button(304, 125, one_player_img, 1)
two_players_button = button.Button(304, 250, two_players_img, 1)
quit_button = button.Button(307, 375, quit_img, 1)

# define fonts
font = pygame.font.SysFont('Helvetica', 30, True)

# define colours
TEXT_COL = (255, 255, 255)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_width = img.get_width()
    text_height = img.get_height()
    WIN.blit(img, (x - text_width // 2, y - text_height // 2))


def main():
    global game_paused, menu_state, whowin
    run = True
    clock = pygame.time.Clock()
    # game = Game(WIN)

    while run:
        clock.tick(FPS)

        WIN.fill((52, 78, 91))

        if game_paused:
            if menu_state == "main":
                if one_player_button.draw(WIN):
                    game = Game(WIN)
                    menu_state = "1player"
                if two_players_button.draw(WIN):
                    game = Game(WIN)
                    menu_state = "2players"
                if quit_button.draw(WIN):
                    run = False
            if menu_state == "1player":

                # play with AI
                if game.turn == WHITE:
                    value, new_board = minimax(game.get_board(), 4, WHITE, game)
                    game.ai_move(new_board)

                winner = game.board.check_turn(game.turn)
                if winner:
                    if winner == RED:
                        whowin = "RED won"
                    else:
                        whowin = "WHITE won"
                    menu_state = "won"

                if game.winner() is not None:
                    if game.winner() == RED:
                        whowin = "RED won"
                    else:
                        whowin = "WHITE won"
                    menu_state = "won"
                    # run = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        game.select(row, col)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_paused = True

                game.update()
            if menu_state == "2players":
                winner = game.board.check_turn(game.turn)
                if winner:
                    if winner == RED:
                        whowin = "RED won"
                    else:
                        whowin = "WHITE won"
                    menu_state = "won"

                if game.winner() is not None:
                    if game.winner() == RED:
                        whowin = "RED won"
                    else:
                        whowin = "WHITE won"
                    menu_state = "won"
                    # run = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        game.select(row, col)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_paused = True

                game.update()
            if menu_state == "won":
                draw_text(whowin, font, TEXT_COL, WIDTH // 2, HEIGHT // 2)
        else:
            draw_text("Welcome to Checkers!", font, TEXT_COL,  WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Press Space to continue!", pygame.font.SysFont('Helvetica', 20), TEXT_COL, WIDTH // 2, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
