# 8queens.py
#
#   Solve the eight queens puzzzle as described here: https://en.wikipedia.org/wiki/Eight_queens_puzzle
#     - No AI or web search help 
#     - Except... web searches for:
#       o  point-slope line equation 
#       o  shape rotation      
#       o  handfull of python-specific questions (i.e., set() syntax)
#
#   Run with:
#     $ python -u 8queens.py | tee out.log
#
#   See log.out in repo for results
#     - 12 fundamental solutions are slightly different than those shown on Wikipedia page
#     - Likely a difference in the order of reduction operations
#
#   Runtime: 
#     ~25 minutes
#
#   Optimization ideas:
#     - Careful look at code & refactoring with speed-up in mind
#     - Use threading to run multiple solution trees across multiple cores 
#     - Wikipedia page suggests other (non-obvious) optimizations
#
import time
import sys

# Run parameters
#
queen_count = 8
board_size = (8, 8)
X = 0
Y = 1


# Globals
queens_history = []


# init_queens()
#   Create an "empty" queens list filled with (None,None) (x,y) tuples 
#
def init_queens(queens):
    queens.clear()
    for _ in range(queen_count):
        queens.append((None,None))

# find_queens()
#   Recursively find queens at a given level (up to queen_count)
#
def find_queens(queens, level):
    for x in range(board_size[X]):  
        for y in range(board_size[Y]):
            # Test each candidate at this level
            if (not test_candidate(queens, (x,y))):
                new_queens = queens.copy()
                add_queen(new_queens, (x,y), level)
                if level == queen_count - 1:
                    # This is the final level, so success
                    # Check that this is a unique set
                    if is_unique(new_queens):
                        print(f"Found queens: {new_queens}")
                else:
                    # Advance to the next level
                    find_queens(new_queens, level + 1)


# test_candidate()
#   Tests if candidate conflicts with current queen state 
#
#   queens = ordered list of (x,y) coordinate tuples - sequence of already-placed queens
#   candidate = (x,y) tuple - candidate to test
#
#   return 0: No conflict
#          1: Conflict
#
def test_candidate(queens, candidate):

    # Pull candidate x,y coordinates
    (x,y) = candidate 

    # Check for existing queen in candidate position
    #
    if (x,y) in queens:
        # print(f"Another queen found already at ({x},{y})")
        return 1

    # Check vertical
    for x_span in range(board_size[X]): 
        if (x_span,y) in queens:
            # print(f"Another queen found vertically at ({x_span},{y})")
            return 1

    # Check horizontal
    # Check across column for queens
    for y_span in range(board_size[Y]): 
        if (x,y_span) in queens:
            # print(f"Another queen found horizontally at ({x},{y_span})")
            return 1

    # Check diagonals
    # Use point-slope line equation to check   
    #   y1 - y2 - m(x1 - x2)  | Equal means on the diagonal line
    #   Test both m = 1 and m = -1
    #   (x1,y1) | Existing queen
    #   (x2,y2) | Target coordinate
    x2 = x
    y2 = y
    for (x1,y1) in queens:
        # print(f"Testing queen at ({x1},{y1})")
        if x1 != None and y1 != None:
            if (y1 - y2) == (1 * (x1-x2)): 
                # print(f"Another queen ({x1},{y1}) found diagonally from ({x},{y} with slope = 1)")
                return 1
            if (y1 - y2) == (-1 * (x1 - x2)): 
                # print(f"Another queen ({x1},{y1}) found diagonally from ({x},{y} with slope = -1)")
                return 1
    # If here, no conflict
    return 0


# add_queen()
#   Add a queen to the queens list (next in sequence)
#
def add_queen(queens, candidate, level):
    (x,y) = candidate
    try:
        # print(f"Adding queen at ({x},{y}) level {level}")
        i = queens.index((None, None))
        queens[i] = (x,y)
    except ValueError:
        print(f"ERROR: Attempted to add_queen() to a full queens list - this shouldn't happen") 
        sys.exit(1)
       

# is_unique()
#   Compare new_queens to those discovered so far
#   Eliminates sequence repeats found in different order
#   return 0: is not unique
#          1: is unique
#
def is_unique(new_queens):
    for queen in queens_history: 
        if set(new_queens) == set(queen):
            return 0 
    queens_history.append(new_queens)
    return 1


# rotate90cw()
#   Rotate a sequence of queens by 90 degrees clockwise
#
def rotate90cw(queens):
    new_queens = []
    for (x,y) in queens:
        # Rotate queen coordinate 90 degrees clockwise
        # First, relocate point to 4-quadrant 
        # print(f"(x,y) = ({x},{y})")
        xc = x - ((board_size[X]-1) / 2)
        yc = y - ((board_size[Y]-1) / 2)
        # print(f"(xc,yc) = ({xc},{yc})")
        # Second, rotate clockwise with (xc,yc) -> (yr,-xr) 
        xr = yc
        yr = -xc
        # print(f"(xr,yr) = ({xr},{yr})")
        # Third, relocate back to 1-quadrant
        xn = xr + ((board_size[X]-1) / 2)
        yn = yr + ((board_size[Y]-1) / 2)
        # print(f"(xn,yn) = ({xn},{yn})")
        # print(f"(xn,yn) = ({int(xn)},{int(yn)})")
        # Convert back to int to enable comparison
        new_queens.append((int(xn),int(yn))) 
    # print(f"rotate90cw() in:  {queens}")
    # print(f"rotate90cw() out: {new_queens}")
    return (new_queens)


