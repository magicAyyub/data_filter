from src.dataManagement.data import Data
from typing import Any, Callable, List


class Filter:
    """Classe contenant des méthodes pour filtrer des données en fonction de différents critères."""
    
    @staticmethod
    def filter_by_string_lexicographical(data_list: List[Data], key: str, value: str) -> List[Data]:
        """Filtre les données en fonction d'une comparaison lexicographique d'une valeur de type chaîne de caractères associée à une clé spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, "") == value]

    @staticmethod
    def filter_by_string_contains(data_list: List[Data], key: str, substring: str) -> List[Data]:
        """Filtre les données en fonction de la présence d'une sous-chaîne dans une valeur de type chaîne de caractères associée à une clé spécifique."""
        if substring == "":
            return data_list
        return [data for data in data_list if substring in data.get_field_value(key, "")]

    @staticmethod
    def filter_by_string_starts_with(data_list: List[Data], key: str, prefix: str) -> List[Data]:
        """Filtre les données en fonction du début d'une valeur de type chaîne de caractères associée à une clé spécifique."""
        if prefix == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, "").startswith(prefix)]

    @staticmethod
    def filter_by_string_ends_with(data_list: List[Data], key: str, suffix: str) -> List[Data]:
        """Filtre les données en fonction de la fin d'une valeur de type chaîne de caractères associée à une clé spécifique."""
        if suffix == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, "").endswith(suffix)]

    @staticmethod
    def filter_by_list_all_elements(data_list: List[Data], key: str, element: Any) -> List[Data]:
        """Filtre les données en fonction de la présence de tous les éléments d'une liste associée à une clé spécifique."""
        if element == "":
            return data_list
        return [data for data in data_list if element in data.get_field_value(key, [])]

    @staticmethod
    def filter_by_list_min(data_list: List[Data], key: str, min_value: Any) -> List[Data]:
        """Filtre les données en fonction de la valeur minimale d'une liste associée à une clé spécifique."""
        
        if min_value == "":
            return data_list
        return [data for data in data_list if min(data.get_field_value(key, [])) >= float(min_value)]

    @staticmethod
    def filter_by_list_max(data_list: List[Data], key: str, max_value: Any) -> List[Data]:
        """Filtre les données en fonction de la valeur maximale d'une liste associée à une clé spécifique."""
        if max_value == "":
            return data_list
        return [data for data in data_list if max(data.get_field_value(key, [])) <= float(max_value)]

    @staticmethod
    def filter_by_list_average(data_list: List[Data], key: str, value: Any) -> List[Data]:
        """Filtre les données en fonction d'une condition sur la moyenne des valeurs d'une liste associée à une clé spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if sum(data.get_field_value(key, [])) / len(data.get_field_value(key, [])) >= float(value)]

    @staticmethod
    def compare_fields(data_list: List[Data], field1: str, field2: str) -> List[Data]:
        """Filtre les données en comparant deux champs spécifiques."""
        if field1 == "" or field2 == "":
            return data_list
        return [data for data in data_list if data.get_field_value(field1, "") == data.get_field_value(field2, "")]

    @staticmethod
    def filter_by_global_statistics(data_list: List[Data], key: str, condition: Callable[[Any], bool]) -> List[Data]:
        """Filtre les données en fonction d'une condition sur les statistiques globales d'une liste associée à une clé spécifique."""
        if key == "":
            return data_list
        values = [data.get_field_value(key) for data in data_list]
        return [data for data in data_list if condition(values)]

    @staticmethod
    def filter_by_combined_fields(data_list: List[Data], field1: str, field2: str, threshold: Any) -> List[Data]:
        """Filtre les données en fonction d'une combinaison de deux champs dépassant un seuil spécifique."""
        if field1 == "" or field2 == "":
            return data_list
        return [data for data in data_list if data.get_field_value(field1, 1) * data.get_field_value(field2, 1) > threshold]
    

    @staticmethod
    def filter_by_number_greater_than(data_list: List[Data], key: str, value: Any) -> List[Data]:
        """Filtre les données en fonction d'une valeur numérique supérieure à une valeur spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, 0) > value]
    
    @staticmethod
    def filter_by_number_less_than(data_list: List[Data], key: str, value: Any) -> List[Data]:
        """Filtre les données en fonction d'une valeur numérique inférieure à une valeur spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, 0) < value]
    
    @staticmethod
    def filter_by_number_equal_to(data_list: List[Data], key: str, value: Any) -> List[Data]:
        """Filtre les données en fonction d'une valeur numérique égale à une valeur spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, 0) == value]
    
    @staticmethod
    def filter_by_boolean(data_list: List[Data], key: str, value: bool) -> List[Data]:
        """Filtre les données en fonction d'une valeur booléenne spécifique."""
        if value == "":
            return data_list
        return [data for data in data_list if data.get_field_value(key, False) == value]
