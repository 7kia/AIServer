import requests


class ScoutLayerTrainer:
    @classmethod
    def generate_request_string(cls) -> str:
        return cls._generate_server_address() \
           + "/game-for-layer" \
           + cls._generate_query(
                "ScoutLayer", "motorized",
                16, 4
            )

    # TODO 7kia возможно нужно будет поменять адрес для защиты
    @classmethod
    def _generate_server_address(cls) -> str:
        return "http://localhost:8000"

    @classmethod
    def _generate_query(cls,
                        layer_name: str, troop_type: str,
                        node_amount: int, distance_between_nodes: float
                        ) -> str:
        return f"layerName={layer_name}" \
               f"&troopType={troop_type}" \
               f"&nodeAmount={node_amount}" \
               f"&distanceBetweenNodes={distance_between_nodes}"


if __name__ == '__main__':
    trainer = ScoutLayerTrainer()
    request_string: str = trainer.generate_request_string()
    res = requests.get(request_string)
