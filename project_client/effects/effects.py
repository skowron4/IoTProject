import time
from datetime import datetime
import project_client.config.client_config as conf
from project_client.config.config import *
from PIL import Image, ImageDraw, ImageFont


def run_effects():
    if time.perf_counter_ns() - conf.debounce_stars_effects > conf.PIXEL_TICK_TIME:
        conf.debounce_stars_effects += conf.PIXEL_TICK_TIME
        turn_pixel_on(conf.pixel_id)
        conf.pixel_id += 1
        if conf.pixel_id == conf.TICKS_UNTIL_CARD_READ:
            return True
    return False


def display_init():
    conf.disp.Init()
    conf.disp.clear()


def sound_signal_on():
    GPIO.output(buzzerPin, 0)


def sound_signal_off():
    GPIO.output(buzzerPin, 1)


def turn_pixel_on(index):
    conf.pixels[index] = (0, 255, 0)
    conf.pixels.show()


def pixels_off():
    for i in range(0, 4):
        conf.pixels[i] = (0, 0, 0)
    conf.pixels.show()


def accept_effects():
    conf.pixels.fill((0, 255, 0))
    sound_signal_on()
    conf.pixels.show()
    time.sleep(0.33)
    sound_signal_off()
    time.sleep(0.33)
    sound_signal_on()
    conf.pixels.fill((0, 0, 0))
    time.sleep(0.33)
    sound_signal_off()
    conf.pixels.show()


def denied_effects():
    conf.pixels.fill((255, 0, 0))
    sound_signal_on()
    conf.pixels.show()
    time.sleep(1)
    conf.pixels.fill((0, 0, 0))
    sound_signal_off()
    conf.pixels.show()


def update_clock():
    canvas = Image.new("RGB", (conf.disp.width, conf.disp.height))
    draw = ImageDraw.Draw(canvas)

    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)  # requires test, all code requires xD

    t = datetime.now()

    draw.text((0, 34), t.strftime('%Y-%m-%d %H:%M'), font=font, fill="WHITE")

    conf.disp.ShowImage(canvas, 0, 0)
