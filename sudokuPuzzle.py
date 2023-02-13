# This program will solve a sudoku puzzle using basic solving methods as well as guess and check methods
# I'd like to implement some sort of "decision tree" (not the model) perhaps I make a tree comprised of moves so I can backtrack if guess and check fails

# Will create fresh notes, will be used upon first attempt to solve puzzle and all subsequent times it is necessary to edit notes, TODO make more optimal not correction method
# The structure of the returned dictionary will be {(int x ,int y) : [int]} where the tuple will store the x,y coords and the list will hold the values that could be at that location
def createNotes(puzzle: list) -> dict:
    notes = {}
    for x in range(9):
        for y in range(9):
            if puzzle[x][y] == 0:
                notes[(x,y)] = singleSquareNote(x, y, puzzle)
    return notes

#Generates the notes for a specific square, used in above function and also when pivoting on guess and check
def singleSquareNote(x, y: int, puzzle: list) -> list:
    potential = [1,2,3,4,5,6,7,8,9]  
    for trav in range(9):

        col = puzzle[x][trav]
        if col in potential:
            potential.remove(col)

        row = puzzle[trav][y]
        if row in potential:
            potential.remove(row)

        sqr = puzzle[3*(x//3)+(trav//3)][3*(y//3)+(trav%3)]
        if sqr in potential:
            potential.remove(sqr)
                
    return potential

# Checks puzzle to see if it is valid and solved, ie the puzzle follows the rule of sudoku, a solved puzzle will output the following: True, 1
def isValidPuzzle(puzzle: list) -> (bool, int):
    rows = [[],[],[],[],[],[],[],[],[]]
    cols = [[],[],[],[],[],[],[],[],[]]
    squares = [[],[],[],[],[],[],[],[],[]]
    val = 0
    for x in range(9): # Chose to use 9 so it doesn't have to calculate the length everytime, the puzzles aren't dynamic size so it's fair to assume 9 x 9
        for y in range(9):
            num = puzzle[x][y]

            if num == 0:
                val += 1
                pass
            elif num in rows[x] or num in cols[y] or num in squares[3*(x//3) + y//3]:
                return False, val

            rows[x].append(num)
            cols[y].append(num)
            squares[3*(x//3) + y//3].append(num)

    return True, val

def printHelperV1(matrix: list): #https://stackoverflow.com/questions/13214809/pretty-print-2d-list
    print("\n")
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '   '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n''\n'.join(table))

# Function that utilizes guess and check method to solve a sudoku puzzle.
# Currently uses brute strength to solve, I do wonder if there is a possibility to make this work in a more elegant way, ie solve it in the same way a person solves such a puzzle
def solve(puzzle: list):
    notes = createNotes(puzzle)
    #print(notes)

    # Decisions will store tuples of data that represents filling in a specific sudoku square in the following form: (int nav, int val, [int]) 
    # where the x,y represents the location, the value represents the value used and the integer list holds other potential values, it's empty if there are none
    decisions = []

    # nav variable will be used to traverse locations when attempting to solve and will also determine the threshold for guess and check measures
    nav = 0
    # This loop will run until broken out of by solve condition, general assumption that these puzzles are solvable
    while True:
        x, y = (nav % 81) // 9, (nav % 81) % 9
        # Thought process below is that it will go through all 81 elements and check if there is a single number that must go there, then guess and check for two, then three, and so on.
        if puzzle[x][y] == 0 and len(notes[(x,y)]) <= (nav // 81) + 1: 
            values = notes[(x,y)]
            puzzle[x][y] = values[0]
            decisions.append((nav, values[0], values[1:]))
            nav = 0
        else:
            nav += 1

        # This section will check to see if the puzzle is valid thus far (no repeats in row, col, or 3x3)
        valid, squares = isValidPuzzle(puzzle) 
        if not valid:
            while True:
                if len(decisions) < 10:
                    print(decisions)
                # print(len(decisions))
                xR, yR = (decisions[-1][0] % 81) // 9, (decisions[-1][0] % 81) % 9
                if len(decisions[-1][2]) == 0:
                    # Resetting moves based on an incorrect guess
                    puzzle[xR][yR] = 0
                    decisions.pop()

                else:
                    # Changing incorrect guess to other options for square
                    puzzle[xR][yR] = decisions[len(decisions)-1][2][0]
                    decisions[-1] = (decisions[-1][0], decisions[-1][2][0], decisions[-1][2][1:])
                    nav = decisions[-1][1]+1
                    break
            # Only want to hard reset the notes if the puzzle is invalid and we have to retrace back to most recent guess
            createNotes(puzzle)

        # Case in which the puzzle is fully solved, exit out of main solving loop
        elif valid and squares == 0:
            print("Solved!")
            break


def main():
    puzzle1 = [
    [5,1,9,0,0,0,4,3,0],
    [7,2,4,9,0,0,0,0,0],
    [0,0,0,2,5,4,9,0,0],
    [1,7,0,0,4,0,2,0,6],
    [0,0,0,0,9,0,0,0,3],
    [0,0,3,0,0,6,0,8,0],
    [0,0,1,4,7,0,0,6,0],
    [0,0,0,5,0,8,1,2,0],
    [0,9,0,0,6,0,3,0,4]]

    puzzle2 = [
    [6,8,0,4,7,0,0,0,0],
    [7,3,4,0,6,2,5,0,0],
    [2,0,0,5,0,8,7,0,4],
    [0,0,0,2,5,0,0,0,0],
    [0,0,0,0,8,0,0,1,0],
    [5,6,0,9,1,3,0,0,7],
    [0,0,1,7,2,0,3,0,0],
    [9,2,0,0,4,0,8,0,1],
    [0,7,0,0,0,1,0,5,6]]

    hardPuzzle = [
    [8,0,0,0,0,0,0,7,0],
    [0,0,6,0,1,0,0,5,3],
    [0,4,0,6,0,0,0,0,0],
    [0,0,0,0,8,0,4,0,0],
    [0,0,3,0,0,0,7,0,0],
    [0,2,0,0,0,5,0,3,8],
    [0,0,0,0,0,0,8,0,0],
    [0,0,4,0,5,0,0,6,1],
    [9,0,0,0,0,2,0,0,0]]

    printHelperV1(hardPuzzle)
    solve(hardPuzzle)
    printHelperV1(hardPuzzle)


main()