# mirror()
#   Reflect over x-axis or y-axis
#
def mirror(queens, axis):
    new_queens = []
    if axis == X:
        for (x,y) in queens:
            # Mirror queen coordinate over the x-axis
            # First, relocate y's to 4-quadrant 
            ym = y - ((board_size[Y]-1) / 2)
            # Second, mirror with (x,y) -> (x,-ym) 
            ym = -ym
            # Third, relocate back to 1-quadrant
            ym = ym + ((board_size[Y]-1) / 2)
            # Convert back to int to enable comparison
            new_queens.append((x,int(ym))) 
        # print(f"mirror() x-axis in:  {queens}")
        # print(f"mirror() x-axis out: {new_queens}")
    elif axis == Y:
        for (x,y) in queens:
            # Mirror queen coordinate over the y-axis
            # First, relocate x's to 4-quadrant 
            xm = x - ((board_size[X]-1) / 2)
            # Second, mirror with (x,y) -> (-xm,y) 
            xm = -xm
            # Third, relocate back to 1-quadrant
            xm = xm + ((board_size[X]-1) / 2)
            # Convert back to int to enable comparison
            new_queens.append((int(xm),y)) 
        # print(f"mirror() y-axis in:  {queens}")
        # print(f"mirror() y-axis out: {new_queens}")
    return (new_queens)


def main():
    print(f"{queen_count} queens on {board_size[X]} x {board_size[Y]} board ")

    # Loop through all 1st row queen locations
    # Starting on other rows will just produces duplicates
    #
    x = 0
    start_all = time.perf_counter()
    for y in range(board_size[Y]):
        start = time.perf_counter()
        queens = []
        init_queens(queens)
        print(f"Start ({x},{y})")
        add_queen(queens, (x,y), 0)
        find_queens(queens.copy(), 1)
        end = time.perf_counter()
        print(f"End   ({x},{y}) time: {int(end - start)} seconds")
    end_all = time.perf_counter()
    print(f"Total time: {int(end_all - start_all)} seconds")
    print(f"Total solutions: {len(queens_history)}")

    # Now reduce to fundamental solutions by rotating (90, 180, 270 degrees) and mirroring
    # Wikipedia page says 8x8 has 92 solutions should reduce to 12 fundamental solutions
    #
    new_queens = []
    for queens in queens_history:

        # Remove queen sequence's mirror (before rotation) for duplicates 
        # 
        new_queens.clear()
        new_queens = queens.copy()
        new_queens = mirror(new_queens, X)
        # Catch the case(s) where a mirror matches the original
        if set(new_queens) != set(queens):
            # Otherwise, remove the mirror from queens_history if found there
            for queens_orig in queens_history: 
                if set(new_queens) == set(queens_orig):
                    # print(f"Removing (mirror x-axis): {queens_orig}")
                    queens_history.remove(queens_orig)
                    break

        new_queens.clear()
        new_queens = queens.copy()
        new_queens = mirror(new_queens, Y)
        # Catch the case(s) where a mirror matches the original
        if set(new_queens) != set(queens):
            # Otherwise, remove the mirror from queens_history if found there
            for queens_orig in queens_history: 
                if set(new_queens) == set(queens_orig):
                    # print(f"Removing (mirror y-axis): {queens_orig}")
                    queens_history.remove(queens_orig)
                    break

        # Remove queen sequence's rotation or rotation's mirror from queens_history on match
        new_queens.clear()
        new_queens = queens.copy()
        for r in [90, 180, 270]:
            # Rotate 90 degrees 
            new_queens = rotate90cw(new_queens)
            # Catch the case(s) where a rotation matches the original
            if set(new_queens) != set(queens):
                # Otherwise, remove the rotation from queens_history if found there
                for queens_orig in queens_history: 
                    if set(new_queens) == set(queens_orig):
                        # print(f"Removing ({r} degrees): {queens_orig}")
                        queens_history.remove(queens_orig)
                        break

            # Mirror x-axis rotated queen sequence
            mirror_queens = new_queens.copy()
            mirror_queens = mirror(mirror_queens, X)
            # Catch the case(s) where a rotation's mirror matches the original
            if set(mirror_queens) != set(queens):
                # Otherwise, remove the rotation from queens_history if found there
                for queens_orig in queens_history: 
                    if set(mirror_queens) == set(queens_orig):
                        # print(f"Removing (mirror x-axis): {queens_orig}")
                        queens_history.remove(queens_orig)
                        break

            # Mirror y-axis rotated queen sequence
            mirror_queens = new_queens.copy()
            mirror_queens = mirror(mirror_queens, Y)
            # Catch the case(s) where a rotation's mirror matches the original
            if set(mirror_queens) != set(queens):
                # Otherwise, remove the rotation from queens_history if found there
                for queens_orig in queens_history: 
                    if set(mirror_queens) == set(queens_orig):
                        # print(f"Removing (mirror x-axis): {queens_orig}")
                        queens_history.remove(queens_orig)
                        break

    for queens in queens_history:
        print(f"Found queens (fundamental): {queens}")
    print(f"Total fundamental solutions: {len(queens_history)}")


if __name__ == "__main__":
    main()
