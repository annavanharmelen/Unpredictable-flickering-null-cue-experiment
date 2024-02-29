"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'unpredictable flickering null-cue experiment', see main.py.

made by Anna van Harmelen, 2024
"""

from trial import (
    single_trial,
    generate_stimuli_characteristics,
    show_text,
)
from stimuli import make_one_bar, create_fixation_dot
from response import get_response, wait_for_key
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
            target_orientation = random.choice([-1, 1]) * random.randint(5, 85)

            practice_bar = make_one_bar(
                target_orientation, "#eaeaea", "middle", settings
            )

            report: dict = get_response(
                target_orientation,
                practice_bar.fillColor,
                settings,
                testing,
                None,
                1,
                "left",
                [practice_bar],
            )

            create_fixation_dot(settings)
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
            congruency = random.choice(["congruent", "incongruent"])
            location = random.choice(["left", "right"])
            flicker_type = random.choice(["stable", "invisible", "visible"])
            cue_timing = random.choice(["early", "middle", "late"])

            stimulus = generate_stimuli_characteristics(
                congruency, location, flicker_type, cue_timing
            )

            report: dict = single_trial(**stimulus, settings=settings, testing=True)

    except KeyboardInterrupt:
        show_text(
            f"You decided to stop practicing the trials.\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
