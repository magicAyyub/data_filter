from src.dataManagement.data import Data
from typing import Any, Callable, List


class Filter:
    @staticmethod
    def filter_by_string_lexicographical(data_list: List[Data], key: str, value: str) -> List[Data]:
        return [data.value() for data in data_list if data.get(key, "") == value]

    @staticmethod
    def filter_by_string_contains(data_list: List[Data], key: str, substring: str) -> List[Data]:
        return [data.value() for data in data_list if substring in data.get(key, "")]

    @staticmethod
    def filter_by_string_starts_with(data_list: List[Data], key: str, prefix: str) -> List[Data]:
        return [data.value() for data in data_list if data.get(key, "").startswith(prefix)]

    @staticmethod
    def filter_by_string_ends_with(data_list: List[Data], key: str, suffix: str) -> List[Data]:
        return [data.value() for data in data_list if data.get(key, "").endswith(suffix)]

    @staticmethod
    def filter_by_list_all_elements(data_list: List[Data], key: str, element: Any) -> List[Data]:
        return [data.value() for data in data_list if element in data.get(key, [])]

    @staticmethod
    def filter_by_list_min(data_list: List[Data], key: str, min_value: Any) -> List[Data]:
        return [data.value() for data in data_list if min(data.get(key, [])) >= min_value]

    @staticmethod
    def filter_by_list_max(data_list: List[Data], key: str, max_value: Any) -> List[Data]:
        return [data.value() for data in data_list if max(data.get(key, [])) <= max_value]

    @staticmethod
    def filter_by_list_average(data_list: List[Data], key: str, average_condition: Callable[[Any], bool]) -> List[Data]:
        values = [data.get(key, []) for data in data_list]
        return [data.value() for data in data_list if average_condition(values)]

    @staticmethod
    def compare_fields(data_list: List[Data], field1: str, field2: str) -> List[Data]:
        return [data.value() for data in data_list if data.get(field1, "") == data.get(field2, "")]

    @staticmethod
    def filter_by_global_statistics(data_list: List[Data], key: str, condition: Callable[[Any], bool]) -> List[Data]:
        values = [data.get(key) for data in data_list]
        return [data.value() for data in data_list if condition(values)]

    @staticmethod
    def filter_by_combined_fields(data_list: List[Data], field1: str, field2: str, threshold: Any) -> List[Data]:
        return [data.value() for data in data_list if data.get(field1, 1) * data.get(field2, 1) > threshold]
