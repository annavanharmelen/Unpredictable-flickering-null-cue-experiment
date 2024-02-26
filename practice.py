"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from trial import (
    single_trial,
    generate_stimuli_characteristics,
    show_text,
)
from stimuli import make_one_bar, create_fixation_cross
from response import get_response, wait_for_key
from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from time import sleep
import random

# 1. Practice response dials using a block with a specific orientation
# 2. Practice full trials


def practice(testing, settings):
    # Show explanation
    show_text(
        f"Welcome to the practice trials. You will practice each part until you press Q. \
            \nPress SPACE to start the practice session.",
        settings["window"],
    )
    settings["window"].flip()
    wait_for_key(["space"], settings["keyboard"])

    # Practice dial until user chooses to stop
    try:
        while True:
            target_bar = random.choice(["left", "right"])
            condition = "neutral"
            target = generate_stimuli_characteristics(condition, target_bar)
            target_orientation = target["target_orientation"]
            target_colour = None

            practice_bar = make_one_bar(
                target_orientation, "#eaeaea", "middle", settings
            )

            report: dict = get_response(
                target_orientation,
                target_colour,
                settings,
                testing,
                None,
                1,
                target_bar,
                [practice_bar],
            )

            create_fixation_cross(settings)
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.5)),
            )
            settings["window"].flip()
            sleep(0.5)

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the response dial."
            "Press SPACE to start practicing full trials."
            "\nRemember to press Q to stop practising these trials once you feel comfortable starting the real experiment.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])

    # Practice trials until user chooses to stop
    try:
        while True:
            target_bar = random.choice(["left", "right"])
            condition = random.choice(["congruent", "incongruent", "neutral"])

            stimulus = generate_stimuli_characteristics(condition, target_bar)

            report: dict = single_trial(**stimulus, settings=settings, testing=True)

    except KeyboardInterrupt:
        show_text(
            f"You decided to stop practicing the trials.\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
