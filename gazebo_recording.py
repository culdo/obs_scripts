#
# Project	Gazebo Simulating Recorder
# Version	1.0
# @author	George Hu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# ------------------------------------------------------------
# Main Script Area
# ------------------------------------------------------------

import obspython as obs
from subprocess import check_output
import os

Debug_Mode = False
Enabled_Recording = True


# ------------------------------------------------------------
# OBS Script Functions
# ------------------------------------------------------------

def script_defaults(settings):
    pass
    # if Debug_Mode: print("Calling defaults")


def script_description():
    # if Debug_Mode: print("Calling description")

    return "<b>Gazebo Simulating Recorder</b>" + \
           "<hr>" + \
           "Auto stop recording when Gazebo get closed." + \
           "<br/><br/>" + \
           "Made by George Hu, © 2018" + \
           "<hr>"


def script_load(settings):
    # if Debug_Mode: print("Calling Load")

    obs.obs_data_set_bool(settings, "enabled", False)


def script_properties():
    # if Debug_Mode: print("Calling properties")

    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "enabled", "Enabled")

    obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
    return props


def script_save(settings):
    # if Debug_Mode: print("Calling Save")

    script_update(settings)


def script_unload():
    # if Debug_Mode: print("Calling unload")

    obs.timer_remove(timer_check_recording)


def script_update(settings):
    global Debug_Mode
    # if Debug_Mode: print("Calling Update")

    global Enabled_Recording

    if obs.obs_data_get_bool(settings, "enabled") is not Enabled_Recording:
        if obs.obs_data_get_bool(settings, "enabled") is True:
            # if Debug_Mode: print("Loading Timer")

            Enabled_Recording = True
            obs.timer_add(timer_check_recording, 1000)
        else:
            # if Debug_Mode: print("Unloading Timer")

            Enabled_Recording = False
            obs.timer_remove(timer_check_recording)

    Debug_Mode = obs.obs_data_get_bool(settings, "debug_mode")


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def timer_check_recording():
    # print("Timer Event: timer_check_recording")

    global Enabled_Recording

    if get_pid("gzclient"):
        # print("Find gzclient")
        if not obs.obs_frontend_recording_active():
            obs.obs_frontend_recording_start()
            # print("Recording is started.")
    elif obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()
        # print("Not find gzclient")
        # print("Recording is stopped.")


def get_pid(name):
    try:
        check_output(["pidof", name])
        return True
    except:
        return False
