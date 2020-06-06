assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a  for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
#Support for diagonal constraints
diag1 = [[rows[i]+cols[i] for i in range(len(rows))]]
diag2 = [[rows[i]+cols[8-i] for i in range(len(rows))]]

unitlist = row_units + column_units + square_units + diag1 + diag2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    #Find all instances of naked twins
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    # Collect boxes that have the same elements
    naked_twins = [[box1,box2] for box1 in potential_twins for box2 in peers[box1] if values[box1]==values[box2] ]

    # Get the intersection of peers for the set of twins
    for twins in naked_twins:
        box1 = twins[0]
        box2 = twins[1]
        peers_int = list(set(peers[box1]).intersection(peers[box2]))
        
    # Eliminate the naked twins as possibilities for their peers
        for peer in peers_int:
            if peer not in twins:
                for d in values[box1]:
                    values = assign_value(values, peer, values[peer].replace(d,''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    
    assert len(grid) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Eliminate options from peers if a value has been confirmed
    Args:
        values(dict): The soduku in dictionary form
    Returns:
        The updated values(dict): The soduku in dictionary form - With options reduced by elimination
    """
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                values = assign_value(values, peer, values[peer].replace(values[box], ''))
    
    return values

def only_choice(values):
    """
    Select a value based on it being the only option in a peer set
    Args:
        values(dict): The soduku in dictionary form
    Returns:
        The updated values(dict): The soduku in dictionary form - With options selected based on being the only possible value
    """
    all_digits = '123456789'
    for unit in unitlist:
        dplaces = []
        for d in all_digits:
            dplaces = [box for box in unit if d in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], d)
        
    return values

def reduce_puzzle(values):
    """
    Implements the soduku strategies in attempt to reduce or solve the grid as much as possible until the strategies can no longer solve
    Arg:
        values(dict): The soduku in dictionary form
    Returns:
        The updated values(dict) which has been progressed. False if it has eliminated all options for a box
    """
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)
        
        # Use the Naked Twins strategy
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Reduces the puzzle before using search to evaluate possible solutions
    Arg:
        values(dict): The soduku in dictionary form
    Returns:
        The updated values(dict) which has been progressed. False if it has failed
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False # failed
    if all(len(values[s]) == 1 for s in boxes):
        return values #Success
    
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_soduku = values.copy()
        new_soduku[s] = value
        attempt = search(new_soduku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
