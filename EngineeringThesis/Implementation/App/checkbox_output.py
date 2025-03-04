import customtkinter


class CheckboxOutput(customtkinter.CTkFrame):
    """
    Klasa odpowiedzialna za stworzenie sekcji wyboru typu pliku wyjściowego w interfejsie graficznym.
    Użytkownik może wybrać jeden z dwóch dostępnych typów: "Pliki wideo" lub "Zdjęcia".
    """
    def __init__(self, master):
        """
        Inicjalizuje ramkę zawierającą widżety umożliwiające wybór typu pliku wyjściowego.

        :param master: Referencja do nadrzędnego widżetu (głównego okna aplikacji).
        """
        super().__init__(master)
        
        # Etykieta opisująca sekcję wyboru pliku wyjściowego
        self.label = customtkinter.CTkLabel(self, text="Wybierz rodzaj pliku wyjściowego:")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.selected_output = customtkinter.StringVar()

        self.checkbox_1 = customtkinter.CTkRadioButton(self, text="Pliki wideo", variable=self.selected_output, value="video")
        self.checkbox_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_2 = customtkinter.CTkRadioButton(self, text="Zdjęcia", variable=self.selected_output, value="photo")
        self.checkbox_2.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="e")
    
    def get_selected_output(self):
        """
        Zwraca aktualnie wybrany typ pliku wyjściowego.

        :return: Wartość zmiennej `selected_output`, która wskazuje na wybrany typ pliku.
        """

        return self.selected_output.get()