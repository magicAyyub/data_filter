class UnsupportedFileTypeError(Exception):
    """
    Exception qui se déclenche quand on veut charger des données depuis un fichier qui 
    n'est pas pris en charge.
    """
    def __init__(self, message: str = "Type de fichier non pris en charge"):
        self.message = message
        super().__init__(self.message)