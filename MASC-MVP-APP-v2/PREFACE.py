import tkinter as tk
from tkinter import ttk
from APP import DataFrameManager
from APP import MascApp
import os

class PrefaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MASC MVP APP")
        self.root.geometry("300x200")
        self.path_to_dataframes = "../../DATAFRAMES/MVP_setup_dataframes/"
        self.csv_files = self.load_paths()

        self.label = ttk.Label(self.root, text="Sélectionnez une tempête:")
        self.label.pack(pady=10)

        self.df_combobox = ttk.Combobox(self.root, values=self.csv_files)
        self.df_combobox.pack(pady=10)

        self.load_button = ttk.Button(self.root, text="Charger l'interface", command=self.load_dataframe)
        self.load_button.pack(pady=10)

    def load_paths(self):
        march_paths = os.listdir(self.path_to_dataframes+"/march/filtered/")
        april_paths = os.listdir(self.path_to_dataframes+"/april/filtered/")
        paths = []
        for item in march_paths:
            if "._" not in item:
                paths.append(item)
        for item in april_paths:
            if "._" not in item:
                paths.append(item)
        return paths
    def load_dataframe(self):
        selected_file = self.df_combobox.get()
        month = selected_file.split("_")[1]+"/"
        if selected_file:
            data_manager = DataFrameManager(self.path_to_dataframes+month+"filtered/"+selected_file)
            self.root.destroy()
            self.launch_main_app(data_manager)
        else:
            tk.messagebox.showwarning("ERREUR", "Veuillez choisir une base de données.")

    def launch_main_app(self, data_manager):
        main_root = tk.Tk()
        app = MascApp(main_root, data_manager)
        main_root.mainloop()

if __name__ == "__main__":
    preface_root = tk.Tk()
    preface_app = PrefaceApp(preface_root)
    preface_root.mainloop()