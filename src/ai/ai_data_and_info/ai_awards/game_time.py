class GameTime:
    def __init__(self):
        self._string_presentation: str = ""

    def get_string_presentation(self) -> str:
        return self._string_presentation

    def set_string_presentation(self, value: str):
        self._string_presentation = value

    def get_different_as_string(self, current_time) -> str:
        if self._represents_int(current_time.get_string_presentation()):
            return str(int(current_time.get_string_presentation()) - int(self._string_presentation))
        # TODO 7kia Date не парсится
        return current_time.get_string_presentation() + " - " + self._string_presentation

    def get_different_as_float(self, current_time: str) -> float:
        if self._represents_int(current_time):
            return float(current_time) - float(self._string_presentation)
        raise IOError("Class GameTime: Date type not parse")

    def get_as_float(self) -> float:
        return float(self._string_presentation)

    @staticmethod
    def _represents_int(number: str):
        try:
            int(number)
            return True
        except ValueError:
            return False
