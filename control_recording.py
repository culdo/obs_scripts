#
# Project	OBS Recorder Controller
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
import multiprocessing

import obspython as obs
from obs_controller import start_client

Debug_Mode = False
enabled_flag = True
# ------------------------------------------------------------
# OBS Script Functions
# ------------------------------------------------------------


def script_defaults(settings):
    pass
    print("Calling defaults")


def script_description():
    print("Calling description")

    return "<b>OBS Recorder Controller</b>" + \
           "<hr>" + \
           "Control OBS using IPC of python." + \
           "<br/><br/>" + \
           "Made by George Hu, © 2018" + \
           "<hr>"


def script_load(settings):
    print("Calling Load")
    obs.obs_data_set_bool(settings, "enabled", False)


def script_properties():
    print("Calling properties")

    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "enabled", "Enabled")

    obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
    return props


def script_save(settings):
    print("Calling Save")

    script_update(settings)


def script_unload():
    print("Calling unload")

    obs.timer_remove(timer_check_recording)


def script_update(settings):
    global Debug_Mode
    global cmd
    print("Calling Update")

    if obs.obs_data_get_bool(settings, "enabled") is True:
        print("Loading Timer")
        cmd = start_client()
        obs.timer_add(timer_check_recording, 100)
    else:
        print("Unloading Timer")

        obs.timer_remove(timer_check_recording)

    Debug_Mode = obs.obs_data_get_bool(settings, "debug_mode")


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def timer_check_recording():
    # print("Timer Event: timer_check_recording")
    global cmd

    try:
        if not obs.obs_frontend_recording_active() and cmd.state == "start recording":
            # print("Find gzclient")
            obs.obs_frontend_recording_start()
                # print("Recording is started.")
        elif obs.obs_frontend_recording_active() and cmd.state == "stop recording":
            obs.obs_frontend_recording_stop()
            cmd.state = "idle..."
        elif cmd.state == "disable":
            # obs.obs_frontend_recording_stop()
            obs.timer_remove(timer_check_recording)
        # print("Not find gzclient")
        # print("Recording is stopped.")
    except:
        pass
