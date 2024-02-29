"""
This script is used to test random aspects
of the 'unpredictable flickering null-cue experiment'.

made by Anna van Harmelen, 2024
"""

from set_up import get_monitor_and_dir, get_settings
from practice import practice

monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)

practice(True, settings)

# stop here
import sys

sys.exit()
