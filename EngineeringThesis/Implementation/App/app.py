import os
import customtkinter
import time
import json
import cv2
from tkinter import filedialog
from checkbox_model import CheckboxModel
from checkbox_output import CheckboxOutput
from annotation import Annotation
from slider_threshold import SliderThreshold
from slider_frame import SliderFrame


class App(customtkinter.CTk):
    """
    Główna klasa aplikacji, zawierająca GUI do obsługi systemu wykrywania wyładowań atmosferycznych.
    Oparta na bibliotece customtkinter.
    """

    def __init__(self):
        """
        Inicjalizuje okno aplikacji, deklaruje wszystkie elementy GUI oraz ładuje konfigurację modeli.
        """
        super().__init__()

        # Wczytanie konfiguracji modeli z pliku JSON
        self.models_config = self.load_models_config("App/models_config.json")

        # Inicjalizacja okna aplikacji
        self.title("Wykrywanie wyładowań atmosferycznych")
        self.center_window()
        self.grid_columnconfigure(0, weight=1)  # Rozciąganie kolumny dla wypełnienia okna
        self.grid_rowconfigure(0, weight=1)  # Rozciąganie wiersza dla wypełnienia okna
 
        self.video_path = None
        self.model_choice = None
        
        # Przycisk ładowania wideo
        self.button1 = customtkinter.CTkButton(self, text="Załaduj wideo", command=self.button1_callback)
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Przycisk wyboru folderu docelowego
        self.button2 = customtkinter.CTkButton(self, text="Wybierz folder docelowy", command=self.button2_callback)
        self.button2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
       
        # CheckBox do wyboru modelu
        self.checkbox_model = CheckboxModel(self)
        self.checkbox_model.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.output_choice = None
        self.destination_folder = None

        # CheckBox do wyboru typu wyjścia
        self.checkbox_output = CheckboxOutput(self)
        self.checkbox_output.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        # Slider do wyboru progu detekcji
        self.slider_threshold = SliderThreshold(self)
        self.slider_threshold.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Slider do wyboru częstotliwości przetwarzania klatek w wideo
        self.slider_frame = SliderFrame(self)
        self.slider_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Przycisk rozpoczęcia anotacji
        self.button3 = customtkinter.CTkButton(self, text="Rozpocznij anotację", command=self.button3_callback)
        self.button3.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Etykiety informacyjne dla wideo i folderu docelowego
        self.video_label = customtkinter.CTkLabel(self, text="Wideo: nie wybrano")
        self.video_label.grid(row=7, column=0, padx=10, pady=10, sticky="nsw")

        self.destination_label = customtkinter.CTkLabel(self, text="Folder docelowy: nie wybrano")
        self.destination_label.grid(row=8, column=0, padx=10, pady=10, sticky="nsw")


    def button1_callback(self):
        """
        Obsługuje wybór pliku wideo przez użytkownika.
        Waliduje poprawność wybranego pliku.
        """
        file_types = [("Video files", "*.mp4 *.avi *.mkv *.mov")]
        # Otwieranie okna dialogowego do wyboru pliku
        temp_video = filedialog.askopenfilename(title="Wybierz plik wideo", filetypes=file_types)  # Zabezpieczenie przed brakiem wyboru wideo w oknie dialogowym
        # Sprawdzenie, czy plik został wybrany i jest poprawny
        if temp_video and self.validate_video(temp_video):  
            self.video_path = temp_video
            print(f"Załadowano wideo: {self.video_path}")
            self.video_label.configure(text=f"Wideo: {os.path.basename(self.video_path)}")            
        else:
            print("Nie wybrano poprawnego pliku.")


    def button2_callback(self):
        """
        Obsługuje wybór folderu docelowego przez użytkownika.
        Waliduje poprawność wybranego folderu.
        """
        # Otwieranie okna dialogowego do wyboru folderu
        temp_folder = filedialog.askdirectory(title="Wybierz folder docelowy")  # Zabezpieczenie przed brakiem wyboru folderu w oknie dialogowym
        # Sprawdzenie, czy folder został wybrany i jest poprawny
        if temp_folder and self.validate_folder(temp_folder):
            self.destination_folder = temp_folder
            print(f"Wybrano folder docelowy: {self.destination_folder}")
            self.destination_label.configure(text=f"Folder docelowy: {os.path.basename(self.destination_folder)}")
        else:
            print("Nie wybrano poprawnego folderu.")


    def button3_callback(self):
        """
        Rozpoczyna proces anotacji, wykorzystując wybrane wideo, model i folder docelowy.
        Obsługuje różne przypadki błędów, np. brak wyboru pliku, modelu lub folderu.
        """
        # Sprawdzenie, czy wymagane dane wejściowe są dostępne
        if self.video_path and self.destination_folder:
            # Pobranie wyborów użytkownika dotyczących modelu, wyjścia, thresholdu i klatkowania
            self.model_choice = self.checkbox_model.get_selected_model()
            self.output_choice = self.checkbox_output.get_selected_output()
            threshold = self.slider_threshold.get_threshold()
            frame_rate = self.slider_frame.get_frame_rate()

            if self.model_choice and self.output_choice:  
                # Pobranie szczegółów wybranego modelu z konfiguracji
                model_config = self.models_config["models"].get(self.model_choice)
                if model_config:
                    model_name = model_config["name"]
                    print(f"Wybrano model: {model_name} - {model_config['description']}")
                else:
                    print(f"Nie znaleziono konfiguracji dla modelu: {self.model_choice}")
                    return
                
                # Budowanie ścieżki do modelu
                model_path = f"../Models/{model_name}.keras"            
                print(f"Rozpoczynam anotowanie pliku: {self.video_path}\n")
                try:
                    # Inicjalizacja procesu anotacji
                    a = Annotation(self.video_path, model_path, self.destination_folder, threshold, frame_rate)

                    start_time = time.time()
                    # Wybór trybu anotacji na podstawie wyboru użytkownika
                    if self.output_choice == "video":
                        a.extract_lightning_clips()
                    if self.output_choice == "photo":
                        a.extract_lightning_frames()
                        
                    end_time = time.time()

                    # Wyświetlenie informacji o sukcesie i czasie trwania anotacji
                    print(f"Wyładowania atmosferyczne z pliku {os.path.basename(self.video_path)} zostały pomyślnie anotowane.")
                    print(f"Czas anotacji: {(end_time - start_time):.1f} s.\n")
                    self.show_result_popup("Anotacja zakończona sukcesem.")
                except Exception as e:
                    print(f"Anotacja nie powiodła się. Błąd: {e}")

            elif not self.model_choice:
                print("Brak wybranego modelu.")
            elif not self.output_choice:
                print("Brak wybranego rodzaju pliku wyjściowego.")
        
        elif not self.video_path:
            print("Brak załadowanego wideo do anotacji.")
        elif not self.destination_folder:
            print("Brak wybranego folderu docelowego.")


    def show_result_popup(self, message):
        """
        Wyświetla okno pop-up z wynikami anotacji.
        
        :param message: Treść wiadomości wyświetlanej w oknie
        """
        # Tworzenie okna pop-up
        popup = customtkinter.CTkToplevel(self)
        popup.title("Wynik anotacji")
        popup.transient(self)  # Powiązanie z oknem głównym
        
        # Obliczanie pozycji pop-upu względem okna głównego
        self.update_idletasks()  # Aktualizacja rozmiarów i pozycji okna głównego
        x_popup = self.winfo_rootx() + (self.winfo_width() // 2) - 225
        y_popup = self.winfo_rooty() + (self.winfo_height() // 2) - 30

        # Ustawienie pozycji i rozmiaru pop-upu
        popup.geometry(f"450x60+{x_popup}+{y_popup}")

        # Dodanie etykiety z wiadomością w oknie pop-up
        result_label = customtkinter.CTkLabel(popup, text=message)
        result_label.pack(padx=20, pady=20)

        # Ustawienie modalności (blokada interakcji z głównym oknem, do zamknięcia pop-upu)
        popup.grab_set()

    
    def load_models_config(self, config_name):
        """
        Wczytuje konfigurację modeli z pliku JSON.

        :param config_name: Nazwa pliku JSON z konfiguracją modeli.
        :return: Słownik z konfiguracją modeli.
        """
        # Pobranie ścieżki folderu, w którym znajduje się ten skrypt
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # config_path = os.path.join(base_dir, config_name)
        try:
            # Wczytanie zawartości pliku JSON
            with open(config_name, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Błąd wczytywania konfiguracji modeli: {e}")
            return {"models": {}}
        
    
    def validate_video(self, file_path):
        """
        Waliduje plik wideo, sprawdzając, czy jest poprawnie odczytywany.

        :param file_path: Ścieżka do pliku wideo.
        :return: Flaga walidacji pliku wideo.
        """
        # Próba otwarcia pliku wideo
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            video.release()
            return False
        video.release()
        return True
    

    def validate_folder(self, folder_path):
        """
        Waliduje folder docelowy, sprawdzając jego istnienie i prawa zapisu.

        :param folder_path: Ścieżka do folderu docelowego.
        :return: Flaga walidacji folderu.
        """
        # Sprawdzenie, czy folder istnieje
        if not os.path.exists(folder_path):
            print("Wybrany folder nie istnieje.")
            return False
        # Sprawdzenie praw zapisu w folderze
        if not os.access(folder_path, os.W_OK):
            print("Brak uprawnień do zapisu w wybranym folderze.")
            return False
        return True
    

    def center_window(self):
        """
        Ustawia główne okno programu w centrum monitora.
        """
        # Pobranie wymiarów ekranu
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Ustawienie wymiarów okna
        window_width = 500  
        window_height = 730  
        
        # Obliczenie pozycji x i y, aby okno było wycentrowane
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        # Ustawienie pozycji okna
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


