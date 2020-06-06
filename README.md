# Sudoku Solver

## Naked Twins Strategy

   The naked twins strategy is based on finding 2 boxes in the same peer set which only have 2 values and have the same values. If this
   is the case then the values in the 'twin' boxes can be eliminated from the other boxes in the peer set as possible values since they can only
   exist in those 2 boxes. To do this, we need to perform the following steps:

   1. Identify naked twin candidates in a peer set
   2. Get the intersection of the peers for naked twin boxes
   3. Eliminate the values contained in the naked twin boxes from the peers as options

## Diagonal Sudoku (using constraint propagation to solve the diagonal sudoku problem)

   The rules of soduku are such that only one of each digit from 1-9 can exist in a row, column or square (3x3 section). To solve for these units
   the peer dictionaries are used to support the strategies to eliminate and select values for each box. We would simply need to add the diagonal
   boxes as peer sets to enforce the constraint. Once these have been added as peer sets we can use the same strategies to constrain the two
   diagonal sets of boxes to only have one of each value from 1-9 for each set.

## Installation and Setup

   The project configuration in this project is known to work on MacOS but has not be tried on other operating systems.

   To install and setup this project:

   * Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://docs.anaconda.com/anaconda/install/)
   * Create the environment by running `conda env create --file environment.yml`

### Grid Input

The initial grid input is provided in `solution.py` with the `diag_sudoku_grid` variable. Each position in the grid must be represented in the string starting with the top left square as the first character. If the square is empty then the character should be a ".". The provided default example is:

`'2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'`

### Optional: Pygame

Optionally, you can also install pygame if you want to see the visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Provides code for solving the Soduku using the Naked Twins and the Diagonal Soduku strategies
* `solution_test.py` - Tests for the solution solution.
* `PySudoku.py` - This is code for visualizing the solution.
* `visualize.py` -his is code for visualizing your solution.

## Run and Test

To run the visualization: `python solution.py`

To run the tests: `python solution_test.py`
