#!/usr/bin/python
"""
lcd-web.py:
    write strings from a web socket to a simple LCD screen.

Copyright 2016 Tijndagamer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from LCD_i2c import LCD_i2c
import socket
import argparse
from time import sleep

ADDRESS = 0x27
WIDTH = 16
MAX_LINES = 2
BACKLIGHT = True
CLEAR_TIME = 10
lcd = None

def read_config():
    """Reads and stores configuration values."""
    global ADDRESS
    global WIDTH
    global MAX_LINES
    global BACKLIGHT
    global CLEAR_TIME
    with open("/etc/lcd-echo.conf", "r") as config_file:
        contents = config_file.read()
    contents_list = contents.split("\n")
    for line in contents_list:
        if line.startswith("address"):
            ADDRESS = int(line.split(" = ")[1], 0)
        elif line.startswith("width"):
            WIDTH = int(line.split(" = ")[1])
        elif line.startswith("max_lines"):
            MAX_LINES = int(line.split(" = ")[1])
        elif line.startswith("backlight"):
            if line.split(" = ")[1] == "True":
                BACKLIGHT = True
            else:
                BACKLIGHT = False
        elif line.startswith("clear_time"):
            CLEAR_TIME = int(line.split(" = ")[1])
        else:
            pass
    init()

def init():
    global lcd
    lcd = LCD_i2c(ADDRESS, WIDTH, MAX_LINES, BACKLIGHT)

parser = argparse.ArgumentParser(description="Display a line of text from a web socket on a LCD screen")
parser.add_argument("-p", "--port", metavar="n", type=int, help="specify which port lcd-web should listen at. (default 10001)")
parser.add_argument("-b", "--buffer-size", metavar="n", type=int, help="specify the buffer size (default 1024)")
parser.add_argument("-v", "--verbose", help="change verbosity of the program")
args = parser.parse_args()
if args.port is not None:
    port = args.port
else:
    port = 10001
read_config()
if args.buffer_size is not None:
    buffer_size = args.buffer_size
else:
    buffer_size = 1024

# Get local IP address. Thanks to someone on stackoverflow
host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if args.verbose:
    print host
    print port

sock.bind((host, port))
sock.listen(5)

while True:
    connection, connection_address = sock.accept()
    if args.verbose:
        print("got connection w/ " + str(connection_address))
    try:
        recv_msg = connection.recv(buffer_size)
        lcd.lcd_print(recv_msg.strip("\n")) # Remove newline character
        if args.verbose:
            print(recv_msg)
    except:
        pass
    connection.close()
    if args.verbose:
        print("Connection with " + str(connection_address) + " closed.")
