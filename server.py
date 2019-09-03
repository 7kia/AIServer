#!flask/bin/python
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask import request, session
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit

from src.routeController import RouteController
from src.ai.aiManager import AiManager
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True)
controller = RouteController()


@socketio.on('join')
def test_connect(data):
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




@socketio.on('leave')
def test_disconnect(data):
    game_id = str(data["game_id"])
    player_id = str(data["player_id"])

    message = controller.delete_ai([game_id, player_id])

    if message != AiManager.get_succsess_delete_message():
        # TODO(7kis) not check work the code
        emit("can_not_leave", str({"error": message}), room=AiManager.generate_ai_address(game_id, player_id))
    else:
        game_id = data["game_id"]
        player_id = data["player_id"]
        address = AiManager.generate_ai_address(game_id, player_id)
        leave_room(address)
        emit("disconnect")


@socketio.on('setUnitCount')
def set_unit_count(data):
    room_info = data['channel_info']
    game_id = str(room_info["game_id"])
    player_id = str(room_info["player_id"])

    unit_positions = controller.generate_ai_unit_positions(game_id, player_id, data['message'])
    print("place_units")
    emit("place_units", unit_positions, room=AiManager.generate_ai_address(game_id, player_id))


@socketio.on('sendMessage')
def handle_json(data):
    room_info = data['channel_info']
    game_id = room_info["game_id"]
    player_id = room_info["player_id"]

    commands = controller.update_ai(
        data['message'],
        param=[game_id, player_id]
    )
    # print('received json: ' + str(commands))

    address = AiManager.generate_ai_address(game_id, player_id)
    print("accept_command address={0}".format(address))
    emit("accept_command", commands, room=address)


@app.route('/ai-server/<string:ai_type>/<string:ai_name>/new', methods=['GET'])
def generate_ai_address(ai_name, ai_type):
    game_id = int(request.args.get('gameId'))
    player_id = int(request.args.get('playerId'))
    return controller.generate_ai_address(
        [game_id, player_id],
        ai_info=[ai_type, ai_name]
    )


if __name__ == '__main__':
    socketio.run(app, debug=True)
