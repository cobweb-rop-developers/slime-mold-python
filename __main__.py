"""This specially named module makes the package runnable."""

import constants
from model import SlimeMoldModel
from ViewController import ViewController


def mult(num):
    return constants.CELL_RADIUS * num


def main() -> None:
    """Entrypoint of simulation."""
    montreal = (mult(16), mult(-8), 500)
    quebec = (mult(19), mult(-5), 500)
    sj = (mult(23), mult(-5), 500)
    halifax = (mult(26), mult(-6), 500)
    sydney = (mult(29), mult(-2), 100)
    sudbery = (mult(2), mult(-10), 700)
    toronto = (mult(6), mult(-14), 700)
    tbay = (mult(-7), mult(-8), 700)
    winnipeg = (mult(-17), mult(-6), 700)
    regina = (mult(-28), mult(-3), 500)
    calgary = (mult(-35), mult(1), 500)
    saskatoon = (mult(-26), mult(0), 500)
    vancouver = (mult(-42), mult(0), 500)
    edmonton = (mult(-33), mult(3), 50)
    pg = (mult(-38), mult(7), 50)
    pr = (mult(-41), mult(11), 50)
    fn = (mult(-36), mult(13), 50)
    wl = (mult(-37), mult(16), 20)
    whitehorse = (mult(-39), mult(19), 20)
    dawson = (mult(-38), mult(23), 20)
    hr = (mult(-32), mult(13), 20)
    yellowknife = (mult(-28), mult(15), 20)

    food_list = [montreal, quebec, sj, halifax, sydney, sudbery, toronto,
                 tbay, winnipeg, regina, calgary, saskatoon, vancouver,
                 edmonton, pg, pr, fn, wl, whitehorse, dawson, hr, yellowknife]
    # food_list = [(mult(6), mult(1), 1000),
    #              (mult(10), mult(6), 500)]
    starting_loc = (mult(10), mult(-10))
    starting_energy = 2100
    exploration = 0.09
    model = SlimeMoldModel(starting_loc, starting_energy, food_list,
                           exploration)  # Model of simulation
    vc = ViewController(model)  # updates the model
    vc.start_simulation()


if __name__ == "__main__":
    main()
