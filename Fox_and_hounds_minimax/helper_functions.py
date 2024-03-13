from copy import deepcopy


def simulate(board_obj, row, col, player, hound_pos=[]):
    """
    simulate() returns copy of board with move enacted if valid

    board_obj: board object
    row: row of move
    col: column of move
    player: (FOX_ICON or HOUND_ICON)
    hound_pos: provide position of hound (col, row) if player is HOUND_ICON
    """


    copy = deepcopy(board_obj)
    copy.move(row, col, player, hound_pos)
    return copy


