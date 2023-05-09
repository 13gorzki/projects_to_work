import os.path
import fnmatch

from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd

from modules.nike import Nike
from modules.log_report import write_log


class TaborPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        producent_label = ctk.CTkLabel(self, text="Wybierz producenta:", font=("", 15))
        producent_label.place(x=80, y=50)

        self.producent_choose = ctk.StringVar()
        producent_button_nike = ctk.CTkRadioButton(
            self,
            text="Nike",
            value="nike",
            variable=self.producent_choose,
            command=self.selected_brand,
        )
        producent_button_nike.place(x=110, y=100)

        producent_button_adidas = ctk.CTkRadioButton(
            self,
            text="adidas",
            value="adidas",
            variable=self.producent_choose,
            command=self.selected_brand,
        )
        producent_button_adidas.place(x=110, y=130)

        self.file_label = ctk.CTkLabel(self, text="Wybierz źródło:", font=("", 15))

        self.selected_nike = ctk.StringVar(value="Wybierz...")
        self.qty_nike = ctk.CTkComboBox(
            self,
            variable=self.selected_nike,
            values=["Pojedynczy plik", "Wiele plików"],
            state="readonly",
            command=self.qty_file,
        )

        self.label_adidas = ctk.CTkLabel(
            self,
            text="W chwili obecnej adidas jest niedostępny",
            text_color="red",
            font=("", 20),
        )

        self.button_once_file = ctk.CTkButton(
            self, text="Wybierz plik", command=self.select_file, font=("", 13)
        )
        self.button_multi_file = ctk.CTkButton(
            self, text="Wybierz folder", command=self.select_folder, font=("", 13)
        )

        self.selected_path = ctk.StringVar()
        self.selected_folder = ctk.StringVar()

        italic_font = ctk.CTkFont(slant="italic", size=13)
        self.selected_label_file = ctk.CTkLabel(
            self, text="Lokalizacja wybranego pliku: ", font=("", 13)
        )
        self.selected_path_entry_file = ctk.CTkEntry(
            self, textvariable=self.selected_path, width=620, state="readonly"
        )
        self.selected_label_folder = ctk.CTkLabel(
            self, text="Lokalizacja wybranego folderu: ", font=("", 13)
        )
        self.selected_path_entry_folder = ctk.CTkEntry(
            self, textvariable=self.selected_folder, width=620, state="readonly"
        )
        self.create_tabor_button = ctk.CTkButton(
            self, text="Utwórz i zapisz", command=self.convert_tabor
        )

        self.info_label = ctk.CTkLabel(
            self,
            text="W folderze mogą znajdować się tylko źródłowe pliki z nike.net",
            text_color="yellow",
            font=("", 11),
        )
        self.error_label = ctk.CTkLabel(
            self, text="BŁĄD !!!", fg_color="red", font=("", 20)
        )

        self.progress_bar_label = ctk.CTkLabel(
            self, text="Przetwarzanie", font=("", 13)
        )
        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
        self.progress_bar.set(0)

    def selected_brand(self):
        selected_brand = self.producent_choose.get()
        if selected_brand == "nike":
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.label_adidas.place_forget()
            self.selected_label_file.place_forget()
            self.selected_label_folder.place_forget()
            self.selected_path_entry_folder.place_forget()
            self.selected_path_entry_file.place_forget()
            self.create_tabor_button.place_forget()
            self.info_label.place_forget()
            self.file_label.place(x=80, y=180)
            # self.file_label.grid(row=3, column=0, sticky='nw')
            self.qty_nike.place(x=110, y=220)
            # self.qty_nike.grid(row=4, column=1, sticky='nw')
        if selected_brand == "adidas":
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.qty_nike.place_forget()
            self.button_multi_file.place_forget()
            self.button_once_file.place_forget()
            self.selected_label_file.place_forget()
            self.selected_label_folder.place_forget()
            self.selected_path_entry_folder.place_forget()
            self.selected_path_entry_file.place_forget()
            self.create_tabor_button.place_forget()
            self.info_label.place_forget()
            self.file_label.place_forget()
            self.label_adidas.place(x=110, y=220)
            # self.label_adidas.grid(row=5, column=2, sticky='nw')

    def qty_file(self, qty):
        qty_selected = self.selected_nike.get()
        if qty_selected == "Pojedynczy plik":
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.button_multi_file.place_forget()
            self.selected_label_file.place_forget()
            self.selected_label_folder.place_forget()
            self.selected_path_entry_folder.place_forget()
            self.selected_path_entry_file.place_forget()
            self.create_tabor_button.place_forget()
            self.info_label.place_forget()
            self.button_once_file.place(x=110, y=270)
            # self.button_once_file.grid(row=4, column=1, sticky='nw')

        if qty_selected == "Wiele plików":
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.button_once_file.place_forget()
            self.selected_label_file.place_forget()
            self.selected_label_folder.place_forget()
            self.selected_path_entry_folder.place_forget()
            self.selected_path_entry_file.place_forget()
            self.create_tabor_button.place_forget()
            self.info_label.place_forget()
            self.button_multi_file.place(x=110, y=270)
            # self.button_multi_file.grid(row=3, column=2, sticky='nw')

    def select_file(self):
        file_types = (("CSV (rozdzielany przecinkami)", "*.csv"), ("All files", "*.*"))
        file_path = filedialog.askopenfilename(
            title="Wybierz plik", filetypes=file_types
        )
        if file_path:
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.selected_path.set(file_path)
            self.selected_folder.set("")
            # self.selected_path_entry_file.configure(textvariable=self.selected_path.get())
            self.selected_label_folder.place_forget()
            self.selected_label_file.place(x=80, y=320)
            # self.selected_label_file.grid(row=4, column=3, sticky='nw')
            self.selected_path_entry_folder.place_forget()
            self.selected_path_entry_file.place(x=260, y=320)
            # self.selected_path_entry_file.grid(row=5, column=4, sticky='nw')
            self.create_tabor_button.place_forget()
            self.info_label.place_forget()
            self.create_tabor_button.place(x=110, y=400)
            # self.create_tabor_button.grid(row=4, column=3, sticky='nw')

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Wybierz folder")
        if folder_path:
            self.progress_bar_label.place_forget()
            self.progress_bar.place_forget()
            self.selected_folder.set(folder_path)
            self.selected_path.set("")
            self.selected_path_entry_folder.configure(
                textvariable=self.selected_folder.get()
            )
            self.selected_label_file.place_forget()
            self.selected_label_folder.place(x=80, y=320)
            # self.selected_label_folder.grid(row=4, column=3, sticky='nw')
            self.selected_path_entry_file.place_forget()
            self.selected_path_entry_folder.place(x=260, y=320)
            self.info_label.place(x=270, y=350)
            # self.selected_path_entry_folder.grid(row=6, column=5, sticky='nw')
            self.create_tabor_button.place_forget()
            self.create_tabor_button.place(x=110, y=400)
            # self.create_tabor_button.grid(row=5, column=4, sticky='nw')

    def convert_tabor(self):
        self.progress_bar.place(x=200, y=460)
        self.progress_bar_label.place(x=260, y=430)
        save_file_name = filedialog.asksaveasfilename(
            title="Save file as...",
            filetypes=[("CSV (rozdzielany przecinkami)", "*.csv")],
            defaultextension=".csv",
            initialfile="Tabor_NIKE",
        )
        from_file = self.selected_path.get()
        from_folder = self.selected_folder.get()

        try:
            if from_file:
                self.single_tabor(from_file, save_file_name)
                # write_log(
                #     "tabor_nike",
                #     20,
                #     f"Tabor wygenerowany z {from_file} -> {save_file_name}",
                # )
            elif from_folder:
                self.multiple_tabor(from_folder, save_file_name)
                # write_log(
                #     "tabor_nike",
                #     20,
                #     f"Tabor wygenerowany z {from_folder} -> {save_file_name}",
                # )
            else:
                self.error_label.place(x=130, y=650)
        except Exception as e:
            write_log("tabor_nike", 40, f"Convert Error {e}")

        if os.path.isfile(save_file_name):
            messagebox.showinfo("Informacja", "Plik utworzony poprawnie")
        else:
            messagebox.showwarning(
                "Błąd",
                "Uwaga, coś poszło nie tak. Skontaktuj się z autorem, lub zrób plik ręcznie",
            )

    def single_tabor(self, from_file, to_file):
        nike = Nike()
        tabor = nike.tabor_nike(from_file)
        self.progress_bar.set(1)
        self.progress_bar.update_idletasks()
        if ".csv" not in to_file:
            output_file = to_file + ".csv"
        else:
            output_file = to_file
        tabor.to_csv(output_file, sep=";", index=False, encoding="utf-8", decimal=",")

    def multiple_tabor(self, from_path, to_file):
        nike = Nike()
        if from_path and to_file:
            df = pd.DataFrame()
            from_path = from_path + "/"
            files_to_log = ""
            qty_file = len(
                [f for f in os.listdir(from_path) if fnmatch.fnmatch(f, "*.csv")]
            )
            file_no = 1
            for file_name in os.listdir(from_path):
                if fnmatch.fnmatch(file_name, "*.csv"):
                    file = from_path + file_name
                    df_nike = nike .tabor_nike(file)
                    df = pd.concat([df, df_nike])
                    files_to_log += file + "\n"
                    self.progress_iter_step(file_no, qty_file)
                    file_no += 1
                else:
                    write_log("nike_from_folder", 30, f"File {file_name} wrong format")
            write_log("nike_from_folder", 10, f"import from file :\n{files_to_log}")

            if ".csv" not in to_file:
                output_file = to_file + ".csv"
            else:
                output_file = to_file
            df.to_csv(output_file, sep=";", index=False, encoding="utf-8", decimal=",")

    def progress_iter_step(self, file_no, qty_no):
        iter_step = file_no/qty_no
        self.progress_bar.set(iter_step)
        self.progress_bar.update_idletasks()
