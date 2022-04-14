#Responsible for user input and setting game state
import pygame as pg
import engine

pg.init()
# Constants
WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
IMAGES = {}
MAX_FPS = 15
COLOURS = pg.Color("white"), pg.Color("gray")

# Initialize piece images
def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for pieces in pieces:
        IMAGES[pieces] = pg.image.load("images/" + pieces + ".png")
        pg.transform.scale(IMAGES[pieces], (SQUARE_SIZE, SQUARE_SIZE)),

def main():
    # Setup our window, clock, preload the images, load the game state
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    game_state = engine.GameState()
    original_piece = []
    load_images()
    create_board(screen)   
    create_pieces(screen, game_state.board)
    clock.tick(MAX_FPS)
    pg.display.update()

    # Game loop that handles events and updates
    last_selection = []
    running = True
    while running:
        for event in pg.event.get():
            # Close window if pressed
            if event.type == pg.QUIT:
                running = False
            # Event click
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get mouse position and store as X/Y values that correspond to each square
                # Retrieve piece selected from that position on the board
                location = pg.mouse.get_pos()
                square_y = location[0] // SQUARE_SIZE 
                square_x = location[1] // SQUARE_SIZE
                selected_piece = game_state.board[square_x][square_y]
                selected_piece_colour = selected_piece[0]

                #No piece is already selected
                if not last_selection:
                    #Check if the player is selecting their own pieces on their turn
                    #Set piece selection to true
                    if selected_piece_colour == "w" and game_state.current_turn == 0 or \
                       selected_piece_colour == "b" and game_state.current_turn == 1:
                        print("Piece selected")
                        last_selection = selected_piece
                    elif selected_piece_colour == "-":
                        print("Nothing selected")
                #Piece is already selected
                else:
                    #Selected same piece as the previous click, unselect the piece
                    if last_selection == selected_piece:
                        last_selection = []
                        print("Unselected piece")
                    

# Creates the board
def create_board(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # Calculates whether the coordinates added together are odd or even
            # - black squares are always odd and white squares are always even
            colour = COLOURS[((r + c) % 2)]
            pg.draw.rect(screen, colour, pg.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# Creates the pieces on the board
def create_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            # If not empty, creates the corresponding piece
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()
