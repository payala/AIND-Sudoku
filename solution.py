import itertools

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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
    # Find all instances of naked twins
    # only boxes that have lenght of two can be naked twins
    candidates = sorted([(key, val) for key, val in values.items() if len(val) == 2], key=lambda x: x[1])

    vals = set([v[1] for v in candidates])
    grouped_candidates = [[val, [box[0] for box in candidates if box[1] == val]] for val in vals]

    # eliminate if item does not happen at least twice
    grouped_candidates = [c for c in grouped_candidates if len(c[1]) >= 2]

    # obtain all combinations in case more than two exist
    grouped_candidates = [[c[0], list(itertools.combinations(c[1], 2))] for c in grouped_candidates]

    # filter out all combinations that are actually not peers between them
    twins = [[twins, c[0]] for c in grouped_candidates for twins in c[1] if twins[0] in peers(twins[1])]

    # Eliminate the naked twins as possibilities for their peers
    for twin in twins:
        for box in combined_peers(twin[0][0], twin[0][1]):
            for c in twin[1]:
                assign_value(values, box, values[box].replace(c, ''))

    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [ca + cb for ca in a for cb in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
diag_units = [[(rows[i] + cols[i]) for i,v in enumerate(rows)],
              [(rows[i] + cols[-1 -i]) for i,v in enumerate(rows)]]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

unitlist = row_units + col_units + square_units + diag_units


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
    enh_grid = [cell if cell != '.' else '123456789' for cell in grid]

    state = dict(zip(boxes, enh_grid))

    return state

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    for key, val in values.items():
        if len(val) == 1:
            # key has single value
            for p in peers(key):
                # eliminate val from all peers
                assign_value(values, p, values[p].replace(val, ''))
    return values


def peers(box):
    """
    Finds all peers of a box
    :param box: source box
    :return: list of strings with keys of the peers
    """

    for s in square_units:
        if box in s:
            sq_unit = s

    p = cross(box[0], cols) + cross(rows, box[1]) + sq_unit

    p = [el for el in p if el != box]

    return p


def combined_peers(box1, box2):
    """
    Finds all boxes that are peers of both box1 and box2
    :param box1:
    :param box2:
    :return:
    """
    return [p for p in peers(box1) if p in peers(box2)]


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        idx = dict(zip('123456789', '.'*9))
        for box in unit:
            for pos_val in values[box]:
                if pos_val == '.':
                    # Nothing to say about this box
                    continue
                elif idx[pos_val] == '.':
                    # this number is still not used in the unit, write it down
                    idx[pos_val] = box
                else:
                    # the number is already in use in the unit, cannot assign
                    idx[pos_val] = 'NA'

        for key, val in idx.items():
            if val != 'NA' and val != '.':
                # only choice found
                assign_value(values, val, key)

    return values


def find_x_wings(values, row=True):
    """
    Finds X-Wings in the sudoku board. Note that X-Wings are either row x-wings or col x-wing, use row parameter
    to determine the type of x-wing to find.
    :param values: Sudoku board in dict format
    :param row: if True, row X-Wings are searched, otherwise col X-Wings.
    :return: list of X-Wings in [X-Wing value, [Col/Row 1, Col/Row 2]] format
    """
    x_wings = []
    if row:
        units = row_units
        coord_idx = 1
    else:
        units = col_units
        coord_idx = 0

    for val in '123456789':
        # For each value, search for rows that have only two possibilities for that value
        occurrences = [find_value(values, unit, val) for unit in units]

        # filter out x-wing candidates (only two occurrences of the same value)
        occurrences = [occ for occ in occurrences if occ[0] == 2]

        # if an x-wing is found, only two occurrences can exist in the same column/row. Separate row/column coord.
        occurrences = [[val,                                                 # value
                       [coord[0] for coord in occ[1]],                          # rows
                       [coord[1] for coord in occ[1]]] for occ in occurrences]  # cols

        for i, occ in enumerate(occurrences[:]):
            # Group xwings in occurence couples, discard any that don't happen in a couple

            if sum([[occ[0], occ[1+coord_idx]] == [oth[0], oth[1+coord_idx]] for oth in occurrences]) != 2:
                # Filter out any occurrence that do not form a square
                occurrences.remove(occ)
                continue
            else:
                # And group the ones that do form a square
                others = [oth for oth in occurrences if oth != occ]
                match = [oth for oth in others
                         if [oth[0], oth[1+coord_idx]] == [occ[0], occ[1+coord_idx]]][0]
                # X-wing found
                coords = [sorted(list(set(occ[1] + match[1]))),
                          sorted(list(set(occ[2] + match[2])))]
                xw = [occ[0]] + coords
                if xw not in x_wings:
                    x_wings.append(xw)

    return x_wings


def x_wing(values):
    """
    Apply the X-Wing Strategy
    :param values: Sudoku in dictionary form.
    :return: Resulting Sudoku in dictionary form after filling in only choices.
    """

    row_xwings = find_x_wings(values, row=True)
    col_xwings = find_x_wings(values, row=False)

    # Go over the found x-wings, and apply the constraint that the value can only appear on the boxes that form the
    # x-wing
    for x_w in row_xwings:
        col_peers = cross(rows, x_w[2])
        xw_pos = cross(x_w[1], x_w[2])
        col_peers = [p for p in col_peers if p not in xw_pos]
        for p in col_peers:
            assign_value(values, p, values[p].replace(x_w[0], ''))

    for x_w in col_xwings:
        row_peers = cross(x_w[1], cols)
        xw_pos = cross(x_w[1], x_w[2])
        row_peers = [p for p in row_peers if p not in xw_pos]
        for p in row_peers:
            assign_value(values, p, values[p].replace(x_w[0], ''))

    return values


def find_value(grid, boxes, value):
    """
    Counts how many times value appears in grid[boxes]
    :param grid: Sudoku in dict form
    :param boxes: array with sudoku keys
    :param value: value to count for
    :return: (n, boxes), where n is the number of occurrences and boxes is a tuple with occurrence locations
    """

    grid_vals = [(grid[b], b) for b in boxes]

    # Count the total number of occurrences
    count = sum([v[0].count(value) for v in grid_vals])

    # Make tuple with locations of the occurrences
    bxs = tuple([v[1] for v in grid_vals if value in v[0]])

    return (count, bxs)


def reduce_puzzle(values):
    stalled = False

    def sanity_check(values):
        return len([box for box in values.keys() if len(values[box]) == 0])

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        #print("{} solved values".format(solved_values_before))
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Use the X-Wing Strategy
        values = x_wing(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if sanity_check(values):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        # No solution
        # print("No solution")
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    easiest = sorted([(key, val) for key, val in values.items() if len(val) > 1], key=lambda x: len(x[1]))

    if not easiest:
        #puzzle solved
        # print("Solution found")
        return values

    options = []

    key, vals = easiest[0]
    node = "{}: {}".format(key, vals)
    # print("Possibilities: {}".format(easiest))
    # print("Creating node {}".format(node))
    for val in vals:
        next_option = dict(values)
        next_option[key] = val
        options.append(next_option)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for option in options:
        # print("Exploring in node {}".format(node))
        values = search(option)
        if values:
            # found a solution
            # print("Solution")
            return values

    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))

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
