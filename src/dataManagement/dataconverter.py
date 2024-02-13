import json
import xml.etree.ElementTree as ET

class DataConverter:
    """Classe contenant des méthodes pour convertir des données en différents formats."""
    
    @staticmethod
    def convert_csv_value(value:str) -> any:
        """Converti les valeurs CSV (Par défaut sous forme de chaîne de caractère) en leur type de données approprié."""
        
        try:
            json_data = json.loads(value)
            return DataConverter.convert_json(json_data)
        except (json.JSONDecodeError, TypeError):
            return value

    @staticmethod
    def convert_json(json_data: any) -> any:
        """Converti les valeurs en chaîne de caractères en leur type de données approprié."""
        
        if isinstance(json_data, list):
            return [DataConverter.convert_json(item) for item in json_data]
        elif isinstance(json_data, dict):
            return {key: DataConverter.convert_json(value) for key, value in json_data.items()}
        elif isinstance(json_data, (int, float, str, bool, type(None))):
            return json_data
        else:
            return str(json_data)

    @staticmethod
    def convert_xml_value(element:ET.Element) -> any:
        """Converti les valeurs XML (Par défaut sous forme de chaîne de caractère) en leur type de données approprié."""
        
        if len(element) > 0:
            return {child.tag.split('}')[-1]: DataConverter.convert_xml_value(child) for child in element}
        else:
            return DataConverter.convert_text(element.text)

    @staticmethod
    def convert_text(text:str) -> any:
        """Converti les valeurs en chaîne de caractères en leur type de données approprié."""
        
        if text.isdigit():
            return int(text)
        try:
            return float(text)
        except ValueError:
            if text.lower() == 'true':
                return True
            elif text.lower() == 'false':
                return False
            return text
    
    @staticmethod   
    def list_to_string(data_array:list) -> str:
        """Transforme une liste en une version lisible sous forme de chaîne de caractères"""
        
        data_string = "| "
        data_string += ' '.join([str(elem) for elem in data_array])
        return data_string