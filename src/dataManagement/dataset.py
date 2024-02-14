import csv
import json
import xml.etree.ElementTree as ET
import yaml
from typing import Any, Callable, List, Dict,Union
from src.dataManagement.data import Data
from src.dataManagement.dataconverter import DataConverter
from  src.customException.save_exception import EmptyDataListError
from src.operations.stat import Stats


class DataSet:
    """Représente un ensemble de donnée ansi que le traitement à effectuer sur ces derniers"""
    
    def __init__(self) -> None:
        self.data_source_folder = "src/dataSources/"
        self.data_list = []
    
    def __str__(self) -> str:
        
        data_array = list(map(lambda data: [f"{elmt} |" for elmt in data.to_dict().values()],self.data_list))      
        data_string = ""
        for element in data_array:
            if isinstance(element,list):
                data_string += DataConverter.list_to_string(element)+"\n"
            else:
                data_string += str(element)+"\n" 
        return data_string
                
    def add_data(self, data:Data) -> None:
        """Rajoute une donnée dans l'ensemble de donnée"""
        
        self.data_list.append(data)
    
    def all_to_dict(self) -> list:
        """Converti et retourne la liste des classes Data sous forme de dictionnaire."""
        
        return [data.to_dict() for data in self.data_list]
    
    def get_by_id(self, id:int) -> Data:
        """Récupère une donnée par son identifiant"""
        
        if self.data_list[id]:
            return self.data_list[id]
        return None
     
    
    def load_csv(self, file_path: str) -> None:
        """Charge des données depuis un fichier CSV"""
        
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_dict = {key: DataConverter.convert_csv_value(value) for key, value in row.items()}
                    self.add_data(Data(data_dict))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")
      
      
        
    def save_csv(self, file_path:str, data_list = None) -> None:
        """Sauvegarde des données dans un fichier CSV"""
        
        if data_list:
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                fieldnames = data_list[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
        else:
            if len(self.data_list) > 0:
                with open(file_path, 'w',encoding='utf-8', newline='') as file:
                    fieldnames = self.all_to_dict()[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.all_to_dict())
            else:
                raise EmptyDataListError()



    def load_json(self, file_path:str) -> None:
        """charge des données depuis un fichier JSON"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for dict_data in json.load(file):
                    self.add_data(Data(dict_data))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")



    def save_json(self, file_path:str, data_list = None) -> None:
        """Sauvegarde des données dans un fichier JSON"""
        
        if data_list:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data_list, file, indent=2)
        else:     
            if len(self.data_list) > 0:     
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.all_to_dict(), file, indent=2)     
            else:
                raise EmptyDataListError()


    def load_xml(self, file_path: str) -> None:
        """Charge des données depuis un fichier XML"""
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = [{child.tag.split('}')[-1]: DataConverter.convert_xml_value(child) for child in item} for item in root]
            for dict_data in data:
                self.add_data(Data(dict_data))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")
            



    def save_xml(self, file_path:str, data_list = None) -> None:
        """Sauvegarde des données dans un fichier XML"""
        
        if data_list:
            root = ET.Element("dataset")
            for item in data_list:
                sub_element = ET.SubElement(root, "record")
                for key, value in item.items():
                    child = ET.SubElement(sub_element, key)
                    child.text = str(value)
            tree = ET.ElementTree(root)
            tree.write(file_path)
        else:
            if len(self.data_list) > 0:
                root = ET.Element("dataset")
                for item in self.all_to_dict():
                    sub_element = ET.SubElement(root, "record")
                    for key, value in item.items():
                        child = ET.SubElement(sub_element, key)
                        child.text = str(value)
                tree = ET.ElementTree(root)
                tree.write(file_path)
            else:
                raise EmptyDataListError()



    def load_yaml(self, file_path:str) -> None:
        """Charger des données depuis un fichier YAML"""
        
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                for dict_data in  yaml.safe_load(file):
                    self.add_data(Data(dict_data))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")
      
        
    def save_yaml(self, file_path:str, data_list = None) -> None:
        """Sauvegarder des données dans un fichier YAML"""
        
        if data_list:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data_list, file)
        else:
            if len(self.data_list) > 0:      
                with open(file_path, 'w', encoding='utf-8') as file:
                    yaml.dump(self.all_to_dict(), file)      
            else:
                raise EmptyDataListError()
        
    def filter_data(self, filter_method: Callable[[List[Data], Any], List[Data]], *args, **kwargs) -> List[Data]:
        """
        Applique le filtre spécifié sur les données de l'ensemble de données.

        Args:
            filter_method (Callable[[List[Data], Any], List[Data]]): La méthode de filtre à appliquer.
            *args: Les arguments positionnels à passer à la méthode de filtre.
            **kwargs: Les arguments nommés à passer à la méthode de filtre.

        Returns:
            List[Data]: La liste des données filtrées.
        """
        return filter_method(self.data_list, *args, **kwargs)
    
    def sort_data(self, sort_function: Callable[[List[Data]], List[Data]], *args, **kwargs) -> List[Data]:
        """Trie les données dans le DataSet.

        Args:
            sort_function (Callable[[List[Data]], List[Data]]): La méthode de trie à appliquer.
            *args: Liste d'arguments de longueur variable.
            **kwargs: Arguments de mots-clés arbitraires.

        Returns:
            List[Data]: Une liste de données triées.
        """
        sorted_data = sort_function(self.data_list, *args, **kwargs)
        return sorted_data

    def generate_stats(self) -> Dict[str, Dict[str, Union[float, int, Dict[Any, int]]]]:
        """Génère des statistiques pour l'ensemble des champs de la DataSet.

        Returns:
            Dict[str, Dict[str, Union[float, int, Dict[Any, int]]]]: Un dictionnaire contenant les statistiques pour chaque champ.
        """
        return Stats.generate_stats(self.data_list)