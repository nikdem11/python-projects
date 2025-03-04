import cv2
import os


def extract_frames(video_path, output_folder, frame_rate=1):
    # Sprawdzenie, czy plik wideo istnieje
    if not os.path.exists(video_path):
        print("Plik wideo nie istnieje.")
        return

    # Utworzenie folderu wyjściowego, jeśli nie istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Otwieranie pliku wideo
    video = cv2.VideoCapture(video_path)
    
    # Sprawdzanie, czy udało się otworzyć wideo
    if not video.isOpened():
        print("Nie udało się otworzyć wideo.")
        return

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

        # Zapisanie klatki co `frame_interval`
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"{video_name}_frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1

        frame_count += 1

    # Zwolnienie zasobów
    video.release()
    print(f"Zapisano {saved_count} klatek do folderu: {output_folder}")


video_name = "test"
video_path = f"../Datasets/lightning_videos/{video_name}.mp4"
output_folder = f"../Datasets/lightning_photos/{video_name}"
frame_rate = 10  

extract_frames(video_path, output_folder, frame_rate)
