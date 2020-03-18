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
import time

import obspython as obs
import socket

Debug_Mode = False
enabled_flag = False
is_connected = False

# Create socket when script loaded
s = socket.socket()
s.setblocking(False)
s.bind(("localhost", 50007))
s.listen(1)


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
           "Enabled when script is added." + \
           "<br/><br/>" + \
           "Made by George Hu, © 2018" + \
           "<hr>"


def script_load(settings):
    print("Calling Load")


def script_properties():
    print("Calling properties")


def script_save(settings):
    print("Calling Save")


def script_unload():
    print("Calling unload")


def script_update(settings):
    print("Calling Update")


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def timer_check_recording():
    # print("Timer Event: timer_check_recording")
    global is_connected
    global conn

    if not is_connected:
        try:
            conn, addr = s.accept()
            conn.setblocking(False)
            print("Connection Established.")
            is_connected = True
        except BlockingIOError:
            pass
    else:
        communicate(conn)


def communicate(conn):
    # buffer msg for repeating check if recording started.
    global msg
    global is_connected
    try:
        msg = conn.recv(4096).decode('ascii')
        print("msg: %s", msg)
    except BlockingIOError:
        # Wait incoming msg and prevent to close connection.
        return
    except ConnectionResetError:
        # In Windows, raise ConnectionResetError when connection is closed.
        print("ConnectionResetError")
        msg = False
    if msg == "start recording":
        obs.timer_add(start_recording, 100)
    elif msg == "stop recording":
        obs.timer_add(stop_recording, 100)
    else:
        print("Connection Closed.")
        conn.close()
        is_connected = False


is_stopped = True


def start_recording():
    global is_stopped
    if is_stopped:
        if not obs.obs_frontend_recording_active():
            obs.obs_frontend_recording_start()
            print("Start recording...")
        else:
            obs.timer_remove(start_recording)


def stop_recording():
    global is_stopped

    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()
        print("Stop recording...")
        is_stopped = False
    else:
        obs.timer_remove(stop_recording)
        is_stopped = True


# Add timer for command checking
obs.timer_add(timer_check_recording, 100)
