# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins strategy exploits the constraint that if in a unit there are two boxes (A and B) with the same two 
values (V1, V2) as the only possibility for them, then we can say that those values necessarily will be in those two 
boxes, since there is no other possible value for those boxes.

Consequently, this constraint can be propagated to other boxes in units that are common to A and B, because values V1
and V2 will not be possible in any other box within common units to A and B. 
 
Once this condition is applied to all the units, the changes made can uncover further changes to other boxes through 
other strategies. This is how we are using constraint propagation to solve the sudoku problem.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: The diagonal sudoku problem is a normal sudoku with two additional units formed by the two diagonals. All the 
previous techniques can be applied in the same way as before, being the only difference that now we have two more 
units to which we have to propagate the constraints.

We already had defined in the normal sudoku line, row and square units:

~~~~
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) 
                for rs in ('ABC', 'DEF', 'GHI') 
                for cs in ('123', '456', '789')]
~~~~

Now we only need to define the additional diagonal units

~~~~
diag_units = [[(rows[i] + cols[i]) for i,v in enumerate(rows)],
              [(rows[i] + cols[-1 -i]) for i,v in enumerate(rows)]]
~~~~

And add them to our list of units to apply constraint propagation:

~~~~
unitlist = row_units + col_units + square_units + diag_units
~~~~

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.