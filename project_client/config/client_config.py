import datetime

import neopixel
import board
import lib.oled.SSD1331 as SSD1331
from mfrc522 import MFRC522
import socketio

config_file = "client_config.txt"
server_address = "http://192.168.37.240:5000"  # need check before run
default_name = "Client1"  # hardcode this :D
disp = SSD1331.SSD1331()
sio = socketio.Client()


cards_permissions = dict()
pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

SECOND_IN_NANO = 10 ** 9


PIXEL_TICK_TIME = 0.2 * SECOND_IN_NANO   # in seconds
TICKS_UNTIL_CARD_READ = 4

MINUTE = 60 * SECOND_IN_NANO

reader = MFRC522()
debounce_stars_effects = 0
last_minute = datetime.datetime.now().minute
current_minute = last_minute

pixel_id = 0
last_card_status = False
access_list = []
