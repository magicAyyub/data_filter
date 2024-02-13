from src.dataManagement.data import Data
from typing import Any, Callable, List

class Sorter:
    """Classe contenant des méthodes pour trier des données en fonction de différents critères."""
    
    
    @staticmethod
    def sort_by_field(data_list: List[Data], key: str, reverse: bool = False) -> List[Data]:
        """Trie les données en fonction d'un champ spécifique."""
        
        return sorted(data_list, key=lambda x: getattr(x, key), reverse=reverse)

    @staticmethod
    def sort_by_multiple_fields(data_list: List[Data], keys: List[str]) -> List[Data]:
        """Trie les données sur la base de plusieurs champs."""
        
        return sorted(data_list, key=lambda x: tuple(getattr(x, key) for key in keys))

    @staticmethod
    def sort_by_global_value(data_list: List[Data], key: str, value_function: Callable[[Any], Any], reverse: bool = False) -> List[Data]:
        """Trie les données sur la base d'une valeur globale calculée à l'aide d'une fonction personnalisée."""
        
        return sorted(data_list, key=lambda x: value_function(getattr(x, key)), reverse=reverse)

    @staticmethod
    def sort_by_priority_criteria(data_list: List[Data], criteria: List[Callable[[Data], Any]]) -> List[Data]:
        """Trie les données en fonction de plusieurs critères avec priorité."""
        
        return sorted(data_list, key=lambda x: [c(x) for c in criteria])
