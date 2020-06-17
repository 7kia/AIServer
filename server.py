#!flask/bin/python
import threading

import eventlet

from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.game_info import GameInfo

eventlet.monkey_patch()

from flask import Flask
from flask import request, session
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit

from src.routeController import RouteController
from src.ai.ai_manager import AiManager

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True)
controller = RouteController()
sem = threading.Semaphore()

@socketio.on('join')
def test_connect(data):
    # sem.acquire()
    print("join")
    controller.create_ai(data)

    room_info = data['channel_info']
    game_id = str(room_info["game_id"])
    player_id = str(room_info["player_id"])
    address = AiManager.generate_ai_address(game_id, player_id)
    join_room(address)
    print('Open socket {0} socket info={1}'
        .format(
        address,
        controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)
    )
    )
    print('Location={0}'
        .format(
        controller.ai_manager.get_ai(game_id, player_id).get_location()
    )
    )
    print("get_unit_count room={0}".format(address))
    emit("get_unit_count", "", room=address)
    # sem.release()

@socketio.on('leave')
def test_disconnect(data):
    sem.acquire()
    game_id = str(data["game_id"])
    player_id = str(data["player_id"])

    message = controller.delete_ai(GameInfo(game_id, player_id))

    if message != AiManager.get_succsess_delete_message():
        # TODO(7kis) not check work the code
        emit("can_not_leave", str({"error": message}), room=AiManager.generate_ai_address(game_id, player_id))
    else:
        game_id = data["game_id"]
        player_id = data["player_id"]
        address = AiManager.generate_ai_address(game_id, player_id)
        leave_room(address)
        emit("disconnect")
    sem.release()

@socketio.on('setUnitCount')
def set_unit_count(data):
    sem.acquire()
    room_info = data['channel_info']
    game_id = str(room_info["game_id"])
    player_id = str(room_info["player_id"])

    unit_positions = controller.generate_ai_unit_positions(game_id, player_id, data['message'])
    print(unit_positions)
    print("place_units")
    emit("place_units", unit_positions, room=AiManager.generate_ai_address(game_id, player_id))
    sem.release()

@socketio.on('sendGame')
def handle_json(data):
    sem.acquire()
    print(f"sendGame {data}")
    room_info = data['channel_info']
    game_id = room_info["game_id"]
    player_id = room_info["player_id"]

    commands = controller.update_ai(
        data['gameState'],
        game_info=GameInfo(game_id, player_id)
    )
    # print('received json: ' + str(commands))

    address = AiManager.generate_ai_address(game_id, player_id)
    print("accept_command address={0}".format(address))
    emit("accept_command", commands, room=address)
    sem.release()


@app.route('/ai-server/<string:ai_type>/<string:ai_address>/new', methods=['GET'])
def generate_ai_address(ai_address, ai_type):
    game_id = int(request.args.get('gameId'))
    player_id = int(request.args.get('playerId'))
    return controller.generate_ai_address(
        game_info=GameInfo(game_id, player_id),
        ai_info=AiInfo(ai_type, ai_address)
    )


@app.route('/get-ai-list', methods=['GET'])
def generate_ai_list():
    return controller.generate_ai_list()


@app.route('/get-ai-type-list', methods=['GET'])
def generate_ai_type_list():
    return controller.generate_ai_type_list()


if __name__ == '__main__':
    socketio.run(app, debug=True)
