import os
import sys

from faker import Faker
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from  functools import partial
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QMessageBox,
    QFileDialog
)

from  src.dataManagement.dataset import DataSet 
from src.customException.load_exception import UnsupportedFileTypeError
from  src.customException.save_exception import EmptyDataListError


class Interface2(QMainWindow):
    """Classe représentant l'interface graphique de l'application."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.dataset = DataSet()
        self.data = self.dataset.all_to_dict()
        
        super().__init__()    
        
        self.setWindowTitle(" Scolar")
        self.setFixedSize(1050, 700)
        self.setWindowIcon(QIcon('src/app/Images/book-open-bookmark.png'))
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        menuBar = self.menuBar()
        menu = self.__create_menu(menuBar)
        
        SUBMENU_ACTIONS = [
            {"action": QAction(QIcon("src/app/Images/json.png"), "&json", self), "statusTip": "Exporter en json", "shortcut": "Ctrl+j", "triggered": partial(self.save, "json")},
            {"action": QAction(QIcon("src/app/Images/csv.png"), "&csv", self), "statusTip": "Exporter en csv", "shortcut": "Ctrl+c", "triggered": partial(self.save, "csv")},
            {"action": QAction(QIcon("src/app/Images/xml.png"), "&xml", self), "statusTip": "Exporter en xml", "shortcut": "Ctrl+x", "triggered": partial(self.save, "xml")},
            {"action": QAction(QIcon("src/app/Images/yaml.png"), "&yaml", self), "statusTip": "Exporter en yaml", "shortcut": "Ctrl+y", "triggered": partial(self.save, "yaml")},     
        ]      
        self.__create_subMenu(menu, "Exporter", SUBMENU_ACTIONS)
        
       
        TOOLBAR_ACTIONS = [
            {"action": QAction(QIcon("src/app/Images/list.png"), "Liste des données", self), "statusTip": "Afficher la liste des données", "shortcut": "Ctrl+Shift+l", "triggered": self.onMyToolBarButtonClick},
            {"action": QAction(QIcon("src/app/Images/filtering.png"), "&Filter", self), "statusTip": "Filtrer les données", "shortcut": "Ctrl+f", "triggered": self.onMyToolBarButtonClick},
            {"action": QAction(QIcon("src/app/Images/sort.png"), "&Trier", self), "statusTip": "Trier les données", "shortcut": "Ctrl+t", "triggered": self.onMyToolBarButtonClick},
            {"action": QAction(QIcon("src/app/Images/analysing.png"), "&Statistique", self), "statusTip": "Statistique des données", "shortcut": "Ctrl+s", "triggered": self.onMyToolBarButtonClick},
        ]
        
        toolbar = QToolBar("Barre d'outils")
        self.addToolBar(toolbar)
        self.__create_toolbar(toolbar, TOOLBAR_ACTIONS)

   
    def run(self):
        """Lancer l'application."""
        self.show()
        self.app.exec()
        
    def onMyToolBarButtonClick(self, s):
        print("click", s)
     
        
    #  ----------------- Méthodes privées utiles
    def __ask_path(self):
        """Ouvre l'exploreur de fichiers pour demander à l'utilisateur de sélectionner un fichier."""
        
        file_path = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", os.getenv("HOME"), "Fichiers (*.json *.csv *.xml *.yaml)")[0]
        if file_path:
            return file_path
        else:
            QMessageBox.information(self, "Information", "Aucun fichier n'a été sélectionné.")
            return None
        
    def __ask_save_folder(self):
        """Ouvre l'exploreur de fichiers pour demander à l'utilisateur de sélectionner un dossier."""
            
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", os.getenv("HOME"))
        if folder:
            return folder
        else:
            QMessageBox.information(self, "Information", "Aucun dossier n'a été sélectionné.")
            return None
    def __create_menu(self, menu):
        """Créer un menu."""
        
        file_menu = menu.addMenu("&Fichier")
        
        button_action = QAction(QIcon("src/app/Images/server.png"), "&Charger", self)
        button_action.setStatusTip("Chargement des données")
        button_action.triggered.connect(self.load)

        button_action.setShortcut(QKeySequence("Ctrl+l"))
        
        file_menu.addAction(button_action)
        
        file_menu.addSeparator()
        return file_menu
        
    def __create_subMenu(self, menu, name, actions):
        """Créer un sous-menu."""  
          
        # Ajouter le menu avec une icon à gauche    
        export_menu = menu.addMenu(QIcon("src/app/Images/export.png"), name)
            
        for action in actions:
            button = action["action"]
            button.setStatusTip(action["statusTip"])
            button.setShortcut(QKeySequence(action["shortcut"]))
            button.triggered.connect(action["triggered"])
            export_menu.addAction(button)
    
    def __create_toolbar(self, toolbar, actions):
        """Créer une barre d'outils."""
            
        for action in actions:
            button = action["action"]
            button.setStatusTip(action["statusTip"])
            button.setShortcut(QKeySequence(action["shortcut"]))
            button.triggered.connect(action["triggered"])
            toolbar.addAction(button)
            



    # ----------------- Méthodes de gestion des événements    
    def load(self):
        """Charge des données depuis un fichier."""
        
        file_path = self.__ask_path()
        
        if file_path:
            self.dataset.load_data(file_path)
            # show dialog to inform the user
            QMessageBox.information(self, "Information", "Les données ont été chargées avec succès.")
    
    def save(self, save_type:str) -> None:
        """Sauvegarde des données dans un fichier."""
        
        if not self.dataset.data_list:
            QMessageBox.critical(self, "Erreur", "Aucune donnée à sauvegarder veuillez charger des données.")
            raise EmptyDataListError()
        
        save_folder = self.__ask_save_folder()
        
        if not save_folder :
            return
        
        if save_type == "json":
            self.dataset.save_json(f"{save_folder}/scolar_data.json")
        elif save_type == "csv":
            self.dataset.save_csv(f"{save_folder}/scolar_data.csv")
        elif save_type == "xml":
            self.dataset.save_xml(f"{save_folder}/scolar_data.xml")
        elif save_type == "yaml":
            self.dataset.save_yaml(f"{save_folder}/scolar_data.yaml")
        else:
            QMessageBox.critical(self, "Erreur", "Format de fichier non supporté")
            raise UnsupportedFileTypeError()
        QMessageBox.information(self, "Information", "Les données ont été sauvegardées avec succès.")
        
    def closeEvent(self, event):
        """Sauvegarde les données avant de fermer l'application."""
        
        self.dataset.save_json("src/app/data/fake_data.json")
        self.dataset.save_csv("src/app/data/fake_data.csv")
        self.dataset.save_xml("src/app/data/fake_data.xml")
        self.dataset.save_yaml("src/app/data/fake_data.yaml")
        event.accept()
  
        
    # -------------- Autre méthodes utiles 
    
    def generate_fake_data_sources(self, number_of_row:int) -> None:
        """Génère des données aléatoires et les sauvegarde dans des fichiers de différents formats."""
        
        fake = Faker("fr_FR")

        data = [] # Liste de dictionnaires

        for i in range(number_of_row):
            
            row = {} # Dictionnaire de données aléatoires
            row["first_name"] = fake.first_name()
            row["last_name"] = fake.last_name()
            row["age"] = fake.random_int(min=18, max=60)
            row["apprentice"] = fake.boolean()
            row["grades"] = [fake.random_int(min=0, max=100) for i in range(fake.random_int(min=3, max=6))]
        
            data.append(row)
        
        self.dataset.save_json(f"{self.dataset.data_source_folder}fake_data.json", data)
        self.dataset.save_csv(f"{self.dataset.data_source_folder}fake_data.csv", data)
        self.dataset.save_xml(f"{self.dataset.data_source_folder}fake_data.xml", data)
        self.dataset.save_yaml(f"{self.dataset.data_source_folder}fake_data.yaml", data)
        
   
