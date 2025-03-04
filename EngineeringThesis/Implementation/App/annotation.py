import cv2
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import numpy as np


class Annotation():
    """
    Klasa odpowiedzialna za wykrywanie wyładowań atmosferycznych w wideo,
    generowanie klipów wideo lub obrazów oraz zapis wyników.
    """

    def __init__(self, video_path, model_path, destination_folder, threshold_detection, frame_rate):
        """
        Inicjalizuje obiekt klasy Annotation z podstawowymi parametrami.
        
        :param video_path: Ścieżka do pliku wideo do analizy.
        :param model_path: Ścieżka do modelu uczenia maszynowego do wykrywania.
        :param destination_folder: Folder docelowy do zapisu wyników.
        :param threshold: Wartość progu przy detekcji wyładowania.
        :param frame_rate: Wartość określająca częstotliwość wyodrębniania klatek z wideo.
        """
        super().__init__()
        self.video_path = video_path
        self.model_path = model_path
        self.destination_folder = destination_folder
        self.threshold = threshold_detection
        self.frame_rate = frame_rate
        self.model = None  # Model zostanie załadowany dynamicznie
        self.video = None  # Obiekt wideo zostanie zainicjalizowany podczas przetwarzania


    def find_ranges(self):
        """
        Analizuje wideo w celu zidentyfikowania zakresów czasowych zawierających wyładowania atmosferyczne.
        Wykorzystuje model predykcji do oceny każdej klatki.

        :return: Lista zakresów czasowych, w których wykryto wyładowania atmosferyczne.
        """

        frame_count = 0
        fps = self.video.get(cv2.CAP_PROP_FPS)  # Odczyt liczby klatek na sekundę z wideo
        frame_interval = int(fps / self.frame_rate)  # Odstęp między sprawdzanymi klatkami
        current_range_start = None  
        lightning_ranges = [] 
        frames_info = {}

        while True:
            # Pobranie kolejnej klatki z wideo
            ret, frame = self.video.read()
            
            # Zakończenie, jeśli brak klatek
            if not ret:
                # Zamknięcie otwartego zakresu przy końcu wideo
                if current_range_start is not None:
                    end_time = frame_count / fps
                    frames_info["koniec_pliku"] = np.float32(100.00)  # Pewność domyślna 
                    lightning_ranges.append((current_range_start, end_time))
                break

            # Sprawdzanie klatki w określonych odstępach czasowych
            if frame_count % frame_interval == 0:
                # Predykcja modelu dla bieżącej klatki
                prediction = self.frame_prediction(frame)
                
                # Sprawdzenie, czy wykryto wyładowanie (wartość mniejsza od odwrotności thresholdu)
                if prediction[0] < 1 - self.threshold:
                    if current_range_start is None:  # Otwarcie nowego zakresu
                        current_range_start = frame_count / fps  
                        range_name = f"pocz_{current_range_start:.2f}_s"
                        frames_info[range_name] = ((1 - prediction[0])*100)  # Zapis początku zakresu wraz z pewnością
                elif prediction[0] > self.threshold:  # brak pioruna, czyli pewność więsza od thresholdu
                    if current_range_start is not None:  # Zamknięcie bieżącego zakresu
                        end_time = frame_count / fps  
                        range_name = f"kon_{end_time:.2f}_s"
                        frames_info[range_name] = ((prediction[0])*100) 
                        lightning_ranges.append((current_range_start, end_time))  # Zapis zakresu do listy
                        current_range_start = None   

            frame_count += 1

        # Generowanie pliku opisowego z wynikami
        self.generate_desc(frames_info, True)  

        if lightning_ranges:
            print(f"Zakresy czasowe z piorunami: {lightning_ranges}")
        else:
            print("Nie wykryto żadnych wyładowań atmosferycznych w podanym wideo.")
        
        return lightning_ranges


    def extract_lightning_clips(self):
        """
        Ekstrahuje fragmenty wideo na podstawie zakresów czasowych, w których wykryto wyładowania atmosferyczne.
        """
        try:      
            self.annotation_preparation()

            # Znalezienie zakresów czasowych z wyładowaniami
            lightning_ranges = self.find_ranges()

            # Pobranie liczby klatek
            fps = self.video.get(cv2.CAP_PROP_FPS)
            # Definiowanie kodeka wideo dla zapisu
            fourcc = cv2.VideoWriter_fourcc(*'XVID')

            for idx, (start_time, end_time) in enumerate(lightning_ranges):
                # Rozszerzenie zakresu czasowego o 1 sekundę z każdej strony
                start_time = max(0, start_time - 1)
                end_time = end_time + 1
                
                # Ustawienie pozycji odtwarzania wideo na początek zakresu
                self.video.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
                output_path = os.path.join(self.destination_folder, f"lightning_clip_{idx:04d}.avi")
                
                # Inicjalizacja obiektu do zapisu wideo
                out = cv2.VideoWriter(
                    output_path, 
                    fourcc, 
                    fps, 
                    (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
                
                while True:
                    current_time = self.video.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    # Wyjście z pętli, jeśli przekroczono czas końcowy zakresu
                    if current_time > end_time:
                        break
                    ret, frame = self.video.read()
                    # Wyjście z pętli, jeśli brak klatek (koniec wideo)
                    if not ret:
                        break
                    out.write(frame)  # Zapis bieżącej klatki 

                out.release()  # Zwolnienie zasobów zapisujących wideo
                print(f"Zapisano klip: {output_path} do folderu: {self.destination_folder}")

            self.video.release()  # Zwolnienie zasobów wideo

        except Exception as e:
            raise RuntimeError(f"Błąd podczas przetwarzania klatek: {e}")


    def extract_lightning_frames(self):
        """
        Ekstrahuje pojedyncze klatki z wideo, które zawierają wykryte przez model
        wyładowania atmosferyczne.
        """
        try:
            self.annotation_preparation()

            frame_count = 0
            saved_count = 0
            fps = self.video.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps / self.frame_rate)
            frames_info = {}

            while True:
                # Przechwycenie kolejnej klatki z wideo
                ret, frame = self.video.read()
                
                # Zakończenie, jeśli brak klatek
                if not ret:
                    break

                # Analizowanie klatek w określonych odstępach czasowych
                if frame_count % frame_interval == 0:          
                    prediction = self.frame_prediction(frame)
                    
                    # Sprawdzenie, czy model wykrył piorun 
                    if prediction[0] < 1 - self.threshold:
                        # Generowanie nazwy pliku dla zapisanej klatki
                        file_name = f"lightning_frame_{saved_count:04d}.jpg"
                        # Obliczanie i zapis pewności detekcji
                        frames_info[file_name] = ((1 - prediction[0])*100)  
                        
                        frame_path = os.path.join(self.destination_folder, file_name)
                        
                        # Zapis bieżącej klatki jako pliku obrazu
                        cv2.imwrite(frame_path, frame)  
                        saved_count += 1
                        
                frame_count += 1

            # Generowanie pliku opisowego z wynikami
            self.generate_desc(frames_info, False)
    
            self.video.release()  # Zwolnienie zasobów wideo
            print(f"Zapisano {saved_count} klatek z klipu do folderu: {self.destination_folder}")

        except Exception as e:
            raise RuntimeError(f"Błąd podczas przetwarzania klatek: {e}")


    def annotation_preparation(self):
        """
        Przygotowuje środowisko do anotacji, m.in. otwiera wideo i ładuje model.
        """
        # Utworzenie podfolderu w którym będą zapisywane anotacje
        self.destination_folder = self.create_subfolder()

        # Otwarcie pliku wideo
        self.video = cv2.VideoCapture(self.video_path)
        
        # Ładowanie modelu        
        self.model = tf.keras.models.load_model(self.model_path)


    def frame_prediction(self, frame):
        """
        Dokonuje predykcji na podstawie podanej klatki wideo.
        
        :param frame: Klatka obrazu wideo w formacie OpenCV.
        :return: Wynik predykcji modelu TensorFlow.
        """
        # Skalowanie klatki do wymiarów obsługiwanych przez model
        img_height, img_width = 224, 224 
        resized_frame = cv2.resize(frame, (img_width, img_height))
        batch_frame = tf.expand_dims(resized_frame, 0)  # Tworzenie batcha

        # Predykcja modelu
        return self.model.predict(batch_frame, verbose=0)  # verbose = 0 wyłącza wyświetlanie kroków

    
    def create_subfolder(self):
        """
        Tworzy podfolder w folderze docelowym, gdzie zapisywane będą wyniki.
        
        :return: Ścieżka do stworzonego podfolderu.
        """
        # Pobranie nazwy pliku wideo (bez rozszerzenia)
        video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        # Pobranie nazwy pliku modelu (bez rozszerzenia)
        model_name = os.path.splitext(os.path.basename(self.model_path))[0]
        # Generowanie ścieżki do podfolderu w folderze docelowym
        subfolder_path = os.path.join(self.destination_folder, f"{video_name}_{model_name}_{self.threshold}_{self.frame_rate}")
        
        # Sprawdzenie, czy podfolder istnieje
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)  # Tworzenie nowego podfolderu
            print(f"Utworzono podfolder: {subfolder_path}")
        else:
            print(f"Podfolder już istnieje: {subfolder_path}")
        
        return subfolder_path


    def generate_desc(self, frames_info, isVideo):
        """
        Generuje plik tekstowy z opisem wyników anotacji.

        :param frames_info: Informacje o klatkach i ich predykcji.
        :param isVideo: Flaga wskazująca, czy opis dotyczy klipów wideo, czy obrazów.
        """
        # Ustalanie nazwy pliku opisowego w zależności od trybu anotacji
        file_name = "video_annotation_desc.txt" if isVideo else "photo_annotation_desc.txt" 
        # Generowanie pełnej ścieżki do pliku opisowego   
        desc_file_path = os.path.join(self.destination_folder, file_name)

        # Tworzenie i zapis treści pliku opisowego
        with open(desc_file_path, "w") as file: 
            file.write(f"Model dokonujący predykcji: {os.path.basename(self.model_path)}\n")
            file.write(f"Plik źródłowy: {self.video_path}\n")

            if isVideo:
                file.write(f"Liczba wyciętych nagrań: {(len(frames_info)/2):.0f}\n")
            else:                           
                file.write(f"Liczba anotowanych klatek: {len(frames_info)}\n") 

            file.write(f"----------------------------------\n")
            file.write("Szczegóły anotacji:\n")

            for file_name, confidence in frames_info.items():
                    file.write(f"Klatka: {file_name} | Pewność: {confidence.item():.2f}%\n")
            
        print(f"Utworzono plik z opisem anotacji: {desc_file_path}") 

