import ast
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame

from  src.dataManagement.dataset import DataSet 

class Interface:
    """Classe représentant l'interface graphique de l'application."""
    
    def __init__(self) -> None:
        self.dataset = DataSet() # Ensemble de données
        self.root = Tk() # Fenêtre principale
        self.title = "Tableau de bord"
        self.size = "1200x768"
        self.image_folder = "src/app/Images"
        self.icon_path = f"{self.image_folder}/icon.png"
        self.bg_color = "#eff5f6"
        self.sound_folder = r"src/app/Son"
        self.configure_window()
    
        
    def configure_window(self):
        """Configure la fenêtre principale."""
        
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.iconphoto(True, self.__load_image(self.icon_path))
        self.root.config(bg=self.bg_color)

    def run(self):
        """Lance l'interface graphique."""
        
        pygame.init()
        self.quit = pygame.mixer.Sound(f"{self.sound_folder}/Sonnerie-Game-of-Thrones.mp3")  
        self.create_components()
        self.root.mainloop()
    
    def close(self):
        """Ferme l'interface graphique."""
        
        self.quit.play()
        pygame.time.wait(int(self.quit.get_length() * 100))
        self.root.quit()
        
        
    def create_components(self):
        """Crée les composants de l'interface."""
        
        self.create_header()
        self.create_menu()
        self.create_dashboard_button()
        self.create_data_source_button()
        self.create_exit_button()
        self.create_dashboard_frame()
        self.create_data_list_button()
      
      
    # ----------------- Méthodes de création de composants
     
    def create_header(self):
        self.header = self.__create_frame(300, 0, 1070, 60, "#0064d3")
        
    def create_menu(self):
        self.menu = self.__create_frame(0, 0, 300, 750, "#ffffff")
        self.create_label_with_image(self.menu, f"{self.image_folder}/icon.png", 5, 5)
        self.create_button(self.menu, "Tableau de bord", self.show_statistics, 100, 320)
        self.create_button(self.menu, "Source de données", self.load_data, 100, 420)
        self.create_button(self.menu, "Quitter", self.close, 100, 520)
    
    def create_dashboard_button(self):
        self.create_label_with_image(self.menu, f"{self.image_folder}/dashboard.png", 35, 300)
        self.create_button(self.menu, "Tableau de bord", self.show_statistics, 100, 320)
        
    def create_data_source_button(self):
        self.create_label_with_image(self.menu, f"{self.image_folder}/source.png", 35, 400)
        self.create_button(self.menu, "Source de données", self.load_data, 100, 420)
    
    def create_data_list_button(self):
        self.create_label_with_image(self.menu, f"{self.image_folder}/data_list.png", 35, 200)
        self.create_button(self.menu, "Liste des données", self.show_data_list, 100, 220)
    
    def create_exit_button(self):
        self.create_label_with_image(self.menu, f"{self.image_folder}/quit.png", 35, 510)
        self.create_button(self.menu, "Quitter", self.close, 100, 520)
    
    def create_dashboard_frame(self):
        self.dashboard_frame = self.__create_frame(300, 60, 1070, 690, self.bg_color)
        self.create_label(self.dashboard_frame, "Tableau de bord", "#0064d3", self.bg_color, 325, 70)
    
    
    def create_label(self, frame, text, text_color, bg_color, x, y, font_family="times new roman", font_size=12, font_weight="normal"):
        label = Label(frame, text=text, font=(font_family, font_size, font_weight), fg=text_color, bg=bg_color)
        label.place(x=x, y=y)
    
    def create_label_with_image(self, frame, image_path, x, y):
        photo = self.__load_image(image_path)
        label = Label(frame, image=photo, bg="#ffffff")
        label.image = photo
        label.place(x=x, y=y)
        
    def create_button(self, frame, text, command, x, y):
        button = Button(frame, text=text, bg="#ffffff", font=("times new roman", 11), bd=0, cursor="hand2", activebackground="#ffffff", command=command)
        button.place(x=x, y=y)
        

    #  ----------------- Méthodes privées utiles
    def __ask_path(self):
        """Ouvre l'exploreur de fichiers pour demander à l'utilisateur de sélectionner un fichier."""
        
        file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.json;*.xml;*.csv;*.yaml")])
        if file_path:
            return file_path
        else:
            messagebox.showinfo("Annulation", "Aucun fichier sélectionné.")
            return None
    
    def __load_image(self,image_path):
        """Charge une image depuis un fichier."""
        
        return ImageTk.PhotoImage(Image.open(image_path))
    
    
    def __create_frame(self, x, y, width, height, bg_color):
        """Crée un cadre dans la fenêtre principale."""
        
        frame = Frame(self.root, bg=bg_color)
        frame.place(x=x, y=y, width=width, height=height)
        return frame 
    
    
    # ----------------- Méthodes de gestion des événements    
    def load_data(self):
        """Charge des données depuis un fichier."""
        
        file_path = self.__ask_path()
         
        if file_path:
                
            if file_path.endswith('.json'):
                self.dataset.load_json(file_path)
               
            elif file_path.endswith('.xml'):
                self.dataset.load_xml(file_path)
                    
            elif file_path.endswith('.csv'):
                self.dataset.load_csv(file_path)
                    
            elif file_path.endswith('.yaml'):
                self.dataset.load_yaml(file_path)
            else:
                messagebox.showerror("Erreur", "Format de fichier non supporté.")
                return
        
    def show_statistics(self):
        """Affiche les statistiques des données."""
        
        if not self.dataset.data_list:
            messagebox.showerror("Erreur", "Aucune donnée à afficher veuillez choisir un fichier source de données.")
            return 
        
        self.dashboard_frame.destroy()
        self.dashboard_frame = self.__create_frame(300, 60, 1070, 690, self.bg_color)
        self.create_label(self.dashboard_frame, "Tableau de bord", "#0064d3", self.bg_color, 325, 70)
        
        data_stats = self.dataset.generate_stats()

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
        # canvas = FigureCanvasTkAgg(fig, master=self.dashboard_frame)
        # canvas.draw()
        # canvas.get_tk_widget().place(x=0, y=100)
        
    def show_data_list(self):
        """Affiche la liste des données."""
        
        if not self.dataset.data_list:
            messagebox.showerror("Erreur", "Aucune donnée à afficher veuillez choisir un fichier source de données.")
            return 
        
        self.dashboard_frame.destroy()
        self.dashboard_frame = self.__create_frame(300, 60, 1070, 690, self.bg_color)
        self.create_label(self.dashboard_frame, "Tableau de bord", "#0064d3", self.bg_color, 325, 70)
        
        data = self.dataset.all_to_dict()
        
        data_list = Listbox(self.dashboard_frame, bg=self.bg_color, font=("times new roman", 12), bd=0, relief=GROOVE, selectbackground="#0064d3")
        data_list.place(x=0, y=100, width=1070, height=590)
        
        for item in data:
            data_list.insert(END, item)
            
    #     data_list.bind("<<ListboxSelect>>", self.show_data)
        
    # def show_data(self, event):
    #     """Affiche les détails d'une donnée."""
        
    #     data_list = event.widget
    #     index = data_list.curselection()[0]
    #     data = data_list.get(index)
        
    #     self.dashboard_frame.destroy()
    #     self.dashboard_frame = self.__create_frame(300, 60, 1070, 690, self.bg_color)
    #     self.create_label(self.dashboard_frame, "Tableau de bord", "#0064d3", self.bg_color, 325, 70)
        
    #     data_details = self.dataset.get_by_id(data)
    #     data_details_label = Label(self.dashboard_frame, text=data_details, font=("times new roman", 12), bg=self.bg_color)
    #     data_details_label.place(x=0, y=100, width=1070, height=590)
        
        
        
          