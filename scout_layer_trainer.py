import requests


class ScoutLayerTrainer:
    @classmethod
    def generate_request_string(cls) -> str:
        shoot_amounts: int = 1
        shoots_to_second: int = 25
        time_scale: float = 150.0
        tick_duration = shoot_amounts / shoots_to_second * time_scale
        return cls._generate_server_address() \
               + "/game-for-layer" \
               + "?" \
               + cls._layer_params("ScoutLayer", "motorized") \
               + "&" + cls._model_graph_options(16, 4) \
               + "&" + cls._timer_params(tick_duration)

    @classmethod
    def _generate_server_address(cls) -> str:
        # TODO 7kia возможно нужно будет поменять адрес для защиты
        return "http://localhost:8000"

    @classmethod
    def _layer_params(cls, layer_name: str, troop_type: str) -> str:
        return f"layerName={layer_name}" \
               f"&troopType={troop_type}" \
               f"&isTrain={True}"

    @classmethod
    def _model_graph_options(cls, node_amount: int, distance_between_nodes: float) -> str:
        return f"nodeAmount={node_amount}" \
               f"&distanceBetweenNodes={distance_between_nodes}"

    @classmethod
    def _timer_params(cls, tick_duration: float) -> str:
        return f"tickDuration={tick_duration}"


if __name__ == '__main__':
    trainer = ScoutLayerTrainer()
    request_string: str = trainer.generate_request_string()
    res = requests.get(request_string)
