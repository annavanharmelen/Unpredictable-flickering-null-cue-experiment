"""
This script is used to test random aspects
of the 'unpredictable flickering null-cue experiment'.

made by Anna van Harmelen, 2024
"""

from set_up import get_monitor_and_dir, get_settings
from practice import practice
from trial import generate_stimuli_characteristics, single_trial


monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)

stimuli_characteristics: dict = generate_stimuli_characteristics(
        "congruent", "left", "high_freq", "middle", "unpredictable"
    )

try:

    report: dict = single_trial(
        **stimuli_characteristics,
        settings=settings,
        testing=True,
        eyetracker=None,
    )

except Exception as e:
    print(e)

# stop here
import sys

sys.exit()
