#=================================
#IMPORTĒŠANA
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import customtkinter
from PIL import ImageTk, Image

#=================================
#LOGA IZVEIDE, NOSAUKUMS, IZMĒRS UN NOSACĪJUMS, KA IZMĒRU NEVAR MAINĪT LIETOTĀJS + LOGA NOFORMĒJUMS BŪS DARK MODE UN AKCENTA KRĀSAS BŪS ZILAS
app = customtkinter.CTk()
app.title('ŠIFRĒŠANA')
app.geometry('350x270')
app.resizable(False, False)

#=================================
#RĀMJA DEFINĒŠANA, TĀ IZMĒRS, NOVIETOJUMS
frame = Frame(app, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
#-------------
frame1 = Frame(app, width=600, height=400)
frame1.pack()
frame1.grid(row=0, column=1)

#=================================
#Bildes definēšana, tā atrašanās vieta rāmī
img = ImageTk.PhotoImage(Image.open("bg.png"))
label = Label(frame, image = img)
label.pack()
#-------------
img1=ImageTk.PhotoImage(Image.open("header.png"))
label1 = Label(frame1, image = img1, borderwidth=0, highlightthickness=0)
label1.pack()

#=================================
#DEFINĒTA FAILU ATLASE NO FAILU PĀRLŪKA
def select_file():
    filepath = filedialog.askopenfilename(initialdir="./", title="Izvēlaties failu", filetypes=[("CSV Faili", "*.csv")])
    file_path.set(filepath)

#DEFINĒTA FAILU ŠIFRĒŠANA IZMANTOJOT FERNET
def encrypt_file():
    #Definēta atslēga
    key_file = 'atslega.key'
    #Definēts, ka fails, ko šifrēt tiek izvēlēts
    file_to_encrypt = file_path.get()

    #Ja netiek izvēlēts fails ko šifrēt, lietotājs saņem brīdinājumu
    if not file_to_encrypt:
        messagebox.showerror("Kļūda", "Lūdzu, izvēlieties failu!")
        return
    
    #Šifrējamais fails definēts un atslēgas nolasīšana
    encrypted_file = 'enc_klienti.csv'
    with open(key_file, 'rb') as key_file:
        key = key_file.read()

    #Oriģinālā faila nolasīšana
    with open(file_to_encrypt, 'rb') as original_file:
        original = original_file.read()
        #Atslēgas ģenerēšana
        f = Fernet(key)
        #Oriģinālā faila šifrēšana
        encrypted = f.encrypt(original)
    #Šifrējuma uzrakstīšana
    with open(encrypted_file, 'wb') as ef:
        ef.write(encrypted)

#-------------

#DEFINĒTA FAILU ŠIFRĒŠANA IZMANTOJOT FERNET
def decrypt_file():
    key_file = 'atslega.key'
    file_to_decrypt = 'dec_klienti.csv'
    encrypted_file = file_path.get()
    if not encrypted_file:
        messagebox.showerror("Kļūda", "Lūdzu, izvēlieties failu!")
        return
    with open(key_file, 'rb') as key_file:
        key = key_file.read()
    with open(encrypted_file, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
    with open(file_to_decrypt, 'wb') as df:
        df.write(decrypted)

#-------------
file_path = tk.StringVar()
#=================================
#NOSAUKUMA IESTATĪŠANA
label2 = tk.Label(text="FAILU ŠIFRĒŠANA",foreground="#1f6aa5", background="#242424",font=('Oswald',24,'bold'))
label2.place(anchor = CENTER, relx = .5, rely = .4)

#=================================
#POGAS IESTATĪŠANA
fails_btn = Button(text="IZVĒLIES FAILU ",bg="#1e1e1e",fg="white", width=12, command=select_file)
fails_btn.place(anchor = CENTER, relx = .5, rely = .7)

klienti_btn = Button(text="  ŠIFRĒ  ",bg="#1e1e1e",fg="white", width=12, command=encrypt_file)
klienti_btn.place(anchor = CENTER, relx = .5, rely = .8)

sifre_btn = Button(text="  ATŠIFRĒ ",bg="#1e1e1e",fg="white", width=12, command=decrypt_file)
sifre_btn.place(anchor = CENTER, relx = .5, rely = .9)
#=================================
#LOGA UZSĀKŠANA
app.mainloop()
