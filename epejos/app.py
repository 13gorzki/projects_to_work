""" zmiana nazwy z tabor converter na epejos (tworca konia trojańskiego)"""
from tkinter import messagebox
import customtkinter as ctk


from page.about import AboutPage
from page.start import StartPage
from page.tabor import TaborPage


class TaborConverter(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("Epejos")
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create menu frame
        self.menu_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.menu_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(
            self.menu_frame, text="Epejos", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tabor_button = ctk.CTkButton(
            self.menu_frame, text="Tabor", command=self.show_tabor_page
        )
        self.tabor_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.kartoteka_button = ctk.CTkButton(
            self.menu_frame, state="disabled", text="Kartoteka (niedostępne)"
        )
        self.kartoteka_button.grid(row=2, column=0, padx=20, pady=10)

        self.help_optionemenu_var = ctk.StringVar(value="Help")
        self.help_optionemenu = ctk.CTkComboBox(
            self.menu_frame,
            values=["Welcome", "About..."],
            variable=self.help_optionemenu_var,
            command=self.help_page,
        )
        self.help_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))

        # create page frame
        self.page_frame = ctk.CTkFrame(self)
        self.page_frame.grid(
            row=0, rowspan=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.page_frame.grid_columnconfigure(0, weight=1)
        self.page_frame.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, TaborPage, AboutPage):
            frame = F(self.page_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky='nsew')
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        self.c_label = ctk.CTkLabel(self, text="©ggorzki 2023", font=("", 9))
        self.c_label.grid(row=3, column=1, padx=10, sticky="se")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_tabor_page(self):
        self.show_frame(TaborPage)
        self.help_optionemenu_var.set("Help")

    def help_page(self, page):
        if self.help_optionemenu_var.get() == "Welcome":
            self.show_frame(StartPage)
        elif self.help_optionemenu_var.get() == "About...":
            self.show_frame(AboutPage)
        else:
            self.help_optionemenu_var.set("Help")
            messagebox.showinfo("Informacja", "Chwilowo niedostępne")


app = TaborConverter()
app.mainloop()
