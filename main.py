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
    
    # Game loop that handles events and updates
    last_square = []
    last_piece = []
    valid_moves = []
    running = True
    while running:
        create_board(screen) 
        for event in pg.event.get():
            # Close window if pressed
            if event.type == pg.QUIT:
                running = False
            # Event click
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get mouse position and store as X/Y values that correspond to each square
                # Retrieve square coordinates, piece type, and piece colour
                location = pg.mouse.get_pos()
                col = location[0] // SQUARE_SIZE 
                row = location[1] // SQUARE_SIZE
                selected_square = [row, col]
                selected_piece = game_state.board[row][col]
                selected_piece_colour = selected_piece[0]
                print("row:" + str(row) + " col: " + str(col))
                #If no prior selection, check if new selection is valid
                if not last_square:
                    #Check if the player is selecting their own pieces on their turn
                    #Select the piece if so and generate an array of valid moves
                    if selected_piece_colour == game_state.current_turn:
                        last_square = selected_square
                        last_piece = selected_piece
                        print("Piece selected")
                        valid_moves = game_state.generate_valid_moves(row, col, selected_piece, selected_piece_colour)
                        
                        
                    else:
                        print("Selection is invalid.")
                #If same square is already selected, unselect 
                elif last_square == selected_square:
                        last_square = []
                        last_piece = []
                        print("Unselected piece")
                #New square selected
                elif last_square != selected_square:
                    print("Selected square: " + str(selected_square))
                    #Check if move is valid, and then move
                    if (row, col) in valid_moves:
                        print("Piece moved")
                        game_state.move(last_square, selected_square, last_piece)
                        last_square = []
                        valid_moves = []
                        game_state.change_turn()
                    else:
                        print("Invalid move")
                       

                    
                    

        #Update Graphics
        if last_piece:        
            highlight_squares(screen, valid_moves, row, col)     
        create_pieces(screen, game_state.board)
        clock.tick(MAX_FPS)
        pg.display.update()

def highlight_squares(screen, valid_moves, row, col):
    s = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
    s.set_alpha(100)
    s.fill(pg.Color('blue'))
    screen.blit(s, (col * SQUARE_SIZE, row *SQUARE_SIZE))
    s.fill(pg.Color('yellow'))
    for move in valid_moves:
        screen.blit(s, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE))

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
