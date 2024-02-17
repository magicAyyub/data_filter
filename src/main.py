from pathlib import Path
import sys

script_path = Path(__file__).resolve()      # Chemin absolu du script

project_root = script_path.parent.parent    # Remonter de deux niveaux  
sys.path.append(str(project_root))         # Ajouter le chemin du projet au path

#from  src.app.interface2 import Interface2
from src.app.interface import Interface

def main():
   
    """
    # Ma version
    app = Interface2()
    # app.generate_fake_data_sources(30) # Générer des données aléatoires
    app.run()
    """
    
    # Ta version
    app = Interface()
    app.run()
    
if __name__ == '__main__':
    main()