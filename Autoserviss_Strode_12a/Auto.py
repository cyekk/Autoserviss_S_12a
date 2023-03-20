#=================================
#IMPORTĒŠANA
from tkinter import *
import tkinter as tk
import customtkinter
import subprocess
from PIL import Image, ImageTk

#=================================
#LOGA IZVEIDE, NOSAUKUMS, IZMĒRS UN NOSACĪJUMS, KA IZMĒRU NEVAR MAINĪT LIETOTĀJS
app = customtkinter.CTk()
app.title('AUTO SERVISA PROGRAMMA')
app.geometry('350x270')
app.resizable(False, False)

#=================================
#FUNKCIJAS DEFINĒŠANA - atvērt detaļu, klienta un šifrēšanas logu
def run_detalulogs():
    subprocess.Popen(['python', 'detalulogs.py'])

def run_klientulogs():
    subprocess.Popen(['python', 'klientulogs.py'])

def run_sifrelogs():
    subprocess.Popen(['python', 'sifrelogs.py'])
#=================================
#BILDES - FONA IESTATĪŠANA
image = Image.open("bg.png")

#Loga izmērs un nosacījums, ka bilde ir loga izmērā
window_width, window_height = app.winfo_width(), app.winfo_height()
image = image.resize((window_width, window_height), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image)
background_label = customtkinter.CTkLabel(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#=================================
#NOSAUKUMA IESTATĪŠANA
label1 = tk.Label(text="AUTO",foreground="white", background="#242424",font=('Oswald',36,'bold'))
label1.place(anchor = CENTER, relx = .5, rely = .2)

label2 = tk.Label(text="SERVISS",foreground="#1f6aa5", background="#242424",font=('Oswald',36,'bold'))
label2.place(anchor = CENTER, relx = .5, rely = .4)

#=================================
#POGAS IESTATĪŠANA
detalas_btn = Button(text="DETAĻAS ",bg="#1e1e1e",fg="white", width=12, command=run_detalulogs)
detalas_btn.place(anchor = CENTER, relx = .5, rely = .7)

klienti_btn = Button(text="  KLIENTI  ",bg="#1e1e1e",fg="white", width=12, command=run_klientulogs)
klienti_btn.place(anchor = CENTER, relx = .5, rely = .8)

sifre_btn = Button(text="  ŠIFRĒŠANA  ",bg="#1e1e1e",fg="white", width=12, command=run_sifrelogs)
sifre_btn.place(anchor = CENTER, relx = .5, rely = .9)

#=================================
#LOGA UZSĀKŠANA
app.mainloop()
