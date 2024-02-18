class Data:
    """Représente une seule entrée de donnée"""
    
    def __init__(self, data_dict:dict) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        self.data = data_dict
    
    
    
    def to_dict(self) -> dict:
        """Retourne la classe sous forme de dictionnaire """
        
        return self.data

    def get_fields(self) -> list:
        """Retourne la liste des champs de la classe"""
        
        return list(self.data.keys())
    
    def get_field_value(self, key:str, default: any) -> any:
        """ Retourne la valeur d'un champ"""
        
        return getattr(self,key,default)
    