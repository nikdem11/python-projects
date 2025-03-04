import customtkinter


class SliderThreshold(customtkinter.CTkFrame):
    """
    Klasa zawierająca suwak do ustawiania progu detekcji piorunów (0.5 do 0.9).
    """
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Etykieta wyświetlająca wartość progu
        self.label = customtkinter.CTkLabel(self, text="Wybierz próg detekcji:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Suwak do wyboru progu
        self.slider = customtkinter.CTkSlider(self, from_=0.5, to=0.9, number_of_steps=8, command=self.update_label)
        self.slider.set(0.6)  # Ustawienie wartości początkowej na 0.6
        self.slider.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Etykieta wyświetlająca wartość progu w czasie rzeczywistym
        self.value_label = customtkinter.CTkLabel(self, text="0.6")
        self.value_label.grid(row=1, column=1, padx=10, pady=10)

    def update_label(self, value):
        """
        Aktualizuje etykietę z bieżącą wartością progu.
        
        :param value: Nowa wartość progu z suwaka.
        """
        self.value_label.configure(text=f"{value:.2f}")
    
    def get_threshold(self):
        """
        Zwraca aktualny próg detekcji jako wartość float.
        
        :return: Aktualny próg.
        """
        value = self.slider.get()
        if value < 0.5 or value > 0.9:
            raise ValueError(f"Nieprawidłowa wartość progu: {value}.")
        return value
