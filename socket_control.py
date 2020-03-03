#
# Project	Recorder Controller using python socket
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
import socket

s = socket.socket()
s.setblocking(False)
s.bind(("localhost", 50007))
s.listen(1)


Debug_Mode = False
enabled_flag = False
is_connected = False
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
    # script_update(settings)


def script_unload():
    print("Calling unload")

    obs.timer_remove(timer_check_recording)


def script_update(settings):
    global Debug_Mode
    global enabled_flag
    print("Calling Update")

    if obs.obs_data_get_bool(settings, "enabled") and not enabled_flag:
        enabled_flag = True
        print("Loading Timer")

        obs.timer_add(timer_check_recording, 100)
    elif not obs.obs_data_get_bool(settings, "enabled") and enabled_flag:
        enabled_flag = False
        print("Unloading Timer")

        obs.timer_remove(timer_check_recording)

    Debug_Mode = obs.obs_data_get_bool(settings, "debug_mode")


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def timer_check_recording():
    # print("Timer Event: timer_check_recording")
    global is_connected
    global conn
    # buffer msg for repeating check if recording started.
    global msg

    if not is_connected:
        try:
            conn, addr = s.accept()
            conn.setblocking(False)
            print("Connection Established.")
            is_connected = True
        except BlockingIOError:
            pass
    else:
        try:
            msg = conn.recv(4096).decode('ascii')
        except BlockingIOError:
            pass
        if msg:
            if not obs.obs_frontend_recording_active() and msg == "start recording":
                obs.obs_frontend_recording_start()
                print(msg)
            elif obs.obs_frontend_recording_active() and msg == "stop recording":
                obs.obs_frontend_recording_stop()
                print(msg)
        else:
            print("Connection Closed.")
            conn.close()
            is_connected = False


        # print("Not find gzclient")
        # print("Recording is stopped.")
