from typing import List, Union, Dict
from src.dataManagement.data import Data

class Stats:
    @staticmethod
    def generate_stats(data_list: List[Data]) -> Dict[str, Dict[str, Union[float, int, str, Dict[str, float]]]]:
        """Génère des statistiques pour l'ensemble des champs de la liste de données."""
        
        if not data_list:
            return {}

        stats = {}

        for field_name in data_list[0].to_dict().keys():
            field_type = type(data_list[0].get_field_value(field_name, None)) 

            if field_type in [int, float]:
                stats[field_name] = Stats.generate_number_stats(data_list, field_name)
            elif field_type == bool:
                stats[field_name] = Stats.generate_boolean_stats(data_list, field_name)
            elif field_type == list:
                stats[field_name] = Stats.generate_list_stats(data_list, field_name)
            else: # On rajoutera des statistiques ici au besoin 
                pass

        return stats

    @staticmethod
    def generate_number_stats(data_list: List[Data], field_name: str) -> Dict[str, Union[float, int, str]]:
        """Génère des statistiques pour un champ numérique spécifique."""
        
        
        values = [data.get_field_value(field_name, 0) for data in data_list]

        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
        }

    @staticmethod
    def generate_boolean_stats(data_list: List[Data], field_name: str) -> Dict[str, float]:
        """Génère des statistiques pour un champ booléen spécifique."""
        
        values = [data.get_field_value(field_name, False) for data in data_list]

        true_percentage = (values.count(True) / len(values)) * 100
        false_percentage = (values.count(False) / len(values)) * 100

        return {
            'true_percentage': true_percentage,
            'false_percentage': false_percentage,
        }

    @staticmethod
    def generate_list_stats(data_list: List[Data], field_name: str) -> Dict[str, Union[float, int, str]]:
        """Génère des statistiques pour un champ représentant une liste."""
        
        list_lengths = [len(data.get_field_value(field_name, [])) for data in data_list]

        return {
            'min_len': min(list_lengths),
            'max_len': max(list_lengths),
            'avg_len': sum(list_lengths) / len(list_lengths),
        }
