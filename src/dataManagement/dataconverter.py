import json
import xml.etree.ElementTree as ET

class DataConverter:
    @staticmethod
    def convert_csv_value(value):
        try:
            json_data = json.loads(value)
            return DataConverter.convert_json(json_data)
        except (json.JSONDecodeError, TypeError):
            return value

    @staticmethod
    def convert_json(json_data):
        if isinstance(json_data, list):
            return [DataConverter.convert_json(item) for item in json_data]
        elif isinstance(json_data, dict):
            return {key: DataConverter.convert_json(value) for key, value in json_data.items()}
        elif isinstance(json_data, (int, float, str, bool, type(None))):
            return json_data
        else:
            return str(json_data)

    @staticmethod
    def convert_xml_value(element):
        if len(element) > 0:
            return {child.tag.split('}')[-1]: DataConverter.convert_xml_value(child) for child in element}
        else:
            return DataConverter.convert_text(element.text)

    @staticmethod
    def convert_text(text):
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
    def list_to_string(data_array:list):
        data_string = "| "
        data_string += ' '.join([str(elem) for elem in data_array])
        return data_string