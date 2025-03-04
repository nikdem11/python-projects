import customtkinter


class CheckboxModel(customtkinter.CTkFrame):
    """
    Klasa odpowiedzialna za stworzenie sekcji wyboru modelu w interfejsie graficznym.
    """
    def __init__(self, master):
        """
        Inicjalizuje ramkę zawierającą widżety umożliwiające wybór modelu.

        :param master: Referencja do nadrzędnego widżetu (głównego okna aplikacji).
        """
        super().__init__(master)
        
        # Etykieta opisująca sekcję wyboru modelu
        self.label = customtkinter.CTkLabel(self, text="Wybierz model:")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.selected_model = customtkinter.StringVar()

        self.checkbox_1 = customtkinter.CTkRadioButton(self, text="Model 1", variable=self.selected_model, value="model1")
        self.checkbox_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_2 = customtkinter.CTkRadioButton(self, text="Model 2", variable=self.selected_model, value="model2")
        self.checkbox_2.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_3 = customtkinter.CTkRadioButton(self, text="Model 3", variable=self.selected_model, value="model3")
        self.checkbox_3.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
    
    def get_selected_model(self):
        """
        Zwraca nazwę aktualnie wybranego modelu.

        :return: Wartość zmiennej `selected_model`, która wskazuje na wybrany model.
        """
        return self.selected_model.get()