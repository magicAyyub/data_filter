from pathlib import Path
import sys

script_path = Path(__file__).resolve()      # Chemin absolu du script

project_root = script_path.parent.parent    # Remonter de deux niveaux  
sys.path.append(str(project_root))         # Ajouter le chemin du projet au path

from  src.dataManagement.dataset import DataSet 
from  src.operations.filter import Filter 
from  src.operations.sorter import Sorter 

def main():
    ds = DataSet()
    
    print(ds.generate_stats())
    
if __name__ == '__main__':
    main()