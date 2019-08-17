#!flask/bin/python
from flask import Flask
from flask import abort, jsonify, request
from flask_socketio import SocketIO, emit

from server import Controller
from server.game import Game

app = Flask(__name__)
socketio = SocketIO(app)
# /ai-server/:ai-name/new?gameId&playerId
# /ai-server/:ai-name/:game-id/:player-id
controller = Controller()

@socketio.on('connect')
def test_connect():
    print('connect')

# /ai-server/script-bot/Intellectual000/new?gameId=1&playerId=1
@app.route('/ai-server/<string:ai_type>/<string:ai_name>/new', methods=['GET'])
def create_ai(ai_name, ai_type):
    game_id = request.args.get('gameId')
    player_id = request.args.get('playerId')

    return Controller.create_ai_for_game(
        game_info=[game_id, player_id],
        ai_info=[ai_type, ai_name]
    )


def convert_to_game(json_file_content):
    game = Game()
    game.id = json_file_content["id"]
    game.users = json_file_content["users"]

    return game


def validate_game(game, param):
    [game_id, player_id] = param
    valid_id = game.id == game_id
    print(game.users)
    valid_player_id = game.users[str(player_id)] is not None
    if not valid_id:
        raise Exception("Posted game id={0} not equal ai game id ={1}".format(game.id, game_id))
    if not valid_player_id:
        raise Exception("Posted user id={0} not content to game with id={1}".format(game.id, game_id))

@app.route('/ai-server/<int:game_id>/<int:player_id>/', methods=['POST'])
def update_ai(game_id, player_id):
    game = convert_to_game(request.get_json())
    validate_game(game, [game_id, player_id])
    return Controller.update_ai(
        game,
        param=[game_id, player_id]
    )


if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
