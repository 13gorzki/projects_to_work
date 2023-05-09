import customtkinter as ctk


class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        main_text = open("data/main_text.txt", "r", encoding="utf-8").read()
        label = ctk.CTkLabel(self, text=main_text, font=("Rockwell", 20))
        label.pack(expand=True)
