"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual

ECCENTRICITY = 6
BAR_SIZE = [0.6, 4]  # width, height
CAPTURE_CUE_SIZE = 0.7  # diameter of circle


def create_fixation_cross(settings, colour="#eaeaea"):
    # Determine size of fixation cross
    fixation_size = settings["deg2pix"](0.22)

    # Make fixation cross
    fixation_cross = visual.ShapeStim(
        win=settings["window"],
        vertices=(
            (0, -fixation_size),
            (0, fixation_size),
            (0, 0),
            (-fixation_size, 0),
            (fixation_size, 0),
        ),
        lineWidth=settings["deg2pix"](0.06),
        lineColor=colour,
        closeShape=False,
        units="pix",
    )

    fixation_cross.draw()


def make_one_bar(orientation, colour, position, settings):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Create bar stimulus
    bar_stimulus = visual.Rect(
        win=settings["window"],
        units="pix",
        width=settings["deg2pix"](BAR_SIZE[0]),
        height=settings["deg2pix"](BAR_SIZE[1]),
        pos=pos,
        ori=orientation,
        fillColor=colour,
    )

    return bar_stimulus


def create_stimuli_frame(left_orientation, right_orientation, colours, settings):
    create_fixation_cross(settings)
    make_one_bar(left_orientation, colours[0], "left", settings).draw()
    make_one_bar(right_orientation, colours[1], "right", settings).draw()


def create_capture_cue_frame(colour, settings):
    capture_cue = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](CAPTURE_CUE_SIZE / 2),
        pos=(0, 0),
        fillColor=colour,
    )

    capture_cue.draw()
    create_fixation_cross(settings)
