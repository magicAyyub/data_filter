class Data:
    """Représente une seule entrée de donnée"""
    
    def __init__(self, data_dict:dict) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        self.data = data_dict
    
    
    
    def value(self) -> dict:
        """Retourne la classe sous forme de dictionnaire """
        
        return self.data
    
    def get(self, key, default):
        """ Retourne la valeur d'un champ"""
        
        return getattr(self,key,default)