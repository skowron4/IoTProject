import time

import neopixel
import socketio
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import board
from config import *


address = "http://192.168.37.240:5000"
passwd = "checcpass"
sio = socketio.Client()

access_list = []


@sio.on('connect', namespace="/card_adder")
def connect():
    print('connection established')


def my_message(card_id):
    sio.emit('card', card_id, namespace="/card_adder")


@sio.on('disconnect', namespace='/card_adder')
def disconnect():
    print('disconnected from server')


def sound_signal_on():
    GPIO.output(buzzerPin, 0)


def sound_signal_off():
    GPIO.output(buzzerPin, 1)


pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
reader = MFRC522()


def pixels_on():
    for i in range(0, 4):
        card_found, _ = reader.MFRC522_Anticoll()
        if card_found == MFRC522.MI_OK:
            pixels[i] = (0, 255, 0)
            pixels.show()
            time.sleep(0.3)
        else:
            return False
    return True


def pixels_off():
    for i in range(0, 4):
        pixels[i] = (0, 0, 0)
    pixels.show()


if __name__ == "__main__":
    sio.connect(address, namespaces=["/card_adder"], headers={"pass": passwd})
    last_card_status = False
    try:
        while True:
            _, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
            status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status != reader.MI_OK:
                last_card_status = False

            if status == reader.MI_OK and not last_card_status:
                status, uid = reader.MFRC522_Anticoll()
                if status == reader.MI_OK:
                    if pixels_on():
                        # send uuid
                        my_message("".join(format(x, "02X") for x in uid))
                        sound_signal_on()
                        time.sleep(0.5)
                        sound_signal_off()
                        last_card_status = True
                    pixels_off()

    finally:
        GPIO.cleanup()
