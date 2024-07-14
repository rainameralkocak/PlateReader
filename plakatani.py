import cv2 
import numpy as np 
import pytesseract 
from tkinter import filedialog, Tk, Button, Label, TOP, RIGHT, LEFT, BOTTOM 
from PIL import Image, ImageTk 

# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def select_image():
    global file_path  
    file_path = filedialog.askopenfilename() 
    if file_path:  
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(image))
        image_label.config(image=photo)
        image_label.image = photo
        process_button.config(state="normal")

def process_image():
    global file_path  
    if file_path: 
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate = gray[y:y + h, x:x + w]
        text = pytesseract.image_to_string(plate, config='--psm 8')
        result_label.config(text="Tespit Edilen Plaka: " + text, fg="steel blue", font=("Arial", 14, "bold"))
        print("Tespit Edilen Plaka:", text) 
        cv2.putText(image, "Plaka: " + text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(image))
        image_label.config(image=photo)
        image_label.image = photo

root = Tk()  
root.title("Plaka Tanıma Uygulaması") 
root.geometry("1500x600")  

file_path = None 

open_button = Button(root, text="Resim Yükle", command=select_image, bg="steel blue", fg="white", padx=20, pady=10)
open_button.pack(side=TOP, padx=10, pady=10)

image_label = Label(root, bg="white")
image_label.pack(side=LEFT, padx=10, pady=10)

process_button = Button(root, text="Tespiti Başlat", command=process_image, state="disabled", bg="medium sea green", fg="white", padx=20, pady=10)
process_button.pack(side=RIGHT, padx=10, pady=10)

result_label = Label(root, text="", fg="blue")
result_label.pack(side=BOTTOM, padx=10, pady=10)

root.mainloop()  
