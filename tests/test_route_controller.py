import asynctest
import json

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.location_builder import LocationBuilder
from src.ai.game_components.location import Location
from src.routeController import RouteController

AI_SERVER_HOST = 'http://127.0.0.1'
AI_SERVER_PORT = '5000'
AI_SERVER_ADDRESS = AI_SERVER_HOST + ":" + AI_SERVER_PORT


class TestRouteController(asynctest.TestCase):
    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/new?gameId={2}&playerId={3}' \
            .format(ai_type, ai_name, game_id, player_id)

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}".format(game_id, player_id)

    def test_generate_ai_address(self):
        controller = RouteController()

        game_id = 2
        player_id = 21
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        game_info = [game_id, player_id]
        ai_info = [ai_type, ai_name]

        response = controller.generate_ai_address(game_info, ai_info)
        self.assertEqual(response, (TestRouteController.generate_ai_address(game_id, player_id), 200))

    @staticmethod
    def generate_mock_location_info():
        return {
            "id": "win_mechanic_test",
            "name": "Win mechanic test",
            "countries": [
                "Russia",
                "NATO"
            ],
            "bounds": {
                "NE": [
                    50.21621729063866,
                    40.330193359375016
                ],
                "SW": [
                    46.9890206199942,
                    35.3890859375
                ]
            },
            "boundsCountry": {
                "Russia": {
                    "NE": [
                        48.12276619505541,
                        39.802849609375016
                    ],
                    "SW": [
                        47.869711326279216,
                        37.74839990234375
                    ]
                },
                "NATO": {
                    "NE": [
                        49.767717668674585,
                        37.028801757812516
                    ],
                    "SW": [
                        47.10879329270628,
                        35.32042138671875
                    ]
                }
            },
            "resources": {
                "Russia": {
                    "ammo": 100,
                    "fuel": 0,
                    "food": 0,
                    "man": 0
                },
                "NATO": {
                    "ammo": 300,
                    "fuel": 0,
                    "food": 0
                }
            },
            "units": {
                "Russia": {
                    "tank": {
                        "regiment": 1
                    },
                    "landbase": {
                        "tactic": 1
                    }
                },
                "NATO": {
                    "landbase": {
                        "tactic": 1
                    }
                }
            },
            "weapons": {
                "Russia": [
                    1984,
                    1986
                ]
            }
        }

    @classmethod
    def create_template_controller_with_ai(cls, game_id, player_id, ai_type, ai_name):
        controller = RouteController()
        controller.test_mode = True
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": ai_type,
            "ai_address": ai_name,
            "location": TestRouteController.generate_mock_location_info(),
            "country": "NATO",
        }
        controller.create_ai(input_data)
        return controller

    @classmethod
    def generate_position_to_center_map(cls, ai):
        ai_location = ai.get_location()
        bounds_country = ai_location.bounds_country[ai.get_country()]
        return [
            (bounds_country["NE"].x + bounds_country["SW"].x) / 2,
            (bounds_country["NE"].y + bounds_country["SW"].y) / 2,
        ]

    def test_create_ai(self):
        game_id = "3"
        player_id = "31"
        country = "NATO"
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_address": "intellectual-000",
            "location": TestRouteController.generate_mock_location_info(),
            "country": country,
            "gameState": self.generate_test_game_state(),
        }

        controller = RouteController()

        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)

        controller.create_ai(input_data)

        # (7kia) For creating connection create ai_socket_connection_info on AI server
        # for understanding that server handle request or no
        try:
            ai = controller.ai_manager.get_ai(game_id, player_id)
            self.assertEqual(ai is not None, True)
            self.assertEqual(
                ai.get_location(),
                LocationBuilder.build(
                    TestRouteController.generate_mock_location_info()
                ))
            self.assertEqual(ai.get_country(), country)

            ai_socket_connection_info = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)
            self.assertEqual(
                ai_socket_connection_info,
                TestRouteController.generate_ai_address(game_id, player_id)
            )
        except Exception as e:
            self.fail(e)

    def test_update_ai(self):
        game_id = "4"
        player_id = "41"
        ai_type = "script-bot"
        ai_name = "test-bot"

        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)
        json_object = {
            "id": game_id,
            "users": {player_id: {}},
            "loserId": None,
            "status": None,
            "units": {
                "ownUnits": {
                    "regiments": {},
                    "bases": {},
                    "supports": {},
                },
                "visibleEnemyUnits": {
                    "regiments": {},
                    "bases": {},
                    "supports": {},
                }
            },
            "currentGameTime": None,
            "battleMatrix": None,
        }
        commands: dict = json.loads(controller.update_ai(json_object, [game_id, player_id]))

        position = TestRouteController.generate_position_to_center_map(
            controller.ai_manager.get_ai(game_id, player_id)
        )
        self.assertEqual(
            commands,
            {
                "data":
                    [
                        {
                            "commandName": "move_or_attack",
                            "arguments": {
                                "unit_id": 1,
                                "position": position
                            }
                        },
                        {
                            "commandName": "retreat_or_storm",
                            "arguments": {
                                "unit_id": 2,
                                "position": position
                            }
                        },
                        {
                            "commandName": "stop_or_defence",
                            "arguments": {
                                "unit_id": 3
                            }
                        },
                    ]
            }
        )

    def test_delete_ai(self):
        game_id = "5"
        player_id = "51"
        ai_type = "script-bot"
        ai_name = "intellectual-000"
        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)
        message = controller.delete_ai([game_id, player_id])

        self.assertEqual(message, "Ai delete")
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)

    def test_set_ai_unit_positions(self):
        game_id = "6"
        player_id = "61"
        ai_type = "script-bot"
        ai_name = "intellectual-000"
        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)

        unit_counts = {
            "tank": {
                "regiment": 1,
            },
            "landbase": {
                "tactic": 1,
            },
        }
        unit_positions = controller.generate_ai_unit_positions(game_id, player_id, unit_counts)

        ai = controller.ai_manager.get_ai(game_id, player_id)
        ai_location: Location = ai.get_location()
        bounds_country = ai_location.bounds_country[ai.get_country()]

        position = [
            (bounds_country["NE"].x + bounds_country["SW"].x) / 2,
            (bounds_country["NE"].y + bounds_country["SW"].y) / 2,
        ]
        expected_country = "NATO"
        self.assertEqual(
            json.loads(unit_positions),
            {
                "data":
                    [
                        {
                            "commandName": "create_units",
                            "arguments": {
                                "unit_data": [
                                    {
                                        "country": expected_country,
                                        "troopType": "tank",
                                        "position": position,
                                        "troopSize": "regiment",
                                    },
                                    {
                                        "country": expected_country,
                                        "troopType": "landbase",
                                        "position": position,
                                        "troopSize": "tactic",
                                    }
                                ]
                            }
                        }
                    ]
            }
        )

    @staticmethod
    def generate_test_game_state() -> Json:
        no_position: float = -1.0
        return dict(troopAmount=4845.311937490126, organization=176.8321739928711, enemyTroopAmount=5132.199632267703,
                    enemyOrganization=165.1185164218997, experience=0.9810055016136355, overlap=176.8321739928711,
                    speed=4,
                    ownUnitToSectors=[[[], [], [], []], [[], [], [], []], [[], [], [], [
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1,
                         '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                         'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []},
                         '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None},
                         'userId': 91,
                         'id': 8, 'latlng': [37.56, 25.06], 'lastPos': [37.56, 25.06], 'type': 'motorized',
                         'resources': {'ammo': 24.243755544823376}, 'size': 'regiment', 'country': 'NATO',
                         'radius': 2.9906532546823343,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0,
                                         'radius': 3,
                                         'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                              'quantity': 30}, 'APC': 101},
                                         'officiers': 40, 'organization': 50, 'defence': 0,
                                         'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                         'discipline': 50, 'experience': 0, 'organization': 44.47337771027072,
                         'composition': {'man': 1798.6730006640225,
                                         'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 26.617236781087744},
                                         'APC': 99.99639640875537}, '_power': 100, 'defence': 0.1914359075108079,
                         'lastMove': False, 'overlap': 0, 'order': 0, 'name': 15, 'lastbattle': 0, 'densityFire': 0,
                         '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                         'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1,
                         '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                         'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []},
                         '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None},
                         'userId': 91,
                         'id': 9, 'latlng': [37.62, 25.12], 'lastPos': [37.62, 25.12], 'type': 'motorized',
                         'resources': {'ammo': 26.025196196798323}, 'size': 'regiment', 'country': 'NATO',
                         'radius': 2.476056460109017,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0,
                                         'radius': 3,
                                         'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                              'quantity': 30}, 'APC': 101},
                                         'officiers': 40, 'organization': 50, 'defence': 0,
                                         'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                         'discipline': 50, 'experience': 0, 'organization': 44.95764464864862,
                         'composition': {'man': 1265.440343006054,
                                         'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 29.100536710307292},
                                         'APC': 80.6602610387528}, '_power': 100, 'defence': 0.19731156416904871,
                         'lastMove': False, 'overlap': 0, 'order': 0, 'name': 16, 'lastbattle': 0, 'densityFire': 0,
                         '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                         'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1,
                         '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                         'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []},
                         '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None},
                         'userId': 91,
                         'id': 10, 'latlng': [37.68, 25.18], 'lastPos': [37.68, 25.18], 'type': 'motorized',
                         'resources': {'ammo': 29.42825887224712}, 'size': 'regiment', 'country': 'NATO',
                         'radius': 2.489341864887328,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0,
                                         'radius': 3,
                                         'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                              'quantity': 30}, 'APC': 101},
                                         'officiers': 40, 'organization': 50, 'defence': 0,
                                         'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                         'discipline': 50, 'experience': 0, 'organization': 42.59631096635641,
                         'composition': {'man': 1297.2550157681744,
                                         'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 29.23198043898356},
                                         'APC': 93.40231011846842}, '_power': 100, 'defence': 0.18225115723768298,
                         'lastMove': False, 'overlap': 0, 'order': 0, 'name': 17, 'lastbattle': 0, 'densityFire': 0,
                         '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                         'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1,
                         '_status': 1,
                         'transportComponent': {'passengerAmount': 0, 'passengerCount': 0, 'passengers': []},
                         'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                           'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                         'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91, 'id': 6,
                         'latlng': [37.5, 25], 'lastPos': [37.5, 25], 'type': 'landbase',
                         'resources': {'ammo': 115.08917479870753}, 'size': 'tactic', 'country': 'NATO',
                         'radius': 0.9666840193623158,
                         'ownTypeData': {'composition': {'man': 160, 'APC': 10}, 'resources': {'ammo': 50},
                                         'speed': [10, 20],
                                         'discipline': 65, 'experience': 1, 'radius': 1, 'organization': 50},
                         'discipline': 65,
                         'experience': 0.9810055016136355, 'organization': 44.80484066759536,
                         'composition': {'man': 115.88263891916306, 'APC': 9.052217636357287}, '_power': 100,
                         'defence': 0.8805340142401492, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 12,
                         'lastbattle': 0, 'densityFire': 0, '_speed': 10, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                         'updateCity': 0, 'isShow': 0, 'baseId': None}]], [[], [], [], []]
                                      ],
                    enemyUnitToSectors=[[[], [], [], []], [[], [], [], []], [[], [
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1, '_status': 1,
                         'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                           'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                         'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 55, 'id': 3,
                         'latlng': [12.56, 25.06], 'lastPos': [12.56, 25.06], 'type': 'motorized',
                         'resources': {'ammo': 28.269373979076274}, 'size': 'regiment', 'country': 'Russia',
                         'radius': 2.4092305802102656,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0, 'radius': 3, 'composition': {'man': 1800,
                                                                                       'IFV': {'country': 'Russia',
                                                                                               'year': '1986',
                                                                                               'quantity': 30},
                                                                                       'APC': 101}, 'officiers': 40,
                                         'organization': 50, 'defence': 0, 'subunits': {'tank': 1, 'artillery': 1},
                                         'icon': {}, 'icon_revert': {}}, 'discipline': 50, 'experience': 0,
                         'organization': 38.616287210844334, 'composition': {'man': 1467.4902569187805,
                                                                             'IFV': {'country': 'Russia',
                                                                                     'year': '1986',
                                                                                     'quantity': 22.006397329269483},
                                                                             'APC': 72.66416830616976}, '_power': 100,
                         'defence': 0.17306952567148354, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 7,
                         'lastbattle': 0, 'densityFire': 0, '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                         'updateCity': 0, 'isShow': 0, 'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1, '_status': 1,
                         'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                           'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                         'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 55, 'id': 4,
                         'latlng': [12.62, 25.12], 'lastPos': [12.62, 25.12], 'type': 'motorized',
                         'resources': {'ammo': 27.197412632507444}, 'size': 'regiment', 'country': 'Russia',
                         'radius': 2.5644243583280257,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0, 'radius': 3, 'composition': {'man': 1800,
                                                                                       'IFV': {'country': 'Russia',
                                                                                               'year': '1986',
                                                                                               'quantity': 30},
                                                                                       'APC': 101}, 'officiers': 40,
                                         'organization': 50, 'defence': 0, 'subunits': {'tank': 1, 'artillery': 1},
                                         'icon': {}, 'icon_revert': {}}, 'discipline': 50, 'experience': 0,
                         'organization': 39.49982098619377, 'composition': {'man': 1748.6084406364876,
                                                                            'IFV': {'country': 'Russia', 'year': '1986',
                                                                                    'quantity': 28.020787118683256},
                                                                            'APC': 90.54575335574984}, '_power': 100,
                         'defence': 0.16475340452254456, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 9,
                         'lastbattle': 0, 'densityFire': 0, '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                         'updateCity': 0, 'isShow': 0, 'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1, '_status': 1,
                         'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                           'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                         'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 55, 'id': 5,
                         'latlng': [12.68, 25.18], 'lastPos': [12.68, 25.18], 'type': 'motorized',
                         'resources': {'ammo': 24.261246173030504}, 'size': 'regiment', 'country': 'Russia',
                         'radius': 2.444770168268014,
                         'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50,
                                         'experience': 0, 'radius': 3, 'composition': {'man': 1800,
                                                                                       'IFV': {'country': 'Russia',
                                                                                               'year': '1986',
                                                                                               'quantity': 30},
                                                                                       'APC': 101}, 'officiers': 40,
                                         'organization': 50, 'defence': 0, 'subunits': {'tank': 1, 'artillery': 1},
                                         'icon': {}, 'icon_revert': {}}, 'discipline': 50, 'experience': 0,
                         'organization': 47.1018568203978, 'composition': {'man': 1434.6573559680874,
                                                                           'IFV': {'country': 'Russia', 'year': '1986',
                                                                                   'quantity': 29.01169586148989},
                                                                           'APC': 96.5014313824636}, '_power': 100,
                         'defence': 0.20695414261380213, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 10,
                         'lastbattle': 0, 'densityFire': 0, '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                         'updateCity': 0, 'isShow': 0, 'baseId': None},
                        {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                         'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False,
                         'priority': 1, '_status': 1,
                         'transportComponent': {'passengerAmount': 0, 'passengerCount': 0, 'passengers': []},
                         'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                           'targetTrainLatlng': None},
                         'trainInfo': {'trainLoaded': False, 'passengerId': None},
                         'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                         'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 55, 'id': 1,
                         'latlng': [12.5, 25], 'lastPos': [12.5, 25], 'type': 'landbase',
                         'resources': {'ammo': 48.35544199008181}, 'size': 'tactic', 'country': 'Russia',
                         'radius': 0.7517300701015505,
                         'ownTypeData': {'composition': {'man': 160, 'APC': 10}, 'resources': {'ammo': 50},
                                         'speed': [10, 20], 'discipline': 65, 'experience': 1, 'radius': 1,
                                         'organization': 50}, 'discipline': 65, 'experience': 0.9931982810883202,
                         'organization': 39.9005514044638,
                         'composition': {'man': 133.6452716203122, 'APC': 9.048073770208857}, '_power': 100,
                         'defence': 0.8132418058730279, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 3,
                         'lastbattle': 0, 'densityFire': 0, '_speed': 10, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                         'updateCity': 0, 'isShow': 0, 'baseId': None}], [], []], [[], [], [], []]],
                    ownSumInfo=[[no_position, no_position, no_position, no_position], [no_position, no_position, no_position, no_position],
                                [no_position, no_position, no_position, 0.04072935059634568], [no_position, no_position, no_position, no_position]],
                    ownMaxInfo=[[no_position, no_position, no_position, no_position], [no_position, no_position, no_position, no_position],
                                [no_position, no_position, no_position, 0.02036467529817284], [no_position, no_position, no_position, no_position]],
                    enemySumInfo=[[no_position, no_position, no_position, no_position], [no_position, no_position, no_position, no_position],
                                  [no_position, 0.04072935059634536, no_position, no_position], [no_position, no_position, no_position, no_position]],
                    enemyMaxInfo=[[no_position, no_position, no_position, no_position], [no_position, no_position, no_position, no_position],
                                  [no_position, 0.020364675298172683, no_position, no_position], [no_position, no_position, no_position, no_position]],
                    loserId=None, status='PROGESS', units={'ownUnits': {
                'regiments': [
                    {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                     'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False, 'priority': 1,
                     '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                     'targetTrainLatlng': None},
                     'trainInfo': {'trainLoaded': False, 'passengerId': None}, 'supplyTask': {'state': 0, 'value': []},
                     '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91,
                     'id': 8, 'latlng': [37.56, 25.06], 'lastPos': [37.56, 25.06], 'type': 'motorized',
                     'resources': {'ammo': 24.243755544823376}, 'size': 'regiment', 'country': 'NATO',
                     'radius': 3.010528697451041,
                     'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50, 'experience': 0,
                                     'radius': 3,
                                     'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                          'quantity': 30}, 'APC': 101},
                                     'officiers': 40, 'organization': 50, 'defence': 0,
                                     'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                     'discipline': 50, 'experience': 0, 'organization': 44.5105944164901,
                     'composition': {'man': 1798.6730006640225,
                                     'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 26.617236781087744},
                                     'APC': 99.99639640875537}, '_power': 100, 'defence': 0.28403687465987165,
                     'lastMove': False, 'overlap': 0, 'order': 0, 'name': 15, 'lastbattle': 0, 'densityFire': 0,
                     '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                     'baseId': None},
                    {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                     'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False, 'priority': 1,
                     '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                     'targetTrainLatlng': None},
                     'trainInfo': {'trainLoaded': False, 'passengerId': None}, 'supplyTask': {'state': 0, 'value': []},
                     '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91,
                     'id': 9, 'latlng': [37.62, 25.12], 'lastPos': [37.62, 25.12], 'type': 'motorized',
                     'resources': {'ammo': 26.025196196798323}, 'size': 'regiment', 'country': 'NATO',
                     'radius': 2.467602312358493,
                     'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50, 'experience': 0,
                                     'radius': 3,
                                     'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                          'quantity': 30}, 'APC': 101},
                                     'officiers': 40, 'organization': 50, 'defence': 0,
                                     'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                     'discipline': 50, 'experience': 0, 'organization': 44.99438551685143,
                     'composition': {'man': 1265.440343006054,
                                     'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 29.100536710307292},
                                     'APC': 80.6602610387528}, '_power': 100, 'defence': 0.29905667748482284,
                     'lastMove': False, 'overlap': 0, 'order': 0, 'name': 16, 'lastbattle': 0, 'densityFire': 0,
                     '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                     'baseId': None},
                    {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                     'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False, 'priority': 1,
                     '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                     'targetTrainLatlng': None},
                     'trainInfo': {'trainLoaded': False, 'passengerId': None}, 'supplyTask': {'state': 0, 'value': []},
                     '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91,
                     'id': 10, 'latlng': [37.68, 25.18], 'lastPos': [37.68, 25.18], 'type': 'motorized',
                     'resources': {'ammo': 29.42825887224712}, 'size': 'regiment', 'country': 'NATO',
                     'radius': 2.564251106785362,
                     'ownTypeData': {'resources': {'ammo': 30}, 'speed': [30, 75], 'discipline': 50, 'experience': 0,
                                     'radius': 3,
                                     'composition': {'man': 1800, 'IFV': {'country': 'Russia', 'year': '1986',
                                                                          'quantity': 30}, 'APC': 101},
                                     'officiers': 40, 'organization': 50, 'defence': 0,
                                     'subunits': {'tank': 1, 'artillery': 1}, 'icon': {}, 'icon_revert': {}},
                     'discipline': 50, 'experience': 0, 'organization': 42.65051742100785,
                     'composition': {'man': 1297.2550157681744,
                                     'IFV': {'country': 'Russia', 'year': '1986', 'quantity': 29.23198043898356},
                                     'APC': 93.40231011846842}, '_power': 100, 'defence': 0.27689323843346414,
                     'lastMove': False, 'overlap': 0, 'order': 0, 'name': 17, 'lastbattle': 0, 'densityFire': 0,
                     '_speed': 30, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0, 'isShow': 0,
                     'baseId': None}],
                'bases': [
                    {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                     'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False, 'priority': 1,
                     '_status': 1, 'transportComponent': {'passengerAmount': 0, 'passengerCount': 0, 'passengers': []},
                     'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                       'targetTrainLatlng': None},
                     'trainInfo': {'trainLoaded': False, 'passengerId': None},
                     'supplyTask': {'state': 0, 'value': []}, '_sector': -1,
                     'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91, 'id': 6,
                     'latlng': [37.5, 25], 'lastPos': [37.5, 25], 'type': 'landbase',
                     'resources': {'ammo': 115.08917479870753}, 'size': 'tactic', 'country': 'NATO',
                     'radius': 0.9666840193623158,
                     'ownTypeData': {'composition': {'man': 160, 'APC': 10}, 'resources': {'ammo': 50},
                                     'speed': [10, 20],
                                     'discipline': 65, 'experience': 1, 'radius': 1, 'organization': 50},
                     'discipline': 65,
                     'experience': 0.9810055016136355, 'organization': 44.85902803975568,
                     'composition': {'man': 115.88263891916306, 'APC': 9.052217636357287}, '_power': 100,
                     'defence': 1.2939374156743861, 'lastMove': False, 'overlap': 0, 'order': 0, 'name': 12,
                     'lastbattle': 0, 'densityFire': 0, '_speed': 10, 'startTime': 0, 'notShoot': 0, 'distance': 0,
                     'updateCity': 0, 'isShow': 0, 'baseId': None}],
                'supports': [
                    {'MOVE': False, 'STOP': False, 'OWN': True, 'lastElevation': 0, 'elevation': 0, 'battle': False,
                     'enemyCount': 0, 'weather': None, 'visible': True, 'died': False, 'lastdied': False, 'priority': 1,
                     '_status': 1, 'passengerInfo': {'goToTrain': False, 'inTrain': False, 'targetTrainID': None,
                                                     'targetTrainLatlng': None},
                     'trainInfo': {'trainLoaded': False, 'passengerId': None}, 'supplyTask': {'state': 0, 'value': []},
                     '_sector': -1, 'pathInfo': {'state': 0, 'value': None, 'currentPointIndex': None}, 'userId': 91,
                     'id': 7, 'latlng': [37.5, 25], 'lastPos': [37.5, 25], 'type': 'truck',
                     'resources': {'fuel': 55.78941774232346, 'food': None}, 'size': 'regiment', 'country': 'NATO',
                     'radius': 1.4342241590874214,
                     'ownTypeData': {'resources': {'fuel': 60, 'food': 50}, 'speed': [50, 80], 'discipline': 55,
                                     'radius': 2, 'composition': {'man': 100}, 'organization': 50, 'icon': {},
                                     'icon_revert': {}}, 'discipline': 55, 'experience': None,
                     'organization': 45.96304062451917, 'composition': {'man': 94.09978982757941}, '_power': 100,
                     'defence': 0, 'lastMove': True, 'overlap': 0, 'order': 0, 'name': 13, 'lastbattle': 0,
                     'densityFire': 0, '_speed': 50, 'startTime': 0, 'notShoot': 0, 'distance': 0, 'updateCity': 0,
                     'isShow': 0, 'baseId': None}]
            },
                'visibleEnemyUnits': {'regiments': [], 'bases': [], 'supports': []}
            },
                    currentGameTime='2014-06-30T21:00:00.000Z',
                    currentTime=156,
                    graphDensity=[
                        [1, 3, 2, 1],
                        [1, 3, 1, 1],
                        [1, 3, 4, 2],
                        [1, 1, 3, 1],
                    ],
                    ownUnitAmount=4,
                    enemyUnitAmount=3,
                    ownUnitCompositionAmount=10,
                    enemyUnitCompositionAmount=11,
                    ownUnitOrganizationAmount=12,
                    enemyUnitOrganizationAmount=13,
        )


class TestScoutNetwork(asynctest.TestCase):
    def setUp(self):
        self.game_id = "3"
        self.player_id = "31"
        self.country = "NATO"
        self.input_data = {
            "game_id": self.game_id,
            "player_id": self.player_id,
            "ai_type": "neuron-network",
            "ai_address": "scout-layer",
            "location": TestRouteController.generate_mock_location_info(),
            "country": self.country,
            "gameState": TestRouteController.generate_test_game_state(),
            "ai_options": {"troopType": "motorized", "isTrain": True}
        }
        self._game_info = GameInfo(int(self.game_id), int(self.player_id))
        self.controller = RouteController()

    def test_life_circle_network(self):

        self.controller.create_ai(self.input_data)
        commands: Json = self.controller.update_ai(
            TestRouteController.generate_test_game_state(),
            self._game_info
        )
        self.controller.delete_ai(self._game_info)
        with self.assertRaises(Exception):
            var = self.controller.ai_manager.get_ai(self.game_id, self.player_id)
        with self.assertRaises(Exception):
            var = self.controller.ai_manager.get_ai_socket_connection_info(self.game_id, self.player_id)


if __name__ == '__main__':
    asynctest.main()
