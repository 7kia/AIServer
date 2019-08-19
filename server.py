#!flask/bin/python
from flask import Flask
from flask import request, session
from flask_socketio import SocketIO

from src.routeController import RouteController

app = Flask(__name__)
socketio = SocketIO(app)
# @socketio.on('connect')
# def test_connect():
#     print('connect')

controller = RouteController()
@app.route('/ai-server/<string:ai_type>/<string:ai_name>/new', methods=['GET'])
def create_ai(ai_name, ai_type):
    return controller.create_ai_for_game(
        request,
        ai_info=[ai_type, ai_name]
    )

@app.route('/ai-server/<int:game_id>/<int:player_id>/', methods=['POST'])
def update_ai(game_id, player_id):
    return controller.update_ai(
        request,
        param=[game_id, player_id]
    )

@app.route('/ai-server/<int:game_id>/<int:player_id>/delete', methods=['GET'])
def delete_ai(game_id, player_id):
    return controller.delete_ai(
        param=[game_id, player_id]
    )

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
