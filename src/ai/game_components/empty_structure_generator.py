from typing import List


class EmptyStructureGenerator:
    @staticmethod
    def generate_list(fill_value: any, x_size: int = 4, y_size: int = 4) -> List[List[any]]:
        result: List[List[any]] = []
        for y in range(y_size):
            new_array: List[any] = []
            for x in range(x_size):
                new_array.append(fill_value)
            result.append(new_array)
        return result
