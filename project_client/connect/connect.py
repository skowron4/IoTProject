from project_client.config.client_config import sio
import project_client.config.client_config as conf


@sio.on('connect', namespace="/readers")
def connect():
    print("I'm connected!")
    sio.emit("get_data", namespace="/readers")


@sio.on("access_data", namespace="/readers")
def receive_data(data):
    print("Received access list: ", data)
    conf.access_list[:] = data


# Data
def update_data(data):
    # update the cards list
    conf.cards_permissions = data
#
# @sio.on("update", namespace="/readers")
# def notify_server_updated():
#     sio.emit("get_data", callback=update_data, namespace="/readers")
#     print("Update incoming - fetching new access tables")


@sio.on("update", namespace="/readers")
def server_updated():
    print("Update incoming - fetching new access tables")
    sio.emit('get_data', namespace="/readers")


@sio.event
def disconnect():
    print("I'm disconnected")

