from pathlib import Path
import sys

script_path = Path(__file__).resolve()      # Chemin absolu du script

project_root = script_path.parent.parent    # Remonter de deux niveaux  
sys.path.append(str(project_root))         # Ajouter le chemin du projet au path

from  src.App.interface import Interface

def main():
   
    app = Interface()
    app.run()
    
if __name__ == '__main__':
    main()