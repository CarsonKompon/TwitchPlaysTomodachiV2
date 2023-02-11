# Twitch Plays Tomodachi v2.0
# Created by Carson Kompon
# Using TPPFLUSH by hlinxed

import re
import time
import sys
import traceback
import socket
import threading
from datetime import datetime

import pyglet
import discord
from dotenv import dotenv_values

from tppflush import *
from visuals import draw_touches, new_touch

ENV = dotenv_values()

# Init Pyglet
window = pyglet.window.Window(320, 240)

# 3DS Input Redirection Connection
if len(sys.argv) < 2:
    originalIp = "192.168.1.111"
else:
    originalIp = sys.argv[1]
ip = originalIp
server = LumaInputServer(ip)

# Twitch Chat Connection
sock = socket.socket()
lastMessageSent = datetime.now()
def chat_connect():
    global sock, lastMessageSent
    sock = socket.socket()
    sock.connect((ENV["TWITCH_CHAT_HOST"], int(ENV["TWITCH_CHAT_PORT"])))
    sock.send(("PASS " + ENV["TWITCH_BOT_OAUTH"] + "\n").encode("utf-8"))
    sock.send(("NICK " + ENV["TWITCH_BOT_USERNAME"] + "\n").encode("utf-8"))
    sock.send(("JOIN #" + ENV["TWITCH_CHAT_CHANNEL"] + "\n").encode("utf-8"))
    lastMessageSent = datetime.now()
chat_connect()

# Command Queue
commandQueue = []

# Error handling
def error_handle_exception(exc_type, exc_value, exc_traceback):
    log_entry = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(log_entry)
    webhook = discord.SyncWebhook.from_url(ENV["DISCORD_WEBHOOK"])
    webhook.send(log_entry)
sys.excepthook = error_handle_exception

# Alert Mods
def alert_mods(message):
    global sock, lastMessageSent
    print("ALERTED MODS: " + message)
    webhook = discord.SyncWebhook.from_url(ENV["DISCORD_WEBHOOK"])
    webhook.send(message)
    if (datetime.now() - lastMessageSent).total_seconds() > 3:
        sock.send(("PRIVMSG #" + ENV["TWITCH_CHAT_CHANNEL"] + " :The mods have been alerted!\n").encode("utf-8"))
        lastMessageSent = datetime.now()

# Functions for 3DS-related input
def button_press(button, delay=0.1):
    print("BUTTON: " + str(button) + ", " + str(delay) + "s")
    global server
    server.press(button)
    server.send()
    time.sleep(delay)
    server.unpress(button)
    server.send()

def touch_press(x, y, delay=0.15, username="CarsonKompon"):
    print("TOUCH: " + str(x) + ", " + str(y) + ", " + str(delay) + "s (" + username + ")")
    global server, visualTouches
    x = max(0, min(319, int(x)))
    y = max(0, min(239, int(y)))
    new_touch(float(x), float(y), 16, (255, 0, 0), username)
    server.touch(x, y)
    server.send()
    time.sleep(delay)
    server.clear_touch()
    server.send()

def touch_drag(x1, y1, x2, y2, delay=0.1):
    print("DRAG: " + str(x1) + ", " + str(y1) + " -> " + str(x2) + ", " + str(y2))
    global server
    x1 = max(0, min(319, int(x1)))
    y1 = max(0, min(239, int(y1)))
    x2 = max(0, min(319, int(x2)))
    y2 = max(0, min(239, int(y2)))
    server.touch(x1, y1)
    server.send()
    time.sleep(delay)
    server.touch(x2, y2)
    server.send()
    time.sleep(delay)
    server.clear_touch()
    server.send()

def circlepad_press(button, delay=0.1):
    print("CIRCLEPAD: " + str(button) + ", " + str(delay) + "s")
    global server
    server.circle_pad_set(button)
    server.send()
    time.sleep(delay)
    server.circle_pad_set(CPAD_Commands.CPADNEUTRAL)
    server.send()

def cstick_press(button, delay=0.1):
    print("CSTICK: " + str(button) + ", " + str(delay) + "s")
    global server
    server.n3ds_cstick_set(button)
    server.send()
    time.sleep(delay)
    server.n3ds_cstick_set(CSTICK_Commands.CSTICKNEUTRAL)
    server.send()

