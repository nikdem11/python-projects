import tensorflow as tf
import cv2
import os


def dataset_generator(video_path, model_path, output_folder, frame_rate):
        if not os.path.exists(video_path):
            print("Plik wideo nie istnieje.")
            return

        lightning_folder = f"{output_folder}/lightning"
        no_lightning_folder = f"{output_folder}/no_lightning"

        # Utworzenie folderu wyjściowego, jeśli nie istnieje
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            os.makedirs(lightning_folder)
            os.makedirs(no_lightning_folder)
        
        # Otwieranie pliku wideo
        video = cv2.VideoCapture(video_path)
        
        # Sprawdzanie, czy udało się otworzyć wideo
        if not video.isOpened():
            print("Nie udało się otworzyć wideo.")
            return

        # Ładowanie modelu
        model = tf.keras.models.load_model(model_path)

        frame_count = 0
        saved_count = 0
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / frame_rate)

        while True:
            # Przechwycenie klatki
            ret, frame = video.read()
            
            # Zakończenie, jeśli brak klatek
            if not ret:
                break

            # Sprawdzanie klatki co `frame_interval`
            if frame_count % frame_interval == 0:
                # Zmiana rozmiaru klatki do rozmiaru obsługiwanego przez model
                img_height, img_width = 224, 224  
                resized_frame = cv2.resize(frame, (img_width, img_height))
                img_array = tf.keras.utils.img_to_array(resized_frame)
                img_array = tf.expand_dims(img_array, 0)  # Tworzenie batcha

                # Predykcja modelu
                prediction = model.predict(img_array)
                
                if prediction[0] < 0.5:
                    frame_filename = os.path.join(lightning_folder, f"{video_name}_frame_{saved_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame)
                else:
                    frame_filename = os.path.join(no_lightning_folder, f"{video_name}_frame_{saved_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame)
                    
                saved_count += 1  

            frame_count += 1

        # Zwolnienie zasobów
        video.release()
        print(f"Zapisano {saved_count} klatek do podfolderów folderu: {output_folder}")


video_name = "test3"
video_path = f"../Datasets/lightning_videos/{video_name}.mp4"
model_name = "model60v3"
model_path = f"../Models/{model_name}.keras"
output_folder = f"../Datasets/lightning_photos/{video_name}_by_{model_name}"
frame_rate = 1  

dataset_generator(video_path, model_path, output_folder, frame_rate)
