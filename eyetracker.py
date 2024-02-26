"""
This file contains the functions necessary for
connecting and using the eyetracker.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023, using code by Rose Nasrawi
"""

from lib import eyelinker
from psychopy import event
import os


class Eyelinker:
    """
    usage:

       from eyetracker import Eyelinker

    To initialise:

       eyelinker = Eyelinker(participant, session, window, directory)
       eyelinker.calibrate()
    """

    def __init__(self, participant, session, window, directory) -> None:
        """
        This also connects to the tracker
        """
        self.directory = directory
        self.window = window
        self.tracker = eyelinker.EyeLinker(
            window=window, eye="RIGHT", filename=f"{session}_{participant}.edf"
        )
        self.tracker.init_tracker()

    def start(self):
        self.tracker.start_recording()

    def calibrate(self):
        self.tracker.calibrate()

    def stop(self):
        os.chdir(self.directory)

        self.tracker.stop_recording()
        self.tracker.transfer_edf()
        self.tracker.close_edf()


def get_trigger(frame, condition, target_position):
    condition_marker = {"congruent": 1, "incongruent": 3, "neutral": 5}[condition]

    if target_position == "right":
        condition_marker += 1

    return {
        "stimuli_onset": "",
        "capture_cue_onset": "1",
        "probe_cue_onset": "2",
        "response_onset": "3",
        "response_offset": "4",
        "feedback_onset": "5",
    }[frame] + str(condition_marker)