# Process commands
def process_command(message: str, username: str):
    command = message.replace("\r","").replace("\n","").split(" ")
    command[0] = command[0].lower()
    validCommand = True

    # Alert Mods Command
    if command[0].startswith("!mod") or command[0].startswith("!alert"):
        if len(command) > 1:
            alert_mods(username + ": " + (" ".join(command[1:])))
        else:
            alert_mods(username + " has requested assistance!")

    # Touch Command
    elif command[0] == "touch" and len(command) == 3:
        touch_press(command[1], command[2], username=username)

    # Drag Command
    elif (command[0] == "drag" or command[0] == "touch") and len(command) == 5:
        touch_drag(command[1], command[2], command[3], command[4])
    
    # Hold Command
    elif (command[0] == "hold" or command[0] == "touch") and len(command) == 4:
        touch_press(command[1], command[2], max(0, min(float(command[3]) / 10, 5)))

    # Shoulder Buttons
    elif command[0] == "l":
        button_press(HIDButtons.L)
    elif command[0] == "r":
        button_press(HIDButtons.R)

    # D-Pad Commands
    elif command[0] == "up" or command[0] == "dup":
        if len(command) == 2:
            button_press(HIDButtons.DPADUP, max(0, min(float(command[1]) / 10, 5)))
        else:
            button_press(HIDButtons.DPADUP)
    elif command[0] == "down" or command[0] == "ddown":
        if len(command) == 2:
            button_press(HIDButtons.DPADDOWN, max(0, min(float(command[1]) / 10, 5)))
        else:
            button_press(HIDButtons.DPADDOWN)
    elif command[0] == "left" or command[0] == "dleft":
        if len(command) == 2:
            button_press(HIDButtons.DPADLEFT, max(0, min(float(command[1]) / 10, 5)))
        else:
            button_press(HIDButtons.DPADLEFT)
    elif command[0] == "right" or command[0] == "dright":
        if len(command) == 2:
            button_press(HIDButtons.DPADRIGHT, max(0, min(float(command[1]) / 10, 5)))
        else:
            button_press(HIDButtons.DPADRIGHT)

    # Circle Pad Commands
    elif command[0] == "cup":
        if len(command) == 2:
            circlepad_press(CPAD_Commands.CPADUP, max(0, min(float(command[1]) / 10, 5)))
        else:
            circlepad_press(CPAD_Commands.CPADUP)
    elif command[0] == "cdown":
        if len(command) == 2:
            circlepad_press(CPAD_Commands.CPADDOWN, max(0, min(float(command[1]) / 10, 5)))
        else:
            circlepad_press(CPAD_Commands.CPADDOWN)
    elif command[0] == "cleft":
        if len(command) == 2:
            circlepad_press(CPAD_Commands.CPADLEFT, max(0, min(float(command[1]) / 10, 5)))
        else:
            circlepad_press(CPAD_Commands.CPADLEFT)
    elif command[0] == "cright":
        if len(command) == 2:
            circlepad_press(CPAD_Commands.CPADRIGHT, max(0, min(float(command[1]) / 10, 5)))
        else:
            circlepad_press(CPAD_Commands.CPADRIGHT)

    # Wait Command
    elif command[0] == "wait" and len(command) == 2:
        time.sleep(max(0, min(float(command[1]) / 10, 5)))

    # If the command is not valid
    else:
        validCommand = False
    
    if validCommand:
        print("COMMAND: " + message)

# Twitch message handling
def handle_message():
    global sock

    try:
        # Check for new messages
        response = sock.recv(2048).decode("utf-8")
        
        if response.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))
        elif len(response) > 0:
            if response.startswith(":"):
                messageTime = datetime.now().strftime("%H:%M:%S")
                bundle = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', response)
                if bundle is not None:
                    username, channel, pureMessage = bundle.groups()
                    print(f"[{messageTime}] {username}: {pureMessage}")

                    commands = pureMessage.split(";")

                    for command in commands:
                        commandQueue.append({
                            "message": command,
                            "username": username
                        })
    except Exception as e:
        print("WHOA! Something went wrong! Let's try reconnecting...")
        sock.close()
        time.sleep(1)
        chat_connect()
        time.sleep(1)
    handle_message()
threadMessageHandler = threading.Thread(target=handle_message, daemon=True)
threadMessageHandler.start()

# Command Queue Handling
def handle_command_queue():
    global commandQueue

    while True:
        if len(commandQueue) > 0:
            command = commandQueue.pop(0)
            process_command(command["message"], command["username"])
        time.sleep(0.05)
threadCommandQueueHandler = threading.Thread(target=handle_command_queue, daemon=True)
threadCommandQueueHandler.start()

# Mouse Click
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        touch_press(x, 240-y)

# Keyboard Press
@window.event
def on_key_press(symbol, modifiers):
    global server

    # Arrow Keys
    if symbol == pyglet.window.key.UP:
        server.press(HIDButtons.DPADUP)
        server.send()
    elif symbol == pyglet.window.key.DOWN:
        server.press(HIDButtons.DPADDOWN)
        server.send()
    elif symbol == pyglet.window.key.LEFT:
        server.press(HIDButtons.DPADLEFT)
        server.send()
    elif symbol == pyglet.window.key.RIGHT:
        server.press(HIDButtons.DPADRIGHT)
        server.send()

    # Z and X for A and B
    elif symbol == pyglet.window.key.Z:
        server.press(HIDButtons.A)
        server.send()
    elif symbol == pyglet.window.key.X:
        server.press(HIDButtons.B)
        server.send()
    
    # Enter and Backspace for Start and Select
    elif symbol == pyglet.window.key.ENTER:
        server.press(HIDButtons.START)
        server.send()
    elif symbol == pyglet.window.key.BACKSPACE:
        server.press(HIDButtons.SELECT)
        server.send()

    # Q to quit
    elif symbol == pyglet.window.key.Q:
        server.socket.close()
        sock.close()
        pyglet.app.exit()

# Keyboard Released
@window.event
def on_key_release(symbol, modifiers):
    global server

    # Arrow Keys
    if symbol == pyglet.window.key.UP:
        server.unpress(HIDButtons.DPADUP)
        server.send()
    elif symbol == pyglet.window.key.DOWN:
        server.unpress(HIDButtons.DPADDOWN)
        server.send()
    elif symbol == pyglet.window.key.LEFT:
        server.unpress(HIDButtons.DPADLEFT)
        server.send()
    elif symbol == pyglet.window.key.RIGHT:
        server.unpress(HIDButtons.DPADRIGHT)
        server.send()

    # Z and X for A and B
    elif symbol == pyglet.window.key.Z:
        server.unpress(HIDButtons.A)
        server.send()
    elif symbol == pyglet.window.key.X:
        server.unpress(HIDButtons.B)
        server.send()
    
    # Enter and Backspace for Start and Select
    elif symbol == pyglet.window.key.ENTER:
        server.unpress(HIDButtons.START)
        server.send()
    elif symbol == pyglet.window.key.BACKSPACE:
        server.unpress(HIDButtons.SELECT)
        server.send()

# Window Drawing
@window.event
def on_draw():
    global visualTouches
    
    window.clear()

    # Draw visual touches
    draw_touches()


pyglet.app.run()