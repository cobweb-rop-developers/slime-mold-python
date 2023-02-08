"""The model classes maintain the state and logic of a slime mold."""

from __future__ import annotations
from hashlib import new
from typing import List
from random import random
from xmlrpc.client import Boolean
from constants import CELL_RADIUS, ENERGY_DECREASE
import random

__author__ = "Yijia Zhou"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def same(self, other):
        return self.x == other.x and self.y == other.y


class Food:
    location: Point
    energy: int

    def __init__(self, location: Point, energy: int):
        self.location = location
        self.energy = energy


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    total_energy: int
    children: List[Cell]
    parent: Cell
    found_food: Boolean
    exploration: float
    max_children: int

    def __init__(self, location: Point, direction: Point, energy: int, exploration: float):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction
        self.total_energy = energy
        self.children = []
        self.found_food = False
        self.parent = None
        self.exploration = exploration

    def update_on_tick(self) -> None:
        # check if child has found food
        if len(self.children) > 0:
            for child in self.children:
                if child.found_food:
                    self.found_food = True

        # decrements the energy level of a given cell
        if not self.found_food:
            self.total_energy -= ENERGY_DECREASE
            if self.total_energy < 0:
                # cell death
                return False
        return True

    def has_found_food(self, food_list):
        for food in food_list:
            if self.location.same(food.location):
                self.found_food = True
                return True
        return False

    def create_child(self):
        return []

    def set_parent(self, other):
        self.parent = other

    def color(self) -> str:
        """Return the color representation of a cell."""
        return "gold"


class DiagonalCell(Cell):

    def __init__(self, location: Point, direction: Point, energy: int, exploration: float):
        Cell.__init__(self, location, direction, energy, exploration)
        self.max_children = 3
        self.children_dirs = [self.direction, Point(0, self.direction.y),
                              Point(self.direction.x, 0)]

    def create_child(self):
        # diagonal cell creates 3 cell children
        new_children = []
        created_dirs = []

        for dir in self.children_dirs:
            create_child = float(random.randint(0, 100)) / 100
            if create_child < self.exploration:
                new_loc = self.location.add(dir)

                if dir.x == 0:
                    new_cell = StraightCell(new_loc, dir, self.total_energy - 10, self.exploration)
                    created_dirs.append(dir)
                elif dir.y == 0:
                    new_cell = StraightCell(new_loc, dir, self.total_energy - 10, self.exploration)
                    created_dirs.append(dir)
                else:
                    new_cell = DiagonalCell(new_loc, dir, self.total_energy - 10, self.exploration)
                    created_dirs.append(dir)

                new_cell.set_parent(self)
                self.children.append(new_cell)
                new_children.append(new_cell)

        for dir in created_dirs:
            self.children_dirs.remove(dir)

        self.max_children -= len(new_children)
        return new_children


class StraightCell(Cell):

    def __init__(self, location: Point, direction: Point, energy: int, exploration: float):
        Cell.__init__(self, location, direction, energy, exploration)
        self.max_children = 1

    def create_child(self):
        # a straight cell will always make a straight cell
        new_children = []
        create_child = float(random.randint(0, 100)) / 100
        if create_child < self.exploration:
            new_loc = self.location.add(self.direction)
            new_cell = StraightCell(new_loc, self.direction, self.total_energy - 10,
                                    self.exploration)
            new_cell.set_parent(self)
            self.children.append(new_cell)
            new_children.append(new_cell)

        self.max_children -= len(new_children)
        return new_children


class SlimeMoldCenter:
    fruiting_body: List[Cell]
    leading_edge: List[Cell]
    population: List[Cell]

    def __init__(self, starting_loc, initial_energy, exploration):
        """Initialize the cells with random locations and directions."""
        # initialize fruiting body center
        self.population = []
        self.fruiting_body = []
        dirs = [(0, 0), (CELL_RADIUS / 2, 0), (0, CELL_RADIUS / 2),
                (CELL_RADIUS / 2, CELL_RADIUS / 2),
                (-CELL_RADIUS / 2, 0), (0, -CELL_RADIUS / 2), (-CELL_RADIUS / 2, CELL_RADIUS / 2),
                (CELL_RADIUS / 2, -CELL_RADIUS / 2), (-CELL_RADIUS / 2, -CELL_RADIUS / 2)]

        for dir in dirs:
            new_loc = Point(starting_loc[0] + dir[0], starting_loc[1] + dir[1])
            if dir == (0, 0):
                new_cell = Cell(new_loc, Point(dir[0], dir[1]), initial_energy, exploration)
                new_cell.max_children = 0
            elif new_loc.x == 0 or new_loc.y == 0:
                new_cell = StraightCell(new_loc, Point(dir[0], dir[1]), initial_energy, exploration)
            else:
                new_cell = DiagonalCell(new_loc, Point(dir[0], dir[1]), initial_energy, exploration)

            self.fruiting_body.append(new_cell)
            self.population.append(new_cell)

        self.leading_edge = self.fruiting_body[:]

        # initialize board
        self.board = []
        for cell in self.population:
            self.board.append((cell.location.x, cell.location.y))

    def die(self, cell):
        # remove cell from population
        self.population.remove(cell)
        if cell in self.leading_edge:
            self.leading_edge.remove(cell)

    def update_on_tick(self, food_list):
        # update each cell in population
        for cell in self.population:
            alive = cell.update_on_tick()
            if not alive and not cell in self.fruiting_body:
                self.die(cell)

        # create new children
        new_leading_edge = []
        new_cell_loc = None
        for cell in self.leading_edge:
            # check if cell has found food
            if not cell.has_found_food(food_list):
                new_children = cell.create_child()
                for child in new_children:
                    if not (child.location.x, child.location.y) in self.board:
                        self.population.append(child)
                        new_leading_edge.append(child)
                if cell.max_children > 0:
                    new_leading_edge.append(cell)
            else:
                # we have found food, need to create a new center
                new_cell_loc = cell.location

                # now we decrease the exploration not in that direction

        self.leading_edge = new_leading_edge[:]
        return new_cell_loc


class SlimeMoldModel:
    """The state of the simulation."""

    slime_mold_centers = []
    slime_mold_centers_loc = []
    food = []
    time: int = 0

    def __init__(self, starting_loc, initial_energy, food_list, exploration):
        """Initialize the cells with random locations and directions."""
        # initialize fruiting body center
        new_center = SlimeMoldCenter(starting_loc, initial_energy, exploration)
        self.slime_mold_centers = [new_center]
        self.slime_mold_centers_loc = [starting_loc]

        self.food = []
        for food in food_list:
            food_loc = Point(food[0], food[1])
            self.food.append(Food(food_loc, food[2]))

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1

        # update each slime mold center
        new_centers = []
        for center in self.slime_mold_centers:
            result = center.update_on_tick(self.food)

            if not result is None:
                # create a new slime mold center
                new_loc = (result.x, result.y)
                if new_loc not in self.slime_mold_centers_loc:
                    food_energy = self.find_food_energy(new_loc)
                    energy = center.fruiting_body[0].total_energy
                    exploration = center.fruiting_body[0].exploration
                    new_energy = self.find_next_energy(energy, food_energy)
                    new_exploration = self.find_next_exploration(exploration, food_energy)

                    new_center = SlimeMoldCenter(new_loc, new_energy, new_exploration)
                    new_centers.append(new_center)
                    self.slime_mold_centers_loc.append(new_loc)

        # add new centers into slime_mold_centers
        for center in new_centers:
            self.slime_mold_centers.append(center)

    # define equations that determine the next value of whatever
    def find_food_energy(self, location):
        for food in self.food:
            food_loc = (food.location.x, food.location.y)
            if food_loc == location:
                food_energy = food.energy

        return food_energy

    def find_next_energy(self, cur_energy, food_energy):
        new_energy = (cur_energy + food_energy) // 2
        return new_energy

    def find_next_exploration(self, cur_exploration, food_energy):
        # the more energy a food has, the more exploratory the new slime mold center will be
        print(float(food_energy) / 10000)
        return cur_exploration + float(food_energy) / 10000

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""

        # happens when all food locations have been found
        return False
