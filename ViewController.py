"""The ViewController drives the visualization of the simulation."""

from turtle import Turtle, Screen, done
from model import SlimeMoldModel
import constants
from typing import Any
from time import time_ns

NS_TO_MS: int = 1000000


class ViewController:
    """This class is responsible for controlling the simulation and visualizing it."""
    screen: Any
    pen: Turtle
    model: SlimeMoldModel

    def __init__(self, model: SlimeMoldModel):
        """Initialize the VC."""
        self.model = model
        self.screen = Screen()
        self.screen.setup(constants.VIEW_WIDTH, constants.VIEW_HEIGHT)
        self.screen.tracer(0, 0)
        self.screen.delay(0)
        self.screen.title("Slime Mold Model")
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.ht()
        self.pen.speed(0)
        self.screen.bgcolor("black")

    def start_simulation(self) -> None:
        """Call the first tick of the simulation and begin turtle gfx."""
        self.tick()
        done()

    def tick(self) -> None:
        """Update the model state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.model.tick()
        self.pen.clear()
        for center in self.model.slime_mold_centers:
            for cell in center.population:
                self.pen.penup()
                self.pen.goto(cell.location.x, cell.location.y)
                self.pen.pendown()
                self.pen.color(cell.color())
                self.pen.dot(constants.CELL_RADIUS)

        for food in self.model.food:
            self.pen.penup()
            self.pen.goto(food.location.x, food.location.y)
            self.pen.pendown()
            self.pen.color("green")
            self.pen.dot(constants.CELL_RADIUS)
        self.screen.update()

        if self.model.is_complete():
            return
        else:
            end_time = time_ns() // NS_TO_MS
            next_tick = 30 - (end_time - start_time)
            if next_tick < 0:
                next_tick = 0
            end_time = time_ns() // NS_TO_MS
            timediff = (end_time - start_time // NS_TO_MS)            
            print("FRAME RATE:" +  str(1000 / timediff))
            self.screen.ontimer(self.tick, next_tick)
