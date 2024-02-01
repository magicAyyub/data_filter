import csv
import json
import xml.etree.ElementTree as ET
import yaml
from src.dataManagement.data import Data
from src.dataManagement.dataconverter import DataConverter
from  src.customException.save_exception import EmptyDataListError


class DataSet:
    """Représente un ensemble de donnée ansi que le traitement à effectuer sur ces derniers"""
    
    def __init__(self) -> None:
        self.data_list = []
     
     
        
    def add_data(self, data:Data) -> None:
        """Rajoute une donnée dans l'ensemble de donnée"""
        
        self.data_list.append(data)
    
    def all_to_dict(self) -> list:
        """Converti et retourne la liste des classes Data sous forme de dictionnaire."""
        
        return [data.get() for data in self.data_list]
     
    
    def load_csv(self, file_path: str) -> None:
        """Charge des données depuis un fichier CSV"""
        
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_dict = {key: DataConverter.convert_csv_value(value) for key, value in row.items()}
                    self.add_data(Data(data_dict))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")
      
      
        
    def save_csv(self, file_path:str) -> None:
        """Sauvegarde des données dans un fichier CSV"""
        
        if len(self.data_list) > 0:
            with open(file_path, 'w', newline='') as file:
                fieldnames = self.all_to_dict()[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.all_to_dict())
        else:
            raise EmptyDataListError()



    def load_json(self, file_path:str) -> None:
        """charge des données depuis un fichier JSON"""
        
        try:
            with open(file_path, 'r') as file:
                for dict_data in json.load(file):
                    self.add_data(Data(dict_data))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")



    def save_json(self, file_path:str) -> None:
        """Sauvegarde des données dans un fichier JSON"""
        
        if len(self.data_list) > 0:     
            with open(file_path, 'w') as file:
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
            



    def save_xml(self, file_path:str) -> None:
        """Sauvegarde des données dans un fichier XML"""
        
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
            with open(file_path, 'r') as file:
                for dict_data in  yaml.safe_load(file):
                    self.add_data(Data(dict_data))
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun fichier ne correspond à \"{file_path}\"")
      
        
    def save_yaml(self, file_path:str) -> None:
        """Sauvegarder des données dans un fichier YAML"""
        
        if len(self.data_list) > 0:      
            with open(file_path, 'w') as file:
                yaml.dump(self.all_to_dict(), file)      
        else:
            raise EmptyDataListError()
