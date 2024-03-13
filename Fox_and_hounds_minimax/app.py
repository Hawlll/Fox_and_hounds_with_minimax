import pygame as pyg
from constants import *
from board import Board
from draw_pieces import draw_piece
from minimax import minimax


class App:
    def __init__(self) -> None:
        self.win = pyg.display.set_mode((WIDTH, HEIGHT))
        self.title = pyg.display.set_caption("Fox and Hounds with minimax")
        self.clock = pyg.time.Clock()
        self.fps = 30
        self.board = Board()

        self.HOUND_PATH = "Fox_and_hounds_minimax/piece_pics/hound_pic.png"
        self.FOX_PATH = "Fox_and_hounds_minimax/piece_pics/fox_pic.png"
        self.player_1 = FOX_ICON
        self.hound_selected = None
        self.player_2 = HOUND_ICON
        self.current_turn = self.player_1

        self.buffer = pyg.Surface((WIDTH, HEIGHT))
    
    def draw_board(self):
        """
        draw_board() graphically draws board by looping through grid of Board object

        Parameters: None

        """
        self.buffer.fill(BLACK)

        for row in range(ROWS):
            for col in range(COLS):
                block = (col*BLOCK_SIZE, row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                color = ORANGE if not (col+row) % 2 else BLACK
                pyg.draw.rect(self.buffer, color, block)
                
                piece = self.board.getBoard()[row][col] 
                if piece == HOUND_ICON:
                    draw_piece(self.buffer, col*BLOCK_SIZE, row*BLOCK_SIZE, self.HOUND_PATH)
                elif piece == FOX_ICON:
                    draw_piece(self.buffer, col*BLOCK_SIZE, row*BLOCK_SIZE, self.FOX_PATH)

        self.win.blit(self.buffer, (0,0))
    
    def ai_move(self):
        """
        ai_move() calls minimax() to get best move for ai player and then calls move() to move on board

        Parameters: None
        
        """
        if self.player_2 == HOUND_ICON:
            _, move = minimax(self.board, True, AI_DIFFICULTY)
            self.board.move(col=move[0], row=move[1], player=self.player_2, hound_pos=[move[2][0], move[2][1]])
            print("AI MOVED TO", move[0], move[1])
        elif self.player_2 == FOX_ICON:
            _, move = minimax(self.board, False, AI_DIFFICULTY)
            self.board.move(col=move[0], row=move[1], player=self.player_2)
            print("AI MOVED TO", move[0], move[1])

    def run(self):
        """
        run() runs main game loop

        Parameters: None
        
        """

        self.board.create_start_board()
        self.draw_board()

        running = True
        while running:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    print("Exiting App...")
                    running = False
                if self.board.is_win(FOX_ICON):
                    print("Fox Wins!")
                    running = False
                elif self.board.is_win(HOUND_ICON):
                    print("Hounds Win!")
                    running = False

                if event.type == pyg.MOUSEBUTTONDOWN and pyg.mouse.get_pressed()[0]: #Register Left click
                    if self.current_turn == self.player_1:
                        x, y = pyg.mouse.get_pos()
                        col, row = x//100, y//100 #change 100s to known constant
                        if self.player_1 == FOX_ICON:
                            self.board.move(col=col, row=row, player=self.player_1) #player should equal player 1
                            self.current_turn = self.player_2
                            self.draw_board()
                        elif self.player_1 == HOUND_ICON:
                            if not self.hound_selected:
                                self.hound_selected = [col, row]
                            else:
                                self.board.move(col=col, row=row, player=self.player_1, hound_pos=self.hound_selected) #player should equal player 1
                                self.current_turn = self.player_2
                                self.draw_board()
                                self.hound_selected = None
                    else:
                        print("Its not your turn!")
                
            if self.board.is_win(FOX_ICON):
                print("Fox Wins!")
                running = False
            elif self.board.is_win(HOUND_ICON):
                print("Hounds Win!")
                running = False

            elif self.current_turn == self.player_2:
                print("AI is moving...")
                self.ai_move()
                self.current_turn = self.player_1
                self.draw_board()

            self.win.blit(self.buffer, (0,0))
            pyg.display.update()
            self.clock.tick(self.fps)

        print("Thanks for playing")
                



if __name__ == "__main__":
    print('running fox and hounds...')
    pyg.init()
    app = App()
    app.run()