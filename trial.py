"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'unpredictable flickering null-cue experiment', see main.py.

made by Anna van Harmelen, 2024
"""

from psychopy import visual
from psychopy.core import wait
from time import time, sleep
from response import get_response
from stimuli import (
    create_fixation_dot,
    create_capture_cue_frame,
    create_stimuli_frame,
    create_probe_cue,
)
from eyetracker import get_trigger
import random

# experiment flow:
# 1. fixatiekruis
# 2. fixatiekruis + twee blokkies ernaast
# 3. fixatiekruis
# 4. fixatiekruis + vierkantje om het kruis
# 5. fixatiekruis
# 6. probecue
# 7. dials voor respons van proefpersoon

COLOURS = [[19, 146, 206], [217, 103, 241], [101, 148, 14], [238, 104, 60]]
COLOURS = [
    [(rgb_value / 128 - 1) for rgb_value in rgb_triplet] for rgb_triplet in COLOURS
]


def generate_stimuli_characteristics(condition, target_bar, flicker_type, cue_timing):
    stimuli_colours = random.sample(COLOURS, 2)

    orientations = [
        random.choice([-1, 1]) * random.randint(5, 85),
        random.choice([-1, 1]) * random.randint(5, 85),
    ]

    if target_bar == "left":
        target_colour, distractor_colour = stimuli_colours
        target_orientation = orientations[0]
    else:
        distractor_colour, target_colour = stimuli_colours
        target_orientation = orientations[1]

    if condition == "congruent":
        capture_colour = target_colour
    elif condition == "incongruent":
        capture_colour = distractor_colour

    if cue_timing == "early":
        cue_delay = 0.5
    elif cue_timing == "middle":
        cue_delay = 1.0
    elif cue_timing == "late":
        cue_delay = 1.5

    return {
        "ITI": random.randint(500, 800) / 1000,
        "stimuli_colours": stimuli_colours,
        "flicker_type": flicker_type,
        "cue_delay": cue_delay,
        "capture_colour": capture_colour,
        "trial_condition": condition,
        "left_orientation": orientations[0],
        "right_orientation": orientations[1],
        "target_bar": target_bar,
        "target_colour": target_colour,
        "target_orientation": target_orientation,
    }


def do_while_showing(waiting_time, something_to_do, window):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    window.flip()
    start = time()
    something_to_do()
    wait(waiting_time - (time() - start))


def single_trial(
    ITI,
    flicker_type,
    cue_delay,
    left_orientation,
    right_orientation,
    target_bar,
    target_colour,
    target_orientation,
    stimuli_colours,
    capture_colour,
    trial_condition,
    settings,
    testing,
    eyetracker=None,
):
    # Initial fixation cross to eliminate jitter caused by for loop
    create_fixation_dot(settings)

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (ITI, lambda: create_fixation_dot(settings), None),
        (
            0.25,
            lambda: create_stimuli_frame(
                left_orientation, right_orientation, stimuli_colours, settings
            ),
            "stimuli_onset",
        ),
        (cue_delay, lambda: create_fixation_dot(settings), None),
        (
            0.50,
            lambda: create_capture_cue_frame(capture_colour, settings),
            "capture_cue_onset",
        ),
        (2.0 - cue_delay, lambda: create_fixation_dot(settings), None),
        (None, lambda: create_probe_cue(target_colour, settings), None),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!

    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, trial_condition, target_bar)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

    # The for loop only draws the probe cue, never shows it
    # So show it here
    if not testing:
        trigger = get_trigger("probe_cue_onset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")

    settings["window"].flip()

    response = get_response(
        target_orientation,
        target_colour,
        settings,
        testing,
        eyetracker,
        trial_condition,
        target_bar,
    )

    if not testing:
        trigger = get_trigger("response_offset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Show performance
    create_fixation_dot(settings)
    show_text(
        f"{response['performance']}", settings["window"], (0, settings["deg2pix"](0.7))
    )

    if not testing:
        trigger = get_trigger("feedback_onset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")
    settings["window"].flip()
    sleep(0.25)

    return {
        "condition_code": get_trigger("stimuli_onset", trial_condition, target_bar),
        **response,
    }


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()
