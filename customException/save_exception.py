class EmptyDataListError(Exception):
    """
    Exception qui se déclenche quand on veut sauvegarder des données dans un fichier
    mais que la liste des données est vide.
    """
    
    def __init__(self, message="La liste des données à sauvegarder est vide"):
        self.msg = message
        super().__init__(self.msg)