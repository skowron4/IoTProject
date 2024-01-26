import datetime

import GPIO

import project_client.effects.effects as ef
import project_client.config.client_config as conf
import threading
import os
import uuid
import time


def read_card():
    _, _ = conf.reader.MFRC522_Request(conf.reader.PICC_REQIDL)
    status, _ = conf.reader.MFRC522_Request(conf.reader.PICC_REQIDL)
    if status != conf.reader.MI_OK:
        conf.last_card_status = False
        return None

    elif status == conf.reader.MI_OK and not conf.last_card_status:
        status, uid = conf.reader.MFRC522_Anticoll()
        if status == conf.reader.MI_OK:
            return str(uid)


def UUID_maker():
    uuid4 = ""
    if os.path.exists(conf.config_file):
        with open(conf.config_file, 'r') as file:
            uuid4 = file.read()
    elif uuid4 == "":
        uuid4 = uuid.uuid4().hex
        with open(conf.config_file, 'w') as file:
            file.write(uuid4)
    return uuid4


def has_permissions(card_uid):
    return card_uid in conf.access_list


def permission_accepted():
    # open door
    threading.Thread(target=ef.accept_effects)


def permissions_denied():
    threading.Thread(target=ef.denied_effects)


def main_loop():
    running = True
    card_read = False  # for reading a card exactly once
    while running:
        card_uid = read_card()  # uid of card currently read
        if card_uid is not None and not card_read:
            # run card-in-use effects
            reading_finished = ef.run_effects()
            # card was read for allowed time
            if reading_finished:
                card_read = True
                if has_permissions(card_uid):
                    permission_accepted()
                else:
                    permissions_denied()
        elif card_uid is None:
            ef.pixels_off()  # possibly unnecessary
            # reset debouncing
            conf.debounce_stars_effects = time.perf_counter_ns()
            card_read = False
            conf.pixel_id = 0

        conf.current_minute = datetime.datetime.now().minute

        if conf.last_minute != conf.current_minute:
            ef.update_clock()
            conf.last_minute = conf.current_minute


def program():
    # setup uuid
    client_uuid = UUID_maker()

    # setup display
    ef.display_init()

    # start client
    conf.sio.connect(conf.server_address,
                     namespaces=["/readers"],
                     headers={'device_id': client_uuid, 'default_client': conf.default_name})

    main_loop()


if __name__ == "__main__":
    try:
        program()
    finally:
        GPIO.cleanup()
