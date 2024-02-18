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
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)

from  src.dataManagement.dataset import DataSet 
from src.customException.load_exception import UnsupportedFileTypeError
from  src.customException.save_exception import EmptyDataListError
from src.operations.filter import Filter


class Interface2(QMainWindow):
    """Classe représentant l'interface graphique de l'application."""
    
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.dataset = DataSet()
        self.data = self.dataset.data_list
        
        super().__init__()    
        self.__setup()
        
        
   
    def run(self) -> None:
        """Lancer l'application."""
        self.show()
        self.app.exec()
        
    def onMyToolBarButtonClick(self, s):
        print(self.dataset.all_to_dict())
     
        
    #  --------------------------  Méthodes privées utiles
    
    def __setup (self) -> None:
        """Initialiser l'interface graphique."""
        self.setWindowTitle(" Scolar")
        self.setFixedSize(1050, 700)
        self.setWindowIcon(QIcon('src/app/Images/book-open-bookmark.png'))
        
        self.__create_widgets()
        self.__create_layouts()
        self.__add_widgets_to_layouts() 
        
        
           
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
    

        
    def __create_widgets(self):
        """Créer des widgets."""
        
        self.main_widget = QWidget()
        self.list_widget = QTableWidget()
        self.operations_widget = QWidget()

        
    def __create_layouts(self):
        """Créer les layouts."""
        
        self.main_layout = QHBoxLayout(self.main_widget)
        self.operations_layout = QGridLayout(self.operations_widget)
        
    def __add_widgets_to_layouts(self):
        """Ajouter les widgets aux layouts."""
        
        # Menu
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
        
        
        # Tool bar
        TOOLBAR_ACTIONS = [
            {"action": QAction(QIcon("src/app/Images/list.png"), "Liste des données", self), "statusTip": "Afficher la liste des données", "shortcut": "Ctrl+Shift+l", "triggered": partial(self.show_list, self.data)},
            {"action": QAction(QIcon("src/app/Images/filtering.png"), "&Filter", self), "statusTip": "Filtrer les données", "shortcut": "Ctrl+f", "triggered": self.onMyToolBarButtonClick},
            {"action": QAction(QIcon("src/app/Images/sort.png"), "&Trier", self), "statusTip": "Trier les données", "shortcut": "Ctrl+t", "triggered": self.onMyToolBarButtonClick},
            {"action": QAction(QIcon("src/app/Images/analysing.png"), "&Statistique", self), "statusTip": "Statistique des données", "shortcut": "Ctrl+s", "triggered": self.onMyToolBarButtonClick},
        ]
        
        toolbar = QToolBar("Barre d'outils")
        self.addToolBar(toolbar)
        self.__create_toolbar(toolbar, TOOLBAR_ACTIONS)
        
        # Main layout
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.list_widget)  
        self.main_layout.addWidget(self.operations_widget)
        
        # Operations layout
        self.operations_widget.setLayout(self.operations_layout)
        
            
    def __create_filter_widgets(self):
        """Créer les widgets de filtrage."""
        
        self.options = [
            "C - Comparaison lexicographique",
            "C - Contient",
            "C - Commence par",
            "C - Finit par",
            "L - Liste contient",
            "L - Minimum liste superieur à",
            "L - Maximum liste inférieur à",
            "L - Moyenne liste superieur à",
            "G - Comparaison statistiques globales",
            "C - Comparaison de champs",
            "C - Champs combinés"
        ]

        # Votre dictionnaire qui associe chaque option à une méthode de filtrage
        self.methods = {
            "C - Comparaison lexicographique": Filter.filter_by_string_lexicographical,
            "C - Contient": Filter.filter_by_string_contains,
            "C - Commence par": Filter.filter_by_string_starts_with,
            "C - Finit par": Filter.filter_by_string_ends_with,
            "L - Liste contient": Filter.filter_by_list_all_elements,
            "L - Minimum liste superieur à": Filter.filter_by_list_min,
            "L - Maximum liste inférieur à": Filter.filter_by_list_max,
            "L - Moyenne liste superieur à": Filter.filter_by_list_average,
            "G - Comparaison statistiques globales": Filter.filter_by_global_statistics,
            "C - Comparaison de champs": Filter.compare_fields,
            "C - Champs combinés": Filter.filter_by_combined_fields
        }
        
        # Créer un label pour le champ
        self.filter_field_label = QLabel("Choisir le champ à filtrer :")
        # Créer une combobox pour le champ
        self.filter_field_combo = QComboBox()
        # Ajouter les champs disponibles à la combobox
        self.filter_field_combo.addItems(self.fields)
        # Créer un label pour l'option
        self.filter_option_label = QLabel("Choisir l'option de filtrage :")
        # Créer une combobox pour l'option
        self.filter_option_combo = QComboBox()
        # Ajouter les options de filtrage à la combobox
        self.filter_option_combo.addItems(self.options)
        # Créer un label pour la valeur
        self.filter_value_label = QLabel("Saisir la valeur à filtrer :")
        # Créer une line edit pour la valeur
        self.filter_value_edit = QLineEdit()
        # Créer un bouton pour appliquer le filtrage
        self.filter_apply_button = QPushButton("Appliquer")
        
        self.filter_apply_button.clicked.connect(self.filter_data)
        
        
        
    def __add_filter_widgets_to_layout(self):
        """Ajouter les widgets de filtrage au layout."""
        
        self.operations_layout.addWidget(self.filter_field_label, 0, 0)
        self.operations_layout.addWidget(self.filter_field_combo, 0, 1)
        self.operations_layout.addWidget(self.filter_option_label, 1, 0)
        self.operations_layout.addWidget(self.filter_option_combo, 1, 1)
        self.operations_layout.addWidget(self.filter_value_label, 2, 0)
        self.operations_layout.addWidget(self.filter_value_edit, 2, 1)
        self.operations_layout.addWidget(self.filter_apply_button, 3, 0, 1, 2)

        self.operations_layout.setAlignment(Qt.AlignTop)
        self.operations_layout.setSpacing(10)
        self.operations_layout.setContentsMargins(10, 10, 10, 10)
        
        
        


    # ----------------- Méthodes de gestion des événements    
    def load(self):
        """Charge des données depuis un fichier."""
        
        file_path = self.__ask_path()
        
        if file_path:
            self.dataset.load_data(file_path)
            self.data = self.dataset.data_list
            self.show_list(self.dataset.all_to_dict())
            self.statusBar.showMessage(f"Les données ont été chargées avec succès depuis {file_path}")
            self.fields = self.dataset.data_list[0].get_fields()
            self.__create_filter_widgets()
            self.__add_filter_widgets_to_layout()
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
        

    def show_list(self, liste):
        """Affiche une liste de données dans un tableau."""
        
        if liste == []:
            if self.dataset.data_list:
                self.data = self.dataset.data_list
                liste = self.dataset.all_to_dict()
            else:
                QMessageBox.critical(self, "Erreur", "Aucune donnée à afficher veuillez charger des données.")
                raise EmptyDataListError()
        
        # Effacer le tableau
        self.list_widget.clearContents()
        self.list_widget.setRowCount(0)

        self.list_widget.setColumnCount(6)  # Nombre de colonnes basé sur les attributs des étudiants

        headers = ['First Name', 'Last Name', 'Age', 'Apprentice', 'Grades', 'Average Grade']
        self.list_widget.setHorizontalHeaderLabels(headers)

        # Remplir le tableau avec les données des étudiants
        for row, student in enumerate(liste):
            self.list_widget.insertRow(row)
            self.list_widget.setItem(row, 0, QTableWidgetItem(student['first_name']))
            self.list_widget.setItem(row, 1, QTableWidgetItem(student['last_name']))
            self.list_widget.setItem(row, 2, QTableWidgetItem(str(student['age'])))
            self.list_widget.setItem(row, 3, QTableWidgetItem(str(student['apprentice'])))
            self.list_widget.setItem(row, 4, QTableWidgetItem(', '.join(map(str, student['grades']))))

            # Calculer la moyenne des notes
            average_grade = sum(student['grades']) / len(student['grades'])
            self.list_widget.setItem(row, 5, QTableWidgetItem(f'{average_grade:.2f}'))
    
    
    def filter_data(self):
        # Récupérer le champ choisi
        field = self.filter_field_combo.currentText()
        # Récupérer l'option choisie
        option = self.filter_option_combo.currentText()
        # Récupérer la valeur saisie
        value = self.filter_value_edit.text()
        # Récupérer la méthode de filtrage correspondante
        method = self.methods[option]
        # Appeler la méthode de filtrage avec les paramètres appropriés
        # Vous devrez adapter cette partie en fonction des cas particuliers
        filtered_data = method(self.data, field, value)
        # Afficher les données filtrées
        if filtered_data == []:
            QMessageBox.information(self, "Information", "Aucune donnée ne correspond à votre recherche.")
        else:
            self.data = filtered_data
            filtered_data = self.dataset.all_to_dict(filtered_data)
            self.show_list(filtered_data)

  
        
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
        
   
