"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'unpredictable flickering null-cue experiment', see main.py.

made by Anna van Harmelen, 2024
"""

import random
from trial import show_text
from response import wait_for_key


def create_blocks(n_blocks):
    if n_blocks % 6 != 0:
        raise Exception("Expected number of blocks to be divisible by 4.")

    # Generate an equal number of blocks of all types
    block_types = [
        ("predictable", "early"),
        ("predictable", "middle"),
        ("predictable", "late"),
        ("unpredictable", 0),
        ("unpredictable", 0),
        ("unpredictable", 0),
    ]

    blocks = n_blocks // 6 * block_types
    random.shuffle(blocks)

    # Save list of sets of block numbers (in order) + block types
    blocks = list(zip(range(1, n_blocks + 1), block_types))

    return blocks


def create_trials_in_block(n_trials, block_type):
    if n_trials % 36 != 0:
        raise Exception("Expected number of trials to be divisible by 36.")

    # Generate equal distribution of target locations
    locations = 3 * (n_trials // 6 * ["left"] + n_trials // 6 * ["right"])

    # Generate equal distribution of congruencies,
    # that co-occur equally with the target locations
    congruencies = 6 * (
        n_trials // 12 * ["congruent"] + n_trials // 12 * ["incongruent"]
    )

    # Generate equal distribution of flicker types,
    # that co-occur equally with both target locations and directions
    flicker_types = 3 * (n_trials // 3 * ["stable", "invisible", "visible"])

    # Generate timing of capture cue onset in each trial depending on block_type
    if block_type[0] == "predictable":
        cue_timings = n_trials * [block_type[1]]

    elif block_type[0] == "unpredictable":
        cue_timings = (
            n_trials // 3 * ["early"]
            + n_trials // 3 * ["middle"]
            + n_trials // 3 * ["late"]
        )

    else:
        raise Exception(
            "Could not understand block_type passed to create_trials_in_block()"
        )

    # Create trial parameters for all trials
    trials = list(zip(locations, congruencies, flicker_types, cue_timings))
    random.shuffle(trials)

    return trials


def block_break(current_block, n_blocks, settings, eyetracker):
    blocks_left = n_blocks - current_block

    show_text(
        f"You just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
        f"have {blocks_left} block{'s' if blocks_left != 1 else ''} left. "
        "Take a break if you want to, but try not to move your head during this break."
        "\nPress SPACE when you're ready to continue.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            eyetracker.start()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def long_break(n_blocks, settings, eyetracker):
    show_text(
        f"You're halfway through! You have {n_blocks // 2} blocks left. "
        "Now is the time to take a longer break. Maybe get up, stretch, walk around."
        "\nPress SPACE whenever you're ready to continue again.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def finish(n_blocks, settings):
    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks!"
        "You're completely done now. Press SPACE to exit the experiment.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])


def quick_finish(settings):
    show_text(
        f"You've exited the experiment. Press SPACE to close this window.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
