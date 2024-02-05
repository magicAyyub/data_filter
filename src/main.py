from pathlib import Path
import sys

# Récupérer le chemin absolu du script en cours d'exécution
script_path = Path(__file__).resolve()

# Ajouter le chemin du projet au chemin de recherche de Python
project_root = script_path.parent.parent  # Deux niveaux au-dessus pour atteindre le répertoire du projet
sys.path.append(str(project_root))

from  src.dataManagement.dataset import DataSet 
from  src.operations.filter import Filter 
from  src.operations.sorter import Sorter 

def main():
    ds = DataSet()
    
    sorted_data = ds.filter_data(Sorter.sort_by_global_value, "first_name", lambda x: len(x), reverse=True)
    for data in sorted_data:
        print(data.to_dict())
    
if __name__ == '__main__':
    main()
    

 