import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import boto3

my_w = tk.Tk()
my_w.geometry("450x400")
my_w.title("AWS Textract")

l1 = tk.Label(my_w, text="Upload the Image", width=30, font=('times', 18, 'bold'))
l1.pack()

def upload_file():
    aws_mag_con = boto3.session.Session(profile_name='text-to-speech')
    client = aws_mag_con.client(service_name='textract', region_name='us-east-1')

    global img  # Declare img as a global variable

    # Open a file dialog to select an image file
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)

    img = Image.open(filename)

    # Resizing the image
    img_resized = img.resize((400, 200))
    img_tk = ImageTk.PhotoImage(img_resized)

    # Display the image in a label
    img_label = tk.Label(my_w, image=img_tk)
    img_label.image = img_tk  
    img_label.pack()

    # Read the image file as bytes
    imgbytes = get_image_byte(filename)

    response = client.detect_document_text(Document={'Bytes': imgbytes})
    for item in response['Blocks']:
        if item['BlockType'] == 'WORD': #WORD CAN BE REPLACED WITH 'LINE' TO GET DIFFERENT RESULT
            print(item['Text'])

def get_image_byte(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

b1 = tk.Button(my_w, text='Upload File and See What it has!!', width=30, command=upload_file)
b1.pack()

my_w.mainloop()
