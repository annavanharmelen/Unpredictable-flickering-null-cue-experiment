"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'unpredictable flickering null-cue experiment', see main.py.

made by Anna van Harmelen, 2024
"""

from psychopy import visual

ECCENTRICITY = 6
DOT_SIZE = 0.1  # radius of inner circle
TOTAL_DOT_SIZE = 0.35  # radius of outer circle
BAR_SIZE = [0.7, 4]  # width, height
PROBE_CUE_SIZE = 2  # radius of circle (same as response dial size)


decentral_dot = fixation_dot = None


def create_fixation_dot(settings):
    global decentral_dot, fixation_dot

    # Make fixation dot
    if decentral_dot is None:
        decentral_dot = visual.Circle(
            win=settings["window"],
            units="pix",
            radius=settings["deg2pix"](TOTAL_DOT_SIZE),
            pos=(0, 0),
            fillColor="#eaeaea",
        )

    if fixation_dot is None:
        fixation_dot = visual.Circle(
            win=settings["window"],
            units="pix",
            radius=settings["deg2pix"](DOT_SIZE),
            pos=(0, 0),
            fillColor="#000000",
        )

    decentral_dot.draw()
    fixation_dot.draw()


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
    create_fixation_dot(settings)
    make_one_bar(left_orientation, colours[0], "left", settings).draw()
    make_one_bar(right_orientation, colours[1], "right", settings).draw()


def create_capture_cue_frame(colour, settings):
    decentral_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](TOTAL_DOT_SIZE),
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor="#000000",
    )

    return decentral_dot, fixation_dot


def create_probe_cue(colour, settings):
    probe = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](PROBE_CUE_SIZE),
        edges=settings["deg2pix"](1),
        pos=(0, 0),
        lineWidth=settings["deg2pix"](0.1),
        fillColor=None,
        lineColor=colour,
    )
    probe.draw()

    create_fixation_dot(settings)
