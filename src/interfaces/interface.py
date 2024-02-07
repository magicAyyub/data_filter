from tkinter import*
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import*
import time
import pandas as pd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np 
import xml.etree.ElementTree as ET
import json
import pygame




#=================================    Class INTERPHASE   ==================================================
class Dashboard:
    def __init__(self,root):
        self.root=root
        self.root.title("Tableau de bord")
        self.root.geometry("1366x768")
        self.root.config(bg="#eff5f6")
        
        icon= PhotoImage(file=r"Imagee\Capture d'écran 2024-02-05 170158.png")# pour changer l'icone feuille avec mon logo 
        self.root.iconphoto(True,icon)  
            
#====================================== Son quand il quitte ==============================
        pygame.init()
        self.son_quitter = pygame.mixer.Sound(r"Son\Sonnerie-Game-of-Thrones.mp3")             
        
 #================================= en tete ============================================
        self.entete=Frame(self.root,bg="MidnightBlue")
        self.entete.place(x=300,y=0,width=1070,height=60)   
          
        
#================================== Menu ==========================================
        self.FrameMenu=Frame(self.root,bg="#ffffff")
        self.FrameMenu.place(x=0,y=0,width=300,height=750)        
        self.logoImage=Image.open(r"Imagee\Capture d'écran 2024-02-05 170158.png")
        photo=ImageTk.PhotoImage(self.logoImage)
        self.logo=Label(self.FrameMenu,image=photo,bg="#ffffff")
        self.logo.image = photo
        self.logo.place(x=5,y=5)
#======================================  Source de données =======================================
        self.source=Image.open(r"C:\Users\elbar\OneDrive\Images\Captures d’écran\Capture d'écran 2024-02-05 174057.png")
        photo=ImageTk.PhotoImage(self.source)
        self.source=Label(self.FrameMenu,image=photo,bg="#ffffff")
        self.source.image = photo
        self.source.place(x=35,y=400)
        
        self.source_text=Button(self.FrameMenu,text="Source de données",bg="#ffffff",font=("tiem new roman",11),bd=0,cursor="hand2",activebackground="#ffffff",command=self.load_data)
        self.source_text.place(x=100,y=420)
        
        
#===================================     Tableau de bord     ==========================================================
        
        self.dashboard=Image.open(r"C:\Users\elbar\OneDrive\Images\Captures d’écran\Capture d'écran 2024-02-05 172443.png")
        photo=ImageTk.PhotoImage(self.dashboard)
        self.dashboard=Label(self.FrameMenu,image=photo,bg="#ffffff")
        self.dashboard.image = photo
        self.dashboard.place(x=35,y=300)
        
        self.dashboard_text=Button(self.FrameMenu,text="Tableau de bord",bg="#ffffff",font=("tiem new roman",11),bd=0,cursor="hand2",activebackground="#ffffff")
        self.dashboard_text.place(x=100,y=320)
        
        
#==================================== Pour quitter  ===================================================================
        self.quitter=Image.open(r"C:\Users\elbar\OneDrive\Images\Captures d’écran\Capture d'écran 2024-02-07 141709.png")
        photo=ImageTk.PhotoImage(self.quitter)
        self.quitter=Label(self.FrameMenu,image=photo,bg="#ffffff")
        self.quitter.image = photo
        self.quitter.place(x=35,y=510)
        
        self.quitter_text=Button(self.FrameMenu,text="Quitter",bg="#ffffff",font=("tiem new roman",11),bd=0,cursor="hand2",activebackground="#ffffff",command=self.close)
        self.quitter_text.place(x=100,y=520)

#============================= Commande pour quitter l'application =======================================================
    def close(self): 
        self.son_quitter.play()
        pygame.time.wait(int(self.son_quitter.get_length() * 100))  
        
        self.root.quit()
        
#=====================================  Permet de selectionner et charger son ficher  ======================================   
    def load_data(self):
            file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.json;*.xml;*.csv")])
            if file_path:
                #Pour json
                if file_path.endswith('.json'):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                # Pour XML
                    self.update_interface_with_json(data)
                elif file_path.endswith('.xml'):
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                #Pour CSV
                    self.update_interface_with_xml(root)
                elif file_path.endswith('.csv'):
                    data = pd.read_csv(file_path)
                    self.update_interface_with_csv(data)
                else:
                    messagebox.showerror("Erreur", "Format de fichier non supporté.")
            else:
                messagebox.showinfo("Annulation", "Opération annulée par l'utilisateur.")

        
        
        
if __name__=="__main__":
    root=Tk()
    Dashboard(root)
    root.mainloop()        
