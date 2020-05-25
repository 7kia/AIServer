from typing import Dict

from src.ai.game_components.position import Position
from src.ai.game_components.unit import Unit
from src.ai.game_components.unit_state_extractor import UnitStateExtractor

Json = Dict[str, any]


class UnitFactory:
    @staticmethod
    def create_unit(json: Json):
        unit = Unit()
        unit.id = int(json["id"])
        unit.unit_type = str(json["type"])
        unit.state = UnitStateExtractor.extract_state(json)
        unit.position = Position(json["latlng"][0], json["latlng"][1])

        # # this.lastElevation = 0; // предыдущая высота
        # # this.elevation = 0; // высота точки нахождения юнита
        # this.weather
        #
        # died
        # # lastdied
        # # priority
        #
        # transportComponent
        # passengerInfo
        # trainInfo
        # supplyTask
        # pathInfo
        #
        # userId
        # # lastPos
        # # year// зачем
        # # size// batallion / regiment / brigade / division для боевых, tactic / operative / strategic для баз
        # country
        # radius
        #
        # discipline
        # experience
        # organization
        # composition// боевой дух
        # _power
        #
        # defence
        # overlap
        # name
        # # this.lastbattle = 0;//т.к. статус боя ставится и на клиенте и на сервере
        # # this.densityFire = 0;//сколько кг боеприпасов "принял" от противника в раунде боя
        # this._speed = this.ownTypeData.speed[0];//средняя скорость
        #
        # # // TODO(7kia): следующее поле нужно?
        # # this.startTime = 0;//для маршрута в городе по прямой
        # this.notShoot = 0;//юнит не стреляет т.к. большая дистанция или нет боеприпасов
        # # this.distance = 0; // пройденное расстояние юнитом, которое еще не обработал сервер
        # # this.updateCity = 0;//флаг что нужно обновить город на сервере с клиента (при движении на длинную дистанцию сбросить статус города)
        #
        # this.isShow = 0; // TODO(7kia): почему логическая переменная = 0, [censored]?
        # this.baseId = null; // id базы на которой находится юнит
        # TODO 7kia нет полной конвертации юнита
        return unit
