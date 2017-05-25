assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    pass

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Added list for diagonal units
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['I1','H2','G3','F4','E5','D6','C7','B8','A9']]

#Added diagonal units to unitlist
unitlist = row_units + column_units + square_units + diagonal_units
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
    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    #Initialise flag and lists
    flag = 1 #flag to decide whether to search for naked twins or not
    my_list_row = []
    my_list_col = []
    my_list_sq = []
    my_list_diagonal = []
    
    #Start search for naked twins
    while flag:        
        flag = 0
        #Search for naked twins in row units
        for i in range(9):  #scan through all the row units
            for index, box in enumerate(row_units[i]):
                if len(values[box]) == 2:
                    if index == 8:
                        #Prevent out of range error if box is last in the unit
                        continue
                    else:
                        for j in range(index+1,9):
                            if values[box] == values[row_units[i][j]]:
                                if box in my_list_row:
                                    break
                                else:
                                    #Naked twins were found.
                                    #Add boxes to the list of already tested naked twins
                                    my_list_row.append(box)
                                    my_list_row.append(row_units[i][j])
                                    for k in range(9):
                                        if (k != index and k != j) and len(values[row_units[i][k]]) > 1:
                                            flag = 1    #Set search continue flag
                                            for digit in values[box]:   #Remove digits in the naked twins from other box in the unit
                                                values[row_units[i][k]] = values[row_units[i][k]].replace(digit,"")
                                    break
        #Search for naked twins in column units
        for i in range(9):  #scan through all the column units
            for index, box in enumerate(column_units[i]):
                if len(values[box]) == 2:
                    if index == 8:
                        #Prevent out of range error if box is last in the unit
                        continue
                    else:
                        for j in range(index+1,9):
                            if values[box] == values[column_units[i][j]]:
                                if box in my_list_col:
                                    break
                                else:
                                    #Naked twins were found.
                                    #Add boxes to the list of already tested naked twins
                                    my_list_col.append(box)
                                    my_list_col.append(column_units[i][j])
                                    for k in range(9):
                                        if (k != index and k != j) and len(values[column_units[i][k]]) > 1:
                                            flag = 1    #Set search continue flag
                                            for digit in values[box]:   #Remove digits in the naked twins from other box in the unit
                                                values[column_units[i][k]] = values[column_units[i][k]].replace(digit,"")
                                    break
        #Search for naked twins in square units
        for i in range(9):  #scan through all the square units
            for index, box in enumerate(square_units[i]):
                if len(values[box]) == 2:
                    if index == 8:
                        #Prevent out of range error if box is last in the unit
                        continue
                    else:
                        for j in range(index+1,9):
                            if values[box] == values[square_units[i][j]]:
                                if box in my_list_sq:
                                    break
                                else:
                                    #Naked twins were found. 
                                    #Add boxes to the list of already tested naked twins
                                    my_list_sq.append(box)
                                    my_list_sq.append(square_units[i][j])
                                    for k in range(9):
                                        if (k != index and k != j) and len(values[square_units[i][k]]) > 1:
                                            flag = 1    #Set search continue flag
                                            for digit in values[box]:   #Remove digits in the naked twins from other box in the unit
                                                values[square_units[i][k]] = values[square_units[i][k]].replace(digit,"")
                                    break
        #Search for naked twins in diagonal units
        for i in range(2):  #scan through all the diagonal units
            for index, box in enumerate(diagonal_units[i]):
                if len(values[box]) == 2:
                    if index == 8:
                        #Prevent out of range error if box is last in the unit
                        continue
                    else:
                        for j in range(index+1,9):
                            if values[box] == values[diagonal_units[i][j]]:
                                if box in my_list_sq:
                                    break
                                else:
                                    #Naked twins were found.
                                    #Add boxes to the list of already tested naked twins
                                    my_list_diagonal.append(box)
                                    my_list_diagonal.append(diagonal_units[i][j])
                                    for k in range(9):
                                        if (k != index and k != j) and len(values[diagonal_units[i][k]]) > 1:
                                            flag = 1    #Set search continue flag
                                            for digit in values[box]:   #Remove digits in the naked twins from other box in the unit
                                                values[diagonal_units[i][k]] = values[diagonal_units[i][k]].replace(digit,"")
                                    break
    else:
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
    grid_dict = {}
    index = 0
    #Scan through the grid row by row and replace all '.' by '123456789'
    for i in [0, 9, 18, 27, 36, 45, 54, 63, 72]:
        for j in range(9):
            if grid[i+j] == '.':
                grid_dict[row_units[index][j]] = '123456789'                
            else:
                grid_dict[row_units[index][j]] = grid[i+j]
        else:
            index += 1
    else:
        return grid_dict
    pass

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
    pass

def eliminate(values):
    my_list = []
    #Scan through every box and store all the solved boxes in my_list
    for box in boxes:
        if len(values[box]) == 1:
            my_list.append(box)
    #Scan through my_list and eliminates its values from all its peers
    for s_box in my_list:
        num2elim = values[s_box]    #Value to be eliminated
        for p_vals in peers[s_box]:
            if num2elim in values[p_vals]:
                #Eliminate num2elim from peer box if it's present in possible solution
                values[p_vals] = values[p_vals].replace(num2elim,'')
    else:
        return values
    pass

def only_choice(values):
    my_list = []
    #Scan through every units(row, column, square, diagonal)
    for unit in unitlist:
        #print (unit)
        for digit in '123456789':   #Check every digit 1-9 for only choice possiblility in each unit
            for box in unit:    #Store all box in which the digit is present
                if digit in values[box]:
                    my_list.append(box)
            else:
                #print("Length of list"+len(my_list))
                if len(my_list) == 1:   #If number of boxes of a digit is 1, then that's the only choice
                    values[my_list[0]] = digit
                my_list[:] = []
    else:
        return values
    pass

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search(values):
    #Check if there is an error
    res = reduce_puzzle(values)
    if res == False:
        return False
    
    #Check whether the sudoku has all single digit in it's boxes. If yes then 
    #considered solved
    res = values
    if all(len(values[s])==1 for s in boxes):
        return values
    
    #Find the box with the least search possibilities
    search_box = find_search_box(values)
    
    #Try each digit in the search box as a solution and solve sudoku. If it fails 
    #try the next digit and repeat till solution is found
    for digit in values[search_box]:
        new_sudoku = values.copy()
        new_sudoku[search_box] = digit
        attempt = search(new_sudoku)
        if  attempt:
            return attempt
    pass

def find_search_box(values):
    """
    A function to find the box to be used to start the search method to solve 
    the sudoku.
    """
    flag = 0
    search_box = ''
    for box in boxes: #Scan through all boxes
        if len(values[box]) > 1:    #Search should be unsolved            
            if len(values[box]) == 2:   #If box has only two possible solutions, pick that box and return result
                search_box = box
                return search_box
                break
            if flag == 0: #If it is the first box, the store in variable
                search_box = box
                flag = 1
            elif len(values[search_box]) > len(values[box]):    #Check whether length of value in variable is greater, Store the shorter one
                search_box = box
    else:
        return search_box

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
    values = reduce_puzzle(values)
    if values != False:
        values = search(values)
        if values != False:
            return values
        else:
            print ('No solution. Returned False after search')
    else:
        print ('No solution. Returned False in reduced puzzle.')

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
