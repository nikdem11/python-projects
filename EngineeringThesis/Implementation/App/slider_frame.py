import customtkinter


class SliderFrame(customtkinter.CTkFrame):
    """
    Klasa zawierająca suwak do ustawiania częstotliwości przetwarzania klatek w wideo.
    """
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = customtkinter.CTkLabel(self, text="Wybierz częstotliwość przetwarzania klatek:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Suwak do wyboru częstotliwości
        self.slider = customtkinter.CTkSlider(self, from_=1, to=20, number_of_steps=19, command=self.update_label)
        self.slider.set(1)  # Ustawienie wartości początkowej na 0.60
        self.slider.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Etykieta wyświetlająca wartość częstotlowości w czasie rzeczywistym
        self.value_label = customtkinter.CTkLabel(self, text="1")
        self.value_label.grid(row=1, column=1, padx=10, pady=10)

    def update_label(self, value):
        """
        Aktualizuje etykietę z bieżącą wartością częstotliwości.
        
        :param value: Nowa wartość częstotliwości z suwaka.
        """
        self.value_label.configure(text=f"{int(float(value))}")  # Konwersja do liczby całkowitej
    
    def get_frame_rate(self):
        """
        Zwraca aktualną częstotliwość.
        
        :return: Aktualna częstotliwość jako liczba całkowita.
        """
        value = int(self.slider.get())
        if value < 1 or value > 20:
            raise ValueError(f"Nieprawidłowa wartość częstotliwości: {value}.")
        return value

