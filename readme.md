
# Introduction
This code represents a simulation of slime mold behavior. The simulation models individual cells and food sources and tracks the movement and growth of the cells over time. The main module of the simulation is the main.py file, which sets up the initial conditions and starts the simulation.


# Constants
The constants.py file contains the constants used throughout the simulation. These include the dimensions of the simulation bounds, the radius of each cell, and the energy decrease per tick for each cell.

# Model
The model.py file contains the classes that maintain the state and logic of the simulation.

# Point
The Point class represents a 2-dimensional cartesian coordinate point. It has x and y attributes, and can be used to add two points together to create a new point.

# Food
The Food class represents a food source in the simulation. It has a location attribute, which is a Point object, and an energy attribute.

# Cell
The Cell class represents an individual cell in the simulation. It has a location attribute, which is a Point object, a direction attribute, which is also a Point object, and a total_energy attribute. The Cell class also has a children attribute, which is a list of Cell objects representing the cells produced by the parent cell, and a parent attribute, which is a Cell object representing the parent of the cell. The Cell class also has a found_food attribute, which is a boolean indicating whether the cell has found food, and an exploration attribute, which is a float representing the likelihood of the cell producing offspring.

# DiagonalCell
The DiagonalCell class extends the Cell class and represents a diagonal cell in the simulation. It has a max_children attribute of 3, representing the maximum number of children it can produce, and a children_dirs attribute, which is a list of Point objects representing the possible directions the cell can produce children in.

# StraightCell
The StraightCell class extends the Cell class and represents a straight cell in the simulation. It has a max_children attribute of 1, representing the maximum number of children it can produce.

# SlimeMoldCenter
The SlimeMoldCenter class represents a center of a slime mold in the simulation. It has fruiting_body and leading_edge attributes, which are lists of Cell objects representing the cells in the fruiting body and leading edge of the slime mold, respectively, and a population attribute, which is a list of all Cell objects associated with the slime mold center. The SlimeMoldCenter class also has a board attribute, which is a list of tuples representing the locations of all cells in the simulation.

# SlimeMoldModel
The SlimeMoldModel class represents the state of the simulation. It has slime_mold_centers and slime_mold_centers_loc attributes, which are lists of SlimeMoldCenter objects and their locations, respectively, a food attribute, which is a list of Food objects representing the food sources in the simulation, and a time attribute, which is an integer representing the number of ticks that have elapsed in the simulation.
