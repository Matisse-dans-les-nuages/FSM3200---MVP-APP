import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os
import datetime

#=======================================
# CLASS - DATA FRAME MANAGER
#=======================================
class DataFrameManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file, index_col='file')
        #Sauter à la première ligne non-sauvegardée (gain de temps)
        self.progress = self.progress = len(self.df[self.df['saves'] == 1])#get len of df with completed lines (saves == 1)
        self.current_index = self.progress # TODO: set to first unsaved line # 0 if bugs from line 16

    def get_current_row(self):
        return self.df.iloc[self.current_index]

    def update_current_row(self, radio_var, hydrometeor,complete_state):
        self.df.iloc[self.current_index, self.df.columns.get_loc('radio variable')] = radio_var
        self.df.iloc[self.current_index, self.df.columns.get_loc('hydrometeor')] = hydrometeor
        self.df.iloc[self.current_index, self.df.columns.get_loc('saves')] += complete_state

    def save_to_csv(self):
        self.df.to_csv(self.csv_file)

    def next(self):
        if self.current_index < len(self.df) - 1:
            self.current_index += 1
        else:
            messagebox.showinfo("End", "No more images.")
        return self.get_current_row()

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            messagebox.showinfo("Start", "This is the first image.")
        return self.get_current_row()

#=======================================
# CLASS - MASC APP
#=======================================
class MascApp:
    def __init__(self, root, data_manager):
        self.root = root
        # Instance de DataFrameManager qui contient un csv et les fonctions qui s'y rapportent
        self.data_manager = data_manager
        self.path_to_images = "../../MASC_IMAGES/"
        # Fenêtre de l'application
        self.root.title("MASC Validation Protocol Interface")
        self.root.geometry("600x400")

        # Variables initiales dans les sélections du menu
        self.radio_var = tk.IntVar(value=0)
        self.hm_cbx_var = tk.StringVar(value='Aucune Sélection')
        self.position = tk.IntVar(value = data_manager.current_index) # TODO : set to data_manager current index
        self.completed = tk.IntVar(value = self.data_manager.df['saves'].sum())
        self.datalenght = len(data_manager.df)+1
        self.message_to_user_STRINGVAR = tk.StringVar(value=f"image\t\t{self.position.get()} de {self.datalenght}\n\n"
                                                            f"complétée(s)\t{self.completed.get()} de {self.datalenght}")
        # Variable d'auto-sauvegarde
        self.autosave_progress = 0

        # Installation des widgets dès l'initialisation d'une instance de l'app
        self.create_widgets()
        # ==========================
        # END OF __init__()
        # ==========================
    ############################################################################
    #==========================
    # APP WIDGETS
    #==========================
    def create_widgets(self):
        # Image placeholder (Label as placeholder for image display)
        self.image_label = tk.Label(self.root, text= "[ Les images apparaîtront ici ]\n\nAppuyez sur «Commencer la tâche»")
        self.image_label.place(x=20, y=50, anchor='nw', width=300, height=200)

        # =======================================
        # MESSAGE TO USER LABEL - widgets
        # =======================================
        # INFORMATIONS
        message_to_user = ttk.Label(
            self.root,
            textvariable = self.message_to_user_STRINGVAR,
            font = ('Avenir',14)
        )
        # POSITION

        message_to_user.place(x=350,y=200,anchor='nw')


        # =======================================
        # RADIOBUTTON - widgets
        # =======================================
        # ==========================
        # RADIOBUTTON LABEL
        # ==========================
        # INFORMATIONS
        rad_btn_label_STRINGVAR = tk.StringVar(value="L'image est-elle corrompue?")
        rad_btn_label = ttk.Label(
            self.root,
            text=rad_btn_label_STRINGVAR.get(),
            font=('Avenir', 16)
        )
        # POSITION
        rad_btn_label.place(x=350, y=50, anchor='nw')
        # ==========================
        # RADIOBUTTON 1
        # ==========================
        # INFORMATIONS
        self.rad_btn_1 = ttk.Radiobutton(
            self.root,
            text="non",
            value=0,
            variable=self.radio_var,
            command=self.radio_btn_event,
            state='disabled'
        )
        # POSITION
        self.rad_btn_1.place(x=350, y=75, anchor='nw')
        # ==========================
        # RADIOBUTTON 2
        # ==========================
        # INFORMATIONS
        self.rad_btn_2 = ttk.Radiobutton(
            self.root,
            text="oui",
            value=1,
            variable=self.radio_var,
            command=self.radio_btn_event,
            state='disabled'
        )
        #POSITION
        self.rad_btn_2.place(x=400, y=75, anchor='nw')

        # =======================================
        # COMBOBOX - widgets
        # =======================================
        # ==========================
        # COMBOBOX LABEL
        # ==========================
        # VAR
        hm_cbx_label_STRINGVAR = tk.StringVar(value="Identifiez l'hydrométéore.")

        # INFORMATION
        hm_cbx_label = tk.Label(
            self.root,
            text=hm_cbx_label_STRINGVAR.get(),
            font=("Avenir", 16)
        )
        # POSITION
        hm_cbx_label.place(x=350, y=115, anchor='nw')

        # ==========================
        # COMBOBOX 1
        # ==========================
        # VALEURS
        hm_list = ['Small particle',
                   'Columnar crystal',
                   'Planar crystal',
                   'Columnar/Planar crystals',
                   'Aggregate',
                   'Graupel',
                   'None']
        # INFORMATIONS
        self.hm_combobox = ttk.Combobox(
            self.root,
            textvariable=self.hm_cbx_var,
            values=hm_list,
            state='disabled'
        )
        # POSITION
        self.hm_combobox.place(x=350, y=150, anchor='nw')

        # =======================================
        # CLICK BUTTONS - widgets
        # =======================================
        # BOTTOM FRAME
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side='bottom', pady=10)
        # ==========================
        # START BUTTON - |Commencer la tâche|
        # ==========================
        # VAR - |Commencer la tâche|
        Startbutton_text_STRINGVAR = tk.StringVar(value = "Commencer la tâche")

        # INFORMATIONS - |Commencer la tâche|
        self.start_button = ttk.Button(
            self.root,
            command = self.start_button_func,
            text = Startbutton_text_STRINGVAR.get(),
            state='enabled'
        )
        # POSITION - |Commencer la tâche|
        # TODO
        self.start_button.pack(anchor='n')  # Côté droit de l'app

        # ==========================
        # CONFIRM BUTTON - |Confirmer sélection|
        # ==========================
        # VAR - |Confirmer|
        Confirmbutton_text_STRINGVAR = tk.StringVar(value='Confirmer sélection')

        # INFORMATIONS - |Confirmer sélection|
        self.confirm_button = ttk.Button(
            self.root,
            command=self.confirm_btn_func,          #COMMAND - confirm_button_func()
            text=Confirmbutton_text_STRINGVAR.get(),
            state='disabled'
        )
        # POSITION - |Confirmer sélection|
        self.confirm_button.place(x=425,y=300, anchor='nw') # Côté droit de l'app

        # ==========================
        # RESET BUTTON - |Recommencer|
        # ==========================
        # VAR - |Recommencer|
        Resetbutton_text_STRINGVAR = tk.StringVar(value='Recommencer')

        # INFORMATIONS - |Recommencer|
        self.reset_button = ttk.Button(
            self.root,
            command=self.reset_button_func,          #COMMAND - reset_button_func()
            text=Resetbutton_text_STRINGVAR.get(),
            state='disabled'
        )
        # POSITION - |Recommencer|
        self.reset_button.place(x=425, y=325, anchor='nw') #Côté droit de l'app

        # ==========================
        # SAVE BUTTON - |Sauvegarder la progression|
        # ==========================
        # VAR - |Sauvegarder la progression|
        Savebutton_text_STRINGVAR = tk.StringVar(value='Sauvegarder la progression')

        # INFORMATIONS - |Sauvegarder la progression|
        self.save_button = ttk.Button(
            self.button_frame,
            command=self.save_button_func,          #COMMAND - save_button_func()
            text=Savebutton_text_STRINGVAR.get(),
            state='disabled'
        )
        # POSITION - |Sauvegarder et fermer|
        self.save_button.pack(side='left', padx=5)

        # ==========================
        # PREVIOUS BUTTON - |<- Précédent|
        # ==========================
        # VAR - |<- Précédent|
        prev_button_STRINGVAR = tk.StringVar(value="\u2190 Précédent")
        # INFORMATIONS - |<- Précédent|
        self.prev_button = ttk.Button(
            self.root,
            text=prev_button_STRINGVAR.get(),
            command=self.prev_button_func,          #COMMAND - prev_button_func()
            state = 'disabled'
        )
        # POSITION - |<- Précédent|
        self.prev_button.place(x=20, y=275, anchor='nw')

        # ==========================
        # NEXT BUTTON - |Suivant ->|
        # ==========================
        # VAR - |Suivant ->|
        next_button_STRINGVAR = tk.StringVar(value="Suivant \u2192")
        # INFORMATIONS - |Suivant ->|
        self.next_button = ttk.Button(
            self.root,
            text=next_button_STRINGVAR.get(),
            command=self.next_button_func,          #COMMAND - next_button_func()
            state='disabled'
        )
        # POSITION - |Suivant ->|
        self.next_button.place(x=320, y=275, anchor='ne')

        self.root.bind('<Left>', lambda event: self.prev_button_func())
        self.root.bind('<Right>', lambda event: self.next_button_func())
        self.root.bind('<Return>', lambda event: self.confirm_btn_func())
        #TODO
        # Raccourcis pour oui/non
        self.root.bind('<o>', lambda event: self.keyboard_o())

        self.root.bind('<n>', lambda event: self.keyboard_n())
        # Raccourcis pour 7 choix d'hydrométéores

        self.root.bind('<Key>', lambda event: self.keyboard_num(event.keysym))
        # self.root.bind('<1>', lambda event: self.hm_cbx_var.set(value=hm_list[0]))
        # self.root.bind('<2>', lambda event: self.hm_cbx_var.set(value=hm_list[1]))
        # self.root.bind('<3>', lambda event: self.hm_cbx_var.set(value=hm_list[2]))
        # self.root.bind('<4>', lambda event: self.hm_cbx_var.set(value=hm_list[3]))
        # self.root.bind('<5>', lambda event: self.hm_cbx_var.set(value=hm_list[4]))
        # self.root.bind('<6>', lambda event: self.hm_cbx_var.set(value=hm_list[5]))
        # self.root.bind('<7>', lambda event: self.hm_cbx_var.set(value=hm_list[6]))

        #================
        # END OF WIDGETS
        #================
    #################################################################################
    #==========================
    # APP FUNCTIONS
    #==========================

    def keyboard_num(self,keysym):
        hm_list = ['Small particle',
                   'Columnar crystal',
                   'Planar crystal',
                   'Columnar/Planar crystals',
                   'Aggregate',
                   'Graupel',
                   'None']
        if keysym in "1234567":
            position = int(keysym)-1
            hm = hm_list[position]
            self.hm_cbx_var.set(value=hm)

    def keyboard_o(self):
        self.radio_var.set(value = 1)
        self.radio_btn_event()
    def keyboard_n(self):
        self.radio_var.set(value = 0)
        self.radio_btn_event()
    def autosave(self):
        if self.autosave_progress == 5:
            self.save_button_func()
            self.autosave_progress = 0
    # ==========================
    # USER LABEL (mise à jour dynamique)
    # ==========================
    def update_user_label_func(self):
        self.message_to_user_STRINGVAR.set(f"image\t\t{self.position.get()} de {self.datalenght}\n\n"
                                        f"complétée(s)\t{self.completed.get()} de {self.datalenght}")

    # ==========================
    # START BUTTON - |Commencer la tâche|
    # ==========================
    def start_button_func(self):

        #Montrer la première image
        self.show_current_image()

        #Rendre disponible les boutons de navigation et de sauvegarde
        self.prev_button.config(state='enabled')
        self.next_button.config(state='enabled')
        self.save_button.config(state='enabled')

        #On n'a plus besoin du bouton "commencer la tâche"
        self.start_button.config(state='disabled', text = 'Bon travail!')

        #Initialiser la fenêtre différement s'il y a déjà une sauvegarde à la ligne
        if self.data_manager.get_current_row()['saves'] == 0:
            self.reset_options()
            self.reset_button.config(state = 'disabled')
            self.confirm_button.config(state='enabled')
        #S'il n'y a pas de sauvegarde, on initialise normalement.
        else:
            radiov = self.data_manager.get_current_row()['radio variable']
            combov = self.data_manager.get_current_row()['hydrometeor']
            self.radio_var.set(value=int(radiov))
            self.rad_btn_1.config(state = 'disabled')
            self.rad_btn_2.config(state='disabled')
            self.hm_cbx_var.set(value=combov)
            self.hm_combobox.config(state='disabled')
            self.confirm_button.config(state='disabled')
            self.reset_button.config(state='enabled')
        self.position.set(value = self.data_manager.current_index)
        self.update_user_label_func()
    # ==========================
    # RESET BUTTON - |Recommencer| - FONCTION
    # ==========================
    def reset_button_func(self):
        #Modification du compte de photo complétée si on recommence une sélection
        if self.completed.get() > 0:
            self.completed.set(self.completed.get() - 1)

        #Update du label de suivi de la progression
        self.update_user_label_func()

        #Reset des options de l'interface
        self.reset_options()

        #Reset des données dans le dataframe
        report = self.report_func()  # from CONFIRM REPORT
        self.data_manager.update_current_row(report['radio variable'], report['hydrometeor'], -1)

        #Réactivation du bouton de confirmation
        self.confirm_button.config(state='enabled')

        #Désactivation du bouton reset
        self.reset_button.config(state='disabled')

    # ==========================
    # RESET SELECTION - FONCTION
    # ==========================
    def reset_options(self):
        # Reset and enable radio buttons
        self.radio_var.set(value=0)
        self.rad_btn_1.config(state='enabled')
        self.rad_btn_2.config(state='enabled')
        # Reset and enable combobox
        self.hm_cbx_var.set(value='Aucune Sélection')
        self.hm_combobox.config(state='enabled')

    # ==========================
    # SAVE BUTTON - |Sauvegarder la progression| - FONCTION
    # ==========================
    def save_button_func(self):
        self.data_manager.save_to_csv()

    # ==========================
    # RADIOBUTTON - FONCTION
    # ==========================
    def radio_btn_event(self):
        abl_state = ('enabled', 'disabled')
        self.hm_combobox.config(state=abl_state[self.radio_var.get()])
        if self.radio_var.get() == 1:
            self.hm_combobox.set('Aucune Sélection')

    # ==========================
    # CONFIRM BUTTON - |Confirmer sélection|
    # ==========================
    #CONFIRM REPORT
    def report_func(self):
        report = {
            'file': self.data_manager.get_current_row(),
            'radio variable': self.radio_var.get(),
            'hydrometeor': self.hm_cbx_var.get()
        }

        return report
    #APPLY REPORT TO DATAFRAME
    def confirm_btn_func(self):
        # ACTION 1 - Enregistrer le choix si les sélections sont cohérentes (image corrompu et aucun choix, ou image valide et sélection d'hm)
        if (self.hm_cbx_var.get() != 'Aucune Sélection' and int(self.radio_var.get()) == 0) or (self.hm_cbx_var.get() == 'Aucune Sélection' and int(self.radio_var.get()) == 1):
            report = self.report_func() #from CONFIRM REPORT
            #Sauvegarde des nouvelles donées dans le dataframe
            self.data_manager.update_current_row(report['radio variable'], report['hydrometeor'], 1)

            #Modification du compte d'images complétées
            if self.completed.get() < self.datalenght:
                self.completed.set(self.completed.get() + 1)

            #Modification du label pour le suivi de progression
            self.update_user_label_func()

            #Réactivation du bouton reset
            self.reset_button.config(state='enabled')

            #Désactivation du bouton de confirmation pour cette image
            self.confirm_button.config(state='disabled')

            #passage automatique à l'image suivante
            self.autosave_progress+=1
            self.autosave()
            self.next_button_func()

        else:   #si la sélection d'état de l'image et du type d'hm n'est pas valide, on ne peut pas accepter la sélection
            messagebox.showerror('Aucune Sélection',"Veuillez sélectionner un type d'hydrométéore")


    # ==========================
    # SHOW CURRENT IMAGE - FONCTION
    # ==========================
    def path_from_filename(self,filename):
        # TODO
        path = self.path_to_images
        filename = filename.replace('.png ', '')
        timestamp = filename[0:18]
        month_file = timestamp[0:4] + "_" + timestamp[5:7] + "/"
        day_file = ".".join(timestamp[0:10].split("-")) + "/"
        hour = timestamp[11:13] + "/"

        return path + month_file + day_file + hour + filename + '.png'

    def show_current_image(self):
        current_file = self.data_manager.get_current_row().name
        path = self.path_from_filename(current_file)
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((300, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

        else:
            self.image_label.config(text="Image not found")


    # ==========================
    # PREVIOUS BUTTON - |<- Précédent| - FONCTION
    # ==========================
    def prev_button_func(self):
        # Placeholder for the previous button functionality
        self.data_manager.previous()
        self.show_current_image()
        if self.data_manager.get_current_row()['saves'] == 0:
            self.reset_options()
            self.reset_button.config(state = 'disabled')
            self.confirm_button.config(state='enabled')
        else:
            radiov = self.data_manager.get_current_row()['radio variable']
            combov = self.data_manager.get_current_row()['hydrometeor']
            self.radio_var.set(value=int(radiov))
            self.rad_btn_1.config(state = 'disabled')
            self.rad_btn_2.config(state='disabled')
            self.hm_cbx_var.set(value=combov)
            self.hm_combobox.config(state='disabled')
            self.confirm_button.config(state='disabled')
            self.reset_button.config(state='enabled')

        if self.position.get() > 0:
            self.position.set(self.position.get() -1)
        self.update_user_label_func()
        #TODO
        # Changer position "image x de y"


    # ==========================
    # NEXT BUTTON - |Suivant ->| - FONCTION
    # ==========================
    def next_button_func(self):
        # Placeholder for the next button functionality
        self.data_manager.next()
        self.show_current_image()
        if self.data_manager.get_current_row()['saves'] == 0:
            self.reset_options()
            self.reset_button.config(state='disabled')
            self.confirm_button.config(state='enabled')
        else:
            radiov = self.data_manager.get_current_row()['radio variable']
            combov = self.data_manager.get_current_row()['hydrometeor']
            self.radio_var.set(value=int(radiov))
            self.rad_btn_1.config(state='disabled')
            self.rad_btn_2.config(state='disabled')
            self.hm_cbx_var.set(value=combov)
            self.hm_combobox.config(state = 'disabled')
            self.confirm_button.config(state='disabled')
            self.reset_button.config(state='enabled')
        if self.position.get() < self.datalenght:
            self.position.set(self.position.get() + 1)
        self.update_user_label_func()
        #TODO
        # Changer position "image x de y"


# if __name__ == "__main__":
#     # Assume there is a CSV file with appropriate structure
#     csv_file = 'snowflakes_test_df1.csv'
#     data_manager = DataFrameManager(csv_file)
#
#     root = tk.Tk()
#     app = MascApp(root, data_manager)
#     root.mainloop()
