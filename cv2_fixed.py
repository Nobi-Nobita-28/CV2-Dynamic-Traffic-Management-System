import cv2
import torch
import threading
import numpy as np
from PIL import Image, ImageTk
import customtkinter as ctk

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Nobi's Traffic Controller")
app.geometry("880x600")


camera_states = {"camera1": False, "camera2": False}
shared_data = {
    "frames": [None, None],  
    "counts": [{"people": 0, "vehicles": 0}, {"people": 0, "vehicles": 0}]  
}

def detect_and_count_live(video_source, index):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    while camera_states[f"camera{index+1}"]:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            print(f"Error: Unable to retrieve frame from source {video_source}")
            continue

        results = model(frame)
        people_count, vehicle_count = 0, 0

        if results and hasattr(results, 'xyxy'):
            for det in results.xyxy[0]:
                x1, y1, x2, y2 = map(int, det[:4]) 
                conf = det[4].item()  
                cls = int(det[5].item())  
                label = model.names[cls]  

                if label in ['person', 'car', 'truck', 'bus', 'motorbike']:
                    color = (0, 255, 0) if label == 'person' else (255, 0, 0)  
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame,f"{label} {conf:.2f}",(x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)

                    if label == 'person':
                        people_count += 1
                    else:
                        vehicle_count += 1

        with threading.Lock():
            shared_data["frames"][index] = frame.copy()  
            shared_data["counts"][index] = {"people": people_count, "vehicles": vehicle_count}

    cap.release()

def update_ui():
    while True:
        with threading.Lock():
            frames = shared_data["frames"]
            counts = shared_data["counts"]

            for i, frame in enumerate(frames):
                if frame is not None:
                    resized_frame = cv2.resize(frame, (500, 300))
                    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_frame)
                    img_tk = ImageTk.PhotoImage(pil_image)

                    if i == 0:
                        camera1_label.configure(image=img_tk)
                        camera1_label.image = img_tk
                    elif i == 1:
                        camera2_label.configure(image=img_tk)
                        camera2_label.image = img_tk

            total_people = sum(c["people"] for c in counts)
            total_vehicles = sum(c["vehicles"] for c in counts)
            info_label.configure(text=f"People: {total_people} | Vehicles: {total_vehicles}")

def toggle_camera(camera_key, video_source, index):
    if camera_states[camera_key]:
        camera_states[camera_key] = False
    else:
        camera_states[camera_key] = True
        thread = threading.Thread(target=detect_and_count_live, args=(video_source, index))
        thread.daemon = True
        thread.start()

title = ctk.CTkLabel(app, text="Nobi's Traffic Controller", font=("copperplate gothic bold",30))
title.place(x=220, y=20)
frame1 = ctk.CTkFrame(app, width=500, height=300, bg_color="black")
frame1.place(x=20, y=80) 

frame2 = ctk.CTkFrame(app, width=500, height=300, bg_color="black")
frame2.place(x=460, y=80)  

camera1_label = ctk.CTkLabel(frame1, text="")
camera1_label.pack()  

camera2_label = ctk.CTkLabel(frame2, text="")
camera2_label.pack()  

button_frame = ctk.CTkFrame(app, width=800, height=50)
button_frame.place(x=30, y=340)  

camera1_button = ctk.CTkButton(button_frame, text="ON/OFF Camera 1", command=lambda: toggle_camera("camera1", 0, 0))
camera1_button.place(x=200, y=10) 

camera2_button = ctk.CTkButton(button_frame, text="ON/OFF Camera 2", command=lambda: toggle_camera("camera2", 1, 1))
camera2_button.place(x=450, y=10) 

info_label = ctk.CTkLabel(app, text="People: 0 | Vehicles: 0", font=("Arial", 20))
info_label.place(x=320, y=440)  

ui_thread = threading.Thread(target=update_ui)
ui_thread.daemon = True
ui_thread.start()

app.mainloop()
