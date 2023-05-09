import customtkinter as ctk


class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        main_text = open("data/about.txt", "r", encoding="utf-8").read()
        label = ctk.CTkLabel(self, text=main_text, font=("Rockwell", 16))
        label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        update_label = ctk.CTkLabel(self, text="Ostatnie aktualizacje:", font=("", 13))
        update_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        update_text_raw = open("data/update.txt", "r", encoding="utf-8").read()
        update_text_entry = ctk.CTkTextbox(self, width=545, height=280)
        update_text_entry.grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        update_text_entry.insert("0.0", update_text_raw)
        update_text_entry.configure(state="disabled")
