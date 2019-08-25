#!flask/bin/python
from flask import Flask
from flask import request, session
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit

from src.routeController import RouteController
from src.ai.aiManager import AiManager
app = Flask(__name__)
socketio = SocketIO(app)
controller = RouteController()

@socketio.on('join')
def test_connect(data):
    controller.create_ai(data)

    game_id = str(data["game_id"])
    player_id = str(data["player_id"])
    address = AiManager.generate_ai_address(game_id, player_id)
    join_room(address)
    print('Open socket {0} socket info={1}'
          .format(
            address,
            controller.ai_manager.ai_socket_connection_info[game_id][player_id]
        )
    )
    print('Location={0}'
          .format(
            controller.ai_manager.ai_list[game_id][player_id].location
        )
    )


@socketio.on('leave')
def test_disconnect(data):
    message = controller.delete_ai(data)

    if message != AiManager.get_succsess_delete_message():
        emit("can not leave", {"error": message})
    else:
        game_id = data["game_id"]
        player_id = data["player_id"]
        address = AiManager.generate_ai_address(game_id, player_id)
        leave_room(address)
        emit("disconnect")


@socketio.on('send_message')
def handle_json(data):
    room_info = data['channel_info']
    game_id = room_info["game_id"]
    player_id = room_info["player_id"]

    commands = controller.update_ai(
        data['message'],
        param=[game_id, player_id]
    )
    # print('received json: ' + str(commands))

    emit("acceptCommand", commands, room=AiManager.generate_ai_address(game_id, player_id))


@app.route('/ai-server/<string:ai_type>/<string:ai_name>/new', methods=['GET'])
def generate_ai_address(ai_name, ai_type):
    game_id = request.args.get('gameId')
    player_id = request.args.get('playerId')
    return controller.generate_ai_address(
        [game_id, player_id],
        ai_info=[ai_type, ai_name]
    )


if __name__ == '__main__':
    socketio.run(app, debug=True)
