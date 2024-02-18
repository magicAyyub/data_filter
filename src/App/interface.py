import os
import sys

from faker import Faker
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from matplotlib import pyplot as plt
from  functools import partial
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QMessageBox,
    QFileDialog,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QCheckBox
)

from  src.dataManagement.dataset import DataSet 
from src.customException.load_exception import UnsupportedFileTypeError
from  src.customException.save_exception import EmptyDataListError
from src.operations.filter import Filter
from src.operations.sorter import Sorter


class Interface(QMainWindow):
    """Classe représentant l'interface graphique de l'application."""
    
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.dataset = DataSet()
        self.data = self.dataset.data_list
        
        super().__init__()    
        self.__setup()
        
        self.filter_widgets_created = False
        self.sort_widgets_created = False
        
        
   
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
        self.setMinimumSize(1050, 700)
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
            {"action": QAction(QIcon("src/app/Images/list.png"), "Liste des données", self), "statusTip": "Afficher la liste des données", "shortcut": "Ctrl+Shift+l", "triggered": partial(self.show_list, self.dataset.all_to_dict(self.data))},
            {"action": QAction(QIcon("src/app/Images/filtering.png"), "&Filter", self), "statusTip": "Filtrer les données", "shortcut": "Ctrl+f", "triggered": self.show_filter},
            {"action": QAction(QIcon("src/app/Images/sort.png"), "&Trier", self), "statusTip": "Trier les données", "shortcut": "Ctrl+t", "triggered": self.show_sorter},
            {"action": QAction(QIcon("src/app/Images/analysing.png"), "&Statistique", self), "statusTip": "Statistique des données", "shortcut": "Ctrl+s", "triggered": self.show_statistics},
        ]
        
        toolbar = QToolBar("Barre d'outils")
        self.addToolBar(toolbar)
        self.__create_toolbar(toolbar, TOOLBAR_ACTIONS)
        
            # Main layout
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.list_widget, stretch=2)  # Adjust the stretch factor to allocate more space

        # Operations layout
        self.operations_widget = QWidget()
        self.operations_layout = QGridLayout(self.operations_widget)
        self.operations_widget.setLayout(self.operations_layout)
        self.main_layout.addWidget(self.operations_widget, stretch=1)  # Adjust the stretch factor for the filter panel
        
            
    def __create_filter_widgets(self):
        """Créer les widgets de filtrage."""
        
        self.options = [
            "String - Comparaison lexicographique",
            "String - Contient",
            "String - Commence par",
            "String - Finit par",
            "Number - Plus grand que",
            "Number - Plus petit que",
            "Number - Égal à",
            "Boolean - Est Vrai",
            "Boolean - Est Faux",
            "Liste - Minimum liste",
            "Liste - Maximum liste",
            "Liste - Moyenne liste",
            "Liste - Toutes Liste contient",
        ]

        # Votre dictionnaire qui associe chaque option à une méthode de filtrage
        self.methods = {
            "String - Comparaison lexicographique": Filter.filter_by_string_lexicographical,
            "String - Contient": Filter.filter_by_string_contains,
            "String - Commence par": Filter.filter_by_string_starts_with,
            "String - Finit par": Filter.filter_by_string_ends_with,
            "Number - Plus grand que": Filter.filter_by_number_greater_than,
            "Number - Plus petit que": Filter.filter_by_number_less_than,
            "Number - Égal à": Filter.filter_by_number_equal_to,
            "Boolean - Est Vrai": Filter.filter_by_boolean,
            "Boolean - Est Faux": Filter.filter_by_boolean,
            "Liste - Minimum liste": Filter.filter_by_list_min,
            "Liste - Maximum liste": Filter.filter_by_list_max,
            "Liste - Moyenne liste": Filter.filter_by_list_average,
            "Liste - Toutes Liste contient": Filter.filter_by_list_all_elements,
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
        
        
    def __create_sorter_widgets(self):
        """Créer les widgets de tri."""
        
        self.sort_options = [
            "Trier par champ",
            # "Trier par plusieurs champs",
            # "Trier par valeur globale",
            # "Trier par critère de priorité",
        ]

        # Votre dictionnaire qui associe chaque option à une méthode de tri
        self.sort_methods = {
            "Trier par champ": Sorter.sort_by_field,
            # "Trier par plusieurs champs": Sorter.sort_by_multiple_fields,
            # "Trier par valeur globale": Sorter.sort_by_global_value,
            # "Trier par critère de priorité": Sorter.sort_by_priority_criteria,
        }
        
        self.sort_option_label = QLabel("Choisir l'option de tri :")
        self.sort_option_combo = QComboBox()
        self.sort_option_combo.addItems(self.sort_options)
        
        self.sort_field_label = QLabel("Choisir le champ de tri :")
        self.sort_field_combo = QComboBox()
        self.sort_field_combo.addItems(self.fields)
        
        # reverse checkbox
        self.reverse_label = QLabel("Inverser l'ordre")
        self.reverse_checkbox = QCheckBox("Inverser l'ordre")
        
        # Créer un bouton pour appliquer le tri
        self.sort_apply_button = QPushButton("Appliquer")
        
        # Si l'option "Trier par plusieurs champs" est sélectionnée
        if self.sort_option_combo.currentText() == "Trier par plusieurs champs":
            # Modifier la combobox pour permettre la sélection multiple
            self.sort_field_combo.setMultiSelect(True)         
        
        self.sort_apply_button.clicked.connect(self.sort_data)
        
    def __add_sorter_widgets_to_layout(self):
        """Ajouter les widgets de tri au layout."""
        
        self.operations_layout.addWidget(self.sort_option_label, 0, 0)
        self.operations_layout.addWidget(self.sort_option_combo, 0, 1)
        self.operations_layout.addWidget(self.sort_field_label, 1, 0)
        self.operations_layout.addWidget(self.sort_field_combo, 1, 1)
        self.operations_layout.addWidget(self.reverse_label, 2, 0)
        self.operations_layout.addWidget(self.reverse_checkbox, 2, 1)
        self.operations_layout.addWidget(self.sort_apply_button, 3, 0, 1, 2)

        self.operations_layout.setAlignment(Qt.AlignTop)
        self.operations_layout.setSpacing(10)
        self.operations_layout.setContentsMargins(10, 10, 10, 10)

    def remove_filter_widgets(self):
                """Remove the filter widgets from the layout."""
                self.operations_layout.removeWidget(self.filter_field_label)
                self.operations_layout.removeWidget(self.filter_field_combo)
                self.operations_layout.removeWidget(self.filter_option_label)
                self.operations_layout.removeWidget(self.filter_option_combo)
                self.operations_layout.removeWidget(self.filter_value_label)
                self.operations_layout.removeWidget(self.filter_value_edit)
                self.operations_layout.removeWidget(self.filter_apply_button)
                self.operations_layout.removeWidget(self.filter_apply_button)

                self.filter_field_label.deleteLater()
                self.filter_field_combo.deleteLater()
                self.filter_option_label.deleteLater()
                self.filter_option_combo.deleteLater()
                self.filter_value_label.deleteLater()
                self.filter_value_edit.deleteLater()
                self.filter_apply_button.deleteLater()
                self.filter_apply_button.deleteLater()

                self.filter_field_label = None
                self.filter_field_combo = None
                self.filter_option_label = None
                self.filter_option_combo = None
                self.filter_value_label = None
                self.filter_value_edit = None
                self.filter_apply_button = None
                self.filter_apply_button = None

                self.operations_layout.update()
                
    def remove_sorter_widgets(self):
        """Remove the sorter widgets from the layout."""
        self.operations_layout.removeWidget(self.sort_option_label)
        self.operations_layout.removeWidget(self.sort_option_combo)
        self.operations_layout.removeWidget(self.sort_field_label)
        self.operations_layout.removeWidget(self.sort_field_combo)
        self.operations_layout.removeWidget(self.sort_apply_button)
        self.operations_layout.removeWidget(self.reverse_label)

        self.sort_option_label.deleteLater()
        self.sort_option_combo.deleteLater()
        self.sort_field_label.deleteLater()
        self.sort_field_combo.deleteLater()
        self.sort_apply_button.deleteLater()
        self.reverse_label.deleteLater()

        self.sort_option_label = None
        self.sort_option_combo = None
        self.sort_field_label = None
        self.sort_field_combo = None
        self.sort_apply_button = None
        self.reverse_label = None

        self.operations_layout.update()

    # ----------------- Méthodes de gestion des événements    
    def load(self):
        """Charge des données depuis un fichier."""
        
        file_path = self.__ask_path()
        
        if file_path:
            self.dataset.load_data(file_path)
            self.data = self.dataset.data_list
            self.show_list(self.dataset.all_to_dict())
            self.statusBar.showMessage(f"Les données ont été chargées avec succès depuis {file_path}")

    def show_filter(self):
        if not self.dataset.data_list:
            QMessageBox.critical(self, "Erreur", "Aucune donnée à filtrer veuillez charger des données.")
            raise EmptyDataListError()
        
        if self.sort_widgets_created:  
            self.remove_sorter_widgets()
            self.sort_widgets_created = False
        self.fields = self.dataset.data_list[0].get_fields()
        self.__create_filter_widgets()
        self.__add_filter_widgets_to_layout()
        self.filter_widgets_created = True
    
    def show_sorter(self):
        if not self.dataset.data_list:
            QMessageBox.critical(self, "Erreur", "Aucune donnée à trier veuillez charger des données.")
            raise EmptyDataListError()
        if self.filter_widgets_created:  
            self.remove_filter_widgets()
            self.filter_widgets_created = False
            
        self.fields = self.dataset.data_list[0].get_fields()
        self.__create_sorter_widgets()
        self.__add_sorter_widgets_to_layout()
        self.sort_widgets_created = True
       
            
    
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
        field = self.filter_field_combo.currentText()
       
        option = self.filter_option_combo.currentText()
 
        value = self.filter_value_edit.text()

        try:
            value = float(value)
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un nombre pour le filtre.")
            return

        field_types = {
            "first_name": str,
            "last_name": str,
            "age": int,
            "apprentice": bool,
            "grades": list,    
        }

        expected_type = field_types.get(field)

        if expected_type is None:
            QMessageBox.critical(self, "Erreur", "Champ de filtre inconnu.")
            return

        try:
            if expected_type == list:
                value = eval(value)
            elif expected_type == bool:
                value = value.lower() in ['true', '1', 't', 'y', 'yes']
            else:
                value = expected_type(value)
        except ValueError:
            QMessageBox.critical(self, "Erreur", f"Veuillez entrer une valeur de type {expected_type.__name__} pour le filtre.")
            return

        method = self.methods[option]

        try:
            filtered_data = method(self.data, field, value)
        except TypeError as e:
            QMessageBox.critical(self, "Veillez utiliser un type de filtre compatible avec le champ sélectionné.")
            return
        
        if filtered_data == []:
            QMessageBox.information(self, "Information", "Aucune donnée ne correspond à votre recherche.")
        else:
            self.data = filtered_data
            filtered_data = self.dataset.all_to_dict(filtered_data)
            self.show_list(filtered_data)

    def sort_data(self):
        option = self.sort_option_combo.currentText()
        field = self.sort_field_combo.currentText()
        reverse = self.reverse_checkbox.isChecked()

        if option == "Trier par champ":
            if reverse:
                sorted_data = Sorter.sort_by_field(self.data, field, reverse=True)
            else:
                sorted_data = Sorter.sort_by_field(self.data, field)
        elif option == "Trier par plusieurs champs":
            if reverse:
                sorted_data = Sorter.sort_by_multiple_fields(self.data, [field], reverse=True)
            else:
                sorted_data = Sorter.sort_by_multiple_fields(self.data, [field])
        elif option == "Trier par valeur globale":
            if reverse:
                sorted_data = Sorter.sort_by_global_value(self.data, field, lambda x: x, reverse=True)
            else:
                sorted_data = Sorter.sort_by_global_value(self.data, field, lambda x: x)
        elif option == "Trier par critère de priorité":
            if reverse:
                sorted_data = Sorter.sort_by_priority_criteria(self.data, [lambda x: x.get_field_value(field)], reverse=True)
            else:
                sorted_data = Sorter.sort_by_priority_criteria(self.data, [lambda x: x.get_field_value(field)])

        self.data = sorted_data
        sorted_data = self.dataset.all_to_dict(sorted_data)
        self.show_list(sorted_data)

    def show_statistics(self) -> None:
        """Affiche les statistiques des données."""
        
        if not self.dataset.data_list:
            QMessageBox.critical(self, "Erreur", "Aucune donnée à afficher veuillez charger des données.")
            return 
        
        
        data_stats = self.dataset.generate_stats(self.data)

        # Affichage graphique des statistiques
        fig, axes = plt.subplots(1, len(data_stats), figsize=(15, 5))

        for i, (nom_champ, stats_champ) in enumerate(data_stats.items()):
            if isinstance(stats_champ, dict):
                # Traitement spécifique pour chaque type de champ
                if 'min' in stats_champ and 'max' in stats_champ and 'avg' in stats_champ:
                    # Champ représentant un nombre
                    labels = ['Minimum', 'Maximum', 'Moyenne']
                    values = list(stats_champ.values())
                    axes[i].bar(labels, values, color=['blue', 'orange', 'green'])
                    axes[i].set_title(f'Champ représentant un nombre')
                    axes[i].set_xlabel('Statistique')
                    axes[i].set_ylabel('Valeur')

                elif 'true_percentage' in stats_champ and 'false_percentage' in stats_champ:
                    # Champ représentant un booléen
                    labels = ['Vrai', 'Faux']
                    values = list(stats_champ.values())
                    axes[i].pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
                    axes[i].set_title(f'Champ représentant un booléen')

                elif 'min_len' in stats_champ and 'max_len' in stats_champ and 'avg_len' in stats_champ:
                    # Champ représentant une liste
                    labels = ['Longueur Min', 'Longueur Max', 'Longueur Moyenne']
                    values = list(stats_champ.values())
                    axes[i].bar(labels, values, color=['red', 'yellow', 'green'])
                    axes[i].set_title(f'Champ représentant une liste')
                    axes[i].set_xlabel('Type')
                    axes[i].set_ylabel('Longueur')

        plt.tight_layout()
        plt.show() 
        
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
        
   
