from pathlib import Path
import sys

# Récupérer le chemin absolu du script en cours d'exécution
script_path = Path(__file__).resolve()

# Ajouter le chemin du projet au chemin de recherche de Python
project_root = script_path.parent.parent  # Deux niveaux au-dessus pour atteindre le répertoire du projet
sys.path.append(str(project_root))

from  dataManagement.dataset import DataSet 

def main():
    ds = DataSet()
    print(ds)
    
if __name__ == '__main__':
    main()
    

 