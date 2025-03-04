import cv2
import os
import numpy as np
import shutil


def save_bright_frames(folder_path, brightness_threshold=30):
    # Ustawienie ścieżki dla nowego folderu
    new_folder_path = f"{folder_path}_selection"
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Iteracja po wszystkich plikach w folderze
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Sprawdzenie, czy jest to plik obrazu
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Wczytanie obrazu
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"Nie udało się wczytać obrazu: {filename}")
                continue
            
            # Obliczenie średniej jasności
            mean_brightness = np.mean(image)
            
            # Kopiowanie obrazu do nowego folderu, jeśli jasność jest powyżej progu
            if mean_brightness >= brightness_threshold:
                new_file_path = os.path.join(new_folder_path, filename)
                shutil.copy(file_path, new_file_path)
                print(f"Zapisano jasny obraz: {filename} do {new_folder_path}")


folder_name = "test2"
folder_path = f"../Datasets/lightning_photos/{folder_name}"
brightness_threshold = 15  # Próg jasności

save_bright_frames(folder_path, brightness_threshold)
