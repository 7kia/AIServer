from src.ai.position import Position
from src.game_data_extractor import Json
from src.location import Location


# TODO 7kia протестировать класс
class LocationBuilder:
    @staticmethod
    def build(json: Json) -> Location:
        location: Location = Location()
        location.id = json["id"]
        location.name = json["name"]
        location.countries = json["countries"]

        bounds: dict = json["bounds"]
        location.bounds = {
            "NE": Position(bounds["NE"][0], bounds["NE"][1]),
            "SW": Position(bounds["SW"][0], bounds["SW"][1])
        }

        location.bounds_country = {}
        for key in json["boundsCountry"].keys():
            country_data: dict = json["boundsCountry"][key]
            location.bounds_country[key] = {
                "NE": Position(country_data["NE"][0], country_data["NE"][1]),
                "SW": Position(country_data["SW"][0], country_data["SW"][1])
            }

        location.resources = json["resources"]
        # TODO 7kia не удаляй, потом может пригодится
        # for key in json["resources"].keys():
        #     country_data: dict = json["resources"][key]
        #     location.bounds_country[key] = country_data
        location.units = json["units"]
        location.weapons = json["weapons"]

        return location
