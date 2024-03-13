from constants import FOX_ICON, HOUND_ICON, EMPTY_ICON, DEFAULT_FOX_POS, LAST_ROW, ROWS, COLS
from copy import deepcopy


class Board:

    def __init__(self) -> None:
        self.__grid = []

    def getBoard(self):
        return self.__grid
    def setBoard(self, grid):
        self.__grid = grid
    
    def create_start_board(self):

        """
        create_start_board() assigns grid from Board object the starter grid with initial player positions.

        Parameters: None
        
        """


        grid = self.getBoard()
        for _ in range(ROWS):
            grid.append([EMPTY_ICON] * COLS)
        grid[0] = [EMPTY_ICON] + [HOUND_ICON] + [EMPTY_ICON] + [HOUND_ICON] + [EMPTY_ICON] + [HOUND_ICON] + [EMPTY_ICON] + [HOUND_ICON]
        grid[LAST_ROW][DEFAULT_FOX_POS] = FOX_ICON 

    def move(self, row, col, player, hound_pos=[]):

        """
        move() takes row and col arguments and validates the move based upon the grid from Board object. Then, move() updates position of player on the grid.

        Parameters:

        row: the row of the move
        col: the col of the move
        player: the player moving
        hound_pos: if player is hound, provide row and col of specific hound ([col , row])
        
        """

        grid = self.getBoard()
        new_grid = deepcopy(grid)

        if player == FOX_ICON:
            if self.is_valid(row, col, FOX_ICON):
                F_LOC = self.find_player(FOX_ICON)
                F_COL, F_ROW = F_LOC[0][0], F_LOC[0][1]
                new_grid[row][col] = FOX_ICON
                new_grid[F_ROW][F_COL] = EMPTY_ICON
                

        elif player == HOUND_ICON and hound_pos != []: #NEED USER TO HIGHLIGHT HOUND THEY WANT TO MOVE
            if self.is_valid(row, col, HOUND_ICON):
                H_LOCS = self.find_player(HOUND_ICON)
                for HOUND in H_LOCS:
                    if hound_pos == HOUND:
                        new_grid[row][col] = HOUND_ICON
                        new_grid[hound_pos[1]][hound_pos[0]] = EMPTY_ICON

        self.setBoard(new_grid)

    def find_player(self, player):
        """
        find_player() returns the row and column of the given player

        Parameters:
        player: find either fox or all the hounds (FOX_ICON or HOUND_ICON)
        
        """
        grid = self.getBoard()
        PLAYER_LOC = []

        if player == FOX_ICON:

            for index, row in enumerate(grid):
                if row.count(FOX_ICON) == 1:
                    PLAYER_LOC.append([row.index(FOX_ICON), index]) #col, row

        elif player == HOUND_ICON:
            HOUND_ROW = None
            HOUND_COL = None

            for indexy, row in enumerate(grid):
                for indexx, col in enumerate(row):
                    if col == HOUND_ICON:
                        HOUND_ROW, HOUND_COL = indexy, indexx
                        PLAYER_LOC.append([HOUND_COL, HOUND_ROW])
        return PLAYER_LOC



    def is_win(self, player):
        """
        is_win() determines whether the grid from the Board object has a winning condition based upon the player given.

        Parameters:
        player: (FOX_ICON or HOUND_ICON)
        
        """


        grid = self.getBoard()

        if player == HOUND_ICON:
            if self.get_all_moves(FOX_ICON) == 0:
                return True
            else:
                HOUND_COUNT = 0
                F_LOC = self.find_player(FOX_ICON)
                F_COL, F_ROW = F_LOC[0][0], F_LOC[0][1]
                
                for i in range(-1, 2, 2):
                    if self.is_empty(F_ROW, F_COL+i) and self.is_empty(F_ROW+i, F_COL):
                        if grid[F_ROW][F_COL+i] == HOUND_ICON:
                            HOUND_COUNT +=1
                        if grid[F_ROW+i][F_COL] == HOUND_ICON:
                            HOUND_COUNT +=1
                return HOUND_COUNT == 4
        
        
        elif player == FOX_ICON:
            return grid[0].count(FOX_ICON) > 0

    def is_empty(self, row, col):
        """
        is_empty() determines whether the position from the grid is unoccupied, meaning the position has "_", and is not out of bounds

        Parameters:
        row: row of position
        col: col of position
        """




        grid = self.getBoard()
        return 0 <= row < len(grid) and 0 <= col < len(grid[row]) and grid[row][col] == EMPTY_ICON

    def is_valid(self, row, col, player):
        """
        is_valid() determines whether a position is in the list returned from get_all_moves()

        Parameters:
        row: row of move
        col: col of move
        player: player of move (FOX_ICON, HOUND_ICON)
        
        """




        if player == FOX_ICON:
            MOVES = self.get_all_moves(FOX_ICON)
            if [col, row] in MOVES:
                return True
        elif player == HOUND_ICON:
            MOVES = self.get_all_moves(HOUND_ICON)
            for move in MOVES:
                if move[0] == col and move[1] == row:
                    return True
        else:
            print("INVALID MOVE")
            return False

    def get_all_moves(self, player):
        
        """
        get_all_moves() returns all valid moves based upon player

        Parameters:
        player: (FOX_ICON or HOUND_ICON)
        NOTE: Hound players will return all moves for all hounds on grid of board object.
        """

        grid = self.getBoard()
        MOVES = []

        if player == FOX_ICON:
            F_LOC = self.find_player(FOX_ICON)
            F_COL, F_ROW = F_LOC[0][0], F_LOC[0][1]

            if F_COL is not None and F_ROW is not None: 
                for i in range(-1, 2, 2):
                    for j in range(-1, 2, 2):
                        new_row = F_ROW + i
                        new_col = F_COL + j

                 
                        if self.is_empty(new_row, new_col):
                            MOVES.append([new_col, new_row]) 

        elif player == HOUND_ICON:

            HOUND_POS = self.find_player(HOUND_ICON)
            
            if HOUND_POS:
                for hound in HOUND_POS:
                    for i in range(-1, 2, 2):
                            new_row = hound[1] + 1 #ONLY CAN LOOK FOWARD
                            new_col = hound[0] + i

                    
                            if self.is_empty(new_row, new_col):
                                MOVES.append([new_col, new_row, hound])
        return MOVES
    

    def evaluation(self):
        """
        evaluation() calculates evaluation of grid based upon certain factors:
            1.) whether fox is in the corner of grid
            2.) if hound is more moves than fox

        Parameters: None
        
        """


        hound_moves = len(self.get_all_moves(HOUND_ICON))
        fox_moves = len(self.get_all_moves(FOX_ICON))

        # Hound advantage based on move count
        move_advantage = hound_moves - fox_moves

        # Fox position (heuristic bonus for cornering the Fox)
        fox_loc = self.find_player(FOX_ICON)  # Assuming you have a function to find the Fox position
        fox_loc = fox_loc[0]
        fox_col, fox_row = fox_loc[1], fox_loc[0]
        corner_bonus = 0
        if fox_row in (0, ROWS - 1) and fox_col in (0, COLS - 1):
            corner_bonus = 3  # Higher bonus for true corners

        # Combine factors with weights (adjust weights as needed)
        return 2 * move_advantage + corner_bonus
