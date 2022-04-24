# Responsible for storing current game state, determining valid moves
class GameState():
    def __init__(self):
        self.starting_board()
        self.current_turn = "w"
        self.check = False
        self.movelog = {}
        self.white_king_square = [7, 4]
        self.black_king_square = [0, 4]
        self.row_notation = {7: "1", 6 : "2", 5 : "3", 4 : "4", 3: "5", 2 : "6", 1 : "7", 0 : 6}
        self.col_notation = {0: "a", 1 : "b", 2 : "c", 3 : "d", 4: "e", 5 : "f", 6 : "g", 7 : "h"}
        self.en_passant_square = []
    # 8x8 2D list represents the board
    # First character represents Black/White
    # Second character represents the piece type R, N, B, K, P
    # -- Represents empty space
    def starting_board(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
    
    #Converts row/col references to our board into chess notation: e.g 7 (row) / 4 (col) becomes e1 - where 7 is 1 and e is 4
    def convert_rows(self, row, col):
        print(self.col_notation[col] + self.row_notation[row])
        return self.col_notation[col] + self.row_notation[row]
    # Move the piece - original square is now blank, new square is now filled with the old piece.
    # Piece at the new square is automatically overwritten if it exists.
    def move(self, last_square, selected_square, moved_piece):
        self.board[last_square[0]][last_square[1]] = "--"
        
        moved_piece_type = moved_piece[1]
        moved_piece_colour = moved_piece[0]

        #If the moving piece is a King, update its location tracker
        if moved_piece_type == "K":
            if moved_piece_colour == "w":
                self.white_king_square = selected_square
            else:
                self.black_king_square = selected_square
        #If the moving piece is a pawn and its reached the opposite end, promote it
        if moved_piece_type == "P" and moved_piece_colour == "w" and selected_square[0] == 0:
                self.board[selected_square[0]][selected_square[1]] = "wQ"
        elif moved_piece_type == "P" and moved_piece_colour == "b" and selected_square[0] == 7:
                self.board[selected_square[0]][selected_square[1]] = "bQ"
        #If no promotion, just move the piece
        else:
                self.board[selected_square[0]][selected_square[1]] = moved_piece

        # En Passant - If the selected square is eligible for en passant, capture the pawn above the square
        if self.en_passant_square == selected_square:
            print("Success: " + str(selected_square[0]))
            if selected_square[0] == 2 and moved_piece_colour == "w":
                self.board[selected_square[0] + 1][selected_square[1]] = "--"
            if selected_square[0] == 5 and moved_piece_colour == "b":
                print("Success")
                self.board[selected_square[0] - 1][selected_square[1]] = "--"
        
        print("Last square: " + str(last_square[0]) + "Selected square: " + str(selected_square[0]) + "L + 2: " + str(last_square[0] + 2))
        #Set en passant squares
        if moved_piece_type == "P" and moved_piece_colour == "b" and last_square[0] + 2 == selected_square[0]:
            self.en_passant_square = [selected_square[0] - 1, selected_square[1]]
            print("En Passant white")
        elif moved_piece_type == "P" and moved_piece_colour == "w" and last_square[0] - 2 == selected_square[0]:
            self.en_passant_square = [selected_square[0] + 1, selected_square[1]]
            print("En Passant black")
        else:
            self.en_passant_square = []
        
        if self.en_passant_square:
            print("En passant square: " + str(self.en_passant_square))


            

    def change_turn(self):
        if self.current_turn == "w":
            self.current_turn = "b"
        else:
            self.current_turn = "w"
    def generate_valid_moves(self, row, col, selected_piece, selected_piece_colour):
        selected_piece_type = selected_piece[1]
        self.valid_moves = []

        # Pawn
        if selected_piece_type == "P":
            # White pawn
            if selected_piece_colour == "w":
                self.validate_pawn_move(row, col, -1, +1, 6, selected_piece, selected_piece_colour)
            # Black pawn
            else:
                self.validate_pawn_move(row, col, +1, -1, 1, selected_piece, selected_piece_colour)
        # Knight
        if selected_piece_type == "N":
            self.validate_knight(row, col, selected_piece, selected_piece_colour)     
        # Rook
        if selected_piece_type == "R":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
            self.check_line(directions, 7, row, col, selected_piece, selected_piece_colour)
        # Queen
        if selected_piece_type == "Q":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, row, col, selected_piece, selected_piece_colour)
        # Bishop
        if selected_piece_type == "B":
            directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, row, col, selected_piece, selected_piece_colour)
        # King
        if  selected_piece_type == "K":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 1, row, col, selected_piece, selected_piece_colour)
        
        return self.valid_moves

    def validate_pawn_take(self, row, col, new_row, new_col, selected_piece, selected_piece_colour):
        # Skip check if diaganal is off the board
        if new_col < 0 or new_row < 0 or new_col > 7 or new_row > 7:
            return
        else:
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid
            if not self.move_results_in_check(row, col, new_row, new_col, selected_piece, selected_piece_colour):
                # Add to valid moves there is a piece on the diaganal square and the piece is a different colour
                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                if piece != "--" and piece_colour != selected_piece_colour:
                    self.valid_moves.append((new_row, new_col))

    def validate_pawn_move(self, row, col, a, b, starting_row, selected_piece, selected_piece_colour):
        # Check for pieces on diagnal to take
        self.validate_pawn_take(row, col, row + a, col + a, selected_piece, selected_piece_colour)
        self.validate_pawn_take(row, col, row + a, col + b, selected_piece, selected_piece_colour)
        #En Passant Check
        if self.en_passant_square == [row + a, col - 1] or self.en_passant_square == [row + a, col + 1]:
            print("En passant detected")
            replaced_piece = self.board[self.en_passant_square[0] + b][self.en_passant_square[1]]
            self.board[self.en_passant_square[0] + b][self.en_passant_square[1]] = "--"
            if not self.move_results_in_check(row, col, self.en_passant_square[0], self.en_passant_square[1], selected_piece, selected_piece_colour):
                self.valid_moves.append((self.en_passant_square[0], self.en_passant_square[1]))
            self.board[self.en_passant_square[0] + b][self.en_passant_square[1]] = replaced_piece
         
               


        # Check if pawn is on starting position, if so allow double move
        if row == starting_row:
            x = 3
        else:
            x = 2

        for i in range(1, x):
            new_row = row + (i * a)
            piece = self.board[new_row][col]
            # If there is a piece in the way, we can't move there - return before added to valid moves
            if piece != "--":
                return
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid - skip to next move
            if self.move_results_in_check(row, col, new_row, col, selected_piece, selected_piece_colour):
                print("Check")
            else:
                self.valid_moves.append((new_row, col))

    def validate_knight(self, row, col, selected_piece, selected_piece_colour):
        # Iterate through a set of coordinates to check if every possible move is valid
        knight_moveset = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1), (-1, 2))
        for move in knight_moveset:
            new_row = row + move[0]
            new_col = col + move[1]
            # Skip check if position is off the board
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                # Simulates the move and then checks if the move would result in check for the moving player's king.
                # If it does, move is not valid - skip to next move
                if self.move_results_in_check(row, col, new_row, new_col, selected_piece, selected_piece_colour):
                    continue
                # Move is valid if the colour is different
                if piece_colour != selected_piece_colour:
                    self.valid_moves.append((new_row, new_col))
    
    def check_line(self, directions, length, row, col, selected_piece, selected_piece_colour):
        for direction in directions:
            a = direction[0]    
            b = direction[1]
            for i in range(length):
                new_col = col + b
                new_row = row + a
                # End loop if square is out of bounds
                if new_col >= 8 or new_col <= -1 or new_row >= 8 or new_row <= -1:
                    break

                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                # If the piece is the same colour, we stop before it is added to the list (attacking piece is blocked)
                if piece_colour == selected_piece_colour:
                    break
                # If the piece is another colour, we add it to the list and then stop (defending piece is taken)
                if piece != "--":
                    #Check if move results in check before adding it to the list
                    if self.move_results_in_check(row, col, new_row, new_col, selected_piece, selected_piece_colour):
                         print("Check")
                    else:
                        self.valid_moves.append((new_row, new_col))
                    break
                # Iterate the loop by moving in the direction
                a += direction[0]
                b += direction[1]
                #Check if move results in check before adding it to the list
                if self.move_results_in_check(row, col, new_row, new_col, selected_piece, selected_piece_colour):
                    print("Check")
                else: 
                    #Square is empty and doesn't result in check - allow move
                    self.valid_moves.append((new_row, new_col))

          
                
        
    def move_results_in_check(self, row, col, new_row, new_col, selected_piece, selected_piece_colour):
        pin = False
        selected_piece_type = selected_piece[1]
        # Moves the piece to the new location and deletes it from the old location
        # saving the piece it replaces to put it back later
        self.board[row][col] = "--"
        replaced_piece = self.board[new_row][new_col]
        self.board[new_row][new_col] = selected_piece

        # If its the king moving then update its position (used in check pin function)
        if selected_piece_type == "K":
            king_square = (new_row, new_col)
            #Check if a knight covers the square the king is moving to
        else:
            if selected_piece_colour == "w":
                king_square = self.white_king_square
            else:
                king_square = self.black_king_square
        #Horizontal pin check
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        pin = self.move_results_in_knight_check(selected_piece_colour, king_square)
        if not pin:
            pin = self.check_pin(directions, selected_piece_colour, king_square, "Line")
        if not pin:
            #Diaganal pin check
            directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
            pin = self.check_pin(directions, selected_piece_colour, king_square, "Diaganal")

      
        # Reverts the board state to how it was originally
        self.board[row][col] = selected_piece
        self.board[new_row][new_col] = replaced_piece

        # Check to see if king is in check now, returns True if so
        if pin:
            return True
        else:
            return False
    
    def move_results_in_knight_check(self, selected_piece_colour, king_square):
        knight_moveset = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1), (-1, 2))
        for move in knight_moveset:
            new_row = king_square[0] + move[0]
            new_col = king_square[1] + move[1]
            # Skip check if position is off the board
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                piece = self.board[new_row][new_col]
                piece_type = piece[1]
                piece_colour = piece[0]
                # Enemy Knight covers this square
                if piece_type == "N" and piece_colour != selected_piece_colour:
                    print("Knight found")
                    return True

    def check_pin(self, directions, selected_piece_colour, king_square, directiontype):
        for direction in directions:
            row = direction[0]
            col = direction[1]
            for d in range(7):
                new_col = king_square[1] + col
                new_row = king_square[0] + row
                # End loop if square is out of bounds
                if new_col >= 8 or new_col <= -1 or new_row >= 8 or new_row <= -1:
                    break
                # Get details of the iterated square
                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                piece_type = piece[1]

                # If the square empty, it will skip these checks and iterate the next square
                if piece != "--":
                    # If the colour is different, it will stop iterating in this direction
                    # as a friendly piece is blocking the vision
                    if piece_colour != selected_piece_colour:
                        # If the direction is the same as the type of piece that can take in that direction,
                        # we are in check
                        if piece_type == "K" and d == 0:
                            return True
                        if piece_type == "P" and d == 0 and directiontype == "Diaganal":
                            print("Diaganal pawn pin at " + str(new_row) + "." + str(new_col))
                            return True

                        if directiontype == "Line":
                            if piece_type == "R" or piece_type == "Q":
                                print("Line pin at " + str(new_row) + "." + str(new_col))
                                return True
                        if directiontype == "Diaganal":
                            if piece_type == "Q" or piece_type == "B":
                                print("Diaganal pin at " + str(new_row) + "." + str(new_col))
                                return True
                        # All remaining options are enemy pieces which cannot take in this direction,
                        # stop iterating this direction as the vision of other pieces are blocked
                        break
                    else:
                        break
                # Iterate the loop by moving in the direction
                row += direction[0]
                col += direction[1]