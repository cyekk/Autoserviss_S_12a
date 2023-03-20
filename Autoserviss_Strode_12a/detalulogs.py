#=================================
#IMPORTĒŠANA
from tkinter import *
from tkinter import messagebox
from db import Database, save_database1
import customtkinter
import tkinter as tk
import re

#=================================
#LOGA IZVEIDE, NOSAUKUMS, IZMĒRS UN NOSACĪJUMS, KA IZMĒRU NEVAR MAINĪT LIETOTĀJS + LOGA NOFORMĒJUMS BŪS DARK MODE UN AKCENTA KRĀSAS BŪS ZILAS
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")  
app = customtkinter.CTk()  
app.title('AUTO DETAĻU REĢISTRĀCIJA')
app.geometry('740x340')
app.resizable(False, False)

#=================================
#DATUBĀZES DEFINĒŠANA
db = Database('inventars.db')

#=================================================
#DEFINĒT FUNKCIJU = POPULĒT DATUS TABULĀ (aizpildīt tabulu ar info)
def populet_sarakstu():
    detalu_saraksts.delete(0, END)
    for row in db.fetch():
        detalu_saraksts.insert(END, row)

#DEFINĒT DETAĻU PIEVIENOŠANU + LIETOTĀJA BRĪDINĀJUMI
def pievienot_detalu():
    nosauk = nosauk_teksts.get()
    razotajs = razotajs_teksts.get()
    modelis = modelis_teksts.get()
    skaits = skaits_teksts.get()
    cena = cena_teksts.get()

#Ja kāda no vērtībām atstāta tukša, lietotājs saņem brīdinājumu
    if nosauk == '' or razotajs == '' or modelis == '' or skaits == '' or cena == '':
        messagebox.showerror('Kļūda', 'Aizpildiet visas sadaļas!') 
        return

#Ja sekojošais gadījums neizpildās - cena sastāv tikai no cipariem, izņemot gadījumā, ka tai priekšā valūtas simbols ; lietotājs saņem brīdinājumu
    if not re.match(r'^[\$\£\€]?[0-9]+(?:\.[0-9]{1,2})?$', cena):
        messagebox.showerror('Kļūda', 'CENA var saturēt tikai ciparus un valūtas simbolus (piemēram, "$", "£", "€")!')
        return

#Vērtībai skaits jābūt int; ja tas satur citas rakstzīmes, lietotājs saņem brīdinājumu
    try:
        skaits = int(skaits)
    except ValueError:
        messagebox.showerror('Kļūda', 'SKAITS nevar sastāvēt no citām rakstzīmēm')
        return
    
#Ja skaits ir mazāks vai vienāds ar 0, lietotājs saņem brīdinājumu
    if skaits <= 0:
        messagebox.showerror('Kļūda', 'SKAITAM jābūt pozitīvam!')
        return

#Visas ievades vērtības ievietotas attiecīgajās tabulas vietās
    db.insert(nosauk, razotajs, modelis, skaits, cena)
    detalu_saraksts.delete(0, END)
    detalu_saraksts.insert(END, (nosauk, razotajs, modelis, skaits, cena))

#Ievades logi tiek notīrīti, tabulā/sarakstā aizpildās informācija
    notirit_teksts()
    populet_sarakstu()

#=================================================
#FUNKCIJA, KAS NOSAKA, KA VĒRTĪBA IR ATLASĪTA
def select_detalu(event):
    try:
        global selected_detalu
        index = detalu_saraksts.curselection()[0]
        selected_detalu = detalu_saraksts.get(index)

        nosauk_entry.delete(0, END)
        nosauk_entry.insert(END, selected_detalu[1])

        razotajs_entry.delete(0, END)
        razotajs_entry.insert(END, selected_detalu[2])

        modelis_entry.delete(0, END)
        modelis_entry.insert(END, selected_detalu[3])

        skaits_entry.delete(0, END)
        skaits_entry.insert(END, selected_detalu[4])

        cena_entry.delete(0, END)
        cena_entry.insert(END, selected_detalu[5])
    except IndexError:
        pass

#FUNKCIJA, KAS IZDZĒŠ VĒRTĪBU
def nonemt_detalu():
    db.nonemt(selected_detalu[0])
    notirit_teksts()
    populet_sarakstu()

#=================================================
#IERAKSTITO DATU REDIĢĒŠANA
def rediget_detalu():
    db.rediget(selected_detalu[0], nosauk_teksts.get(), razotajs_teksts.get(),
              modelis_teksts.get(), skaits_teksts.get(), cena_teksts.get())
    populet_sarakstu()

#IERAKSTITO DATU ATCELŠANA JEB NOTĪRĪŠANA
def notirit_teksts():
    nosauk_entry.delete(0, END)
    razotajs_entry.delete(0, END)
    modelis_entry.delete(0, END)
    skaits_entry.delete(0, END)
    cena_entry.delete(0, END)

#=================================================
#NOSAUKUMI UN TO ATTIECĪGĀS IEVADES VIETAS -> TO DATU TIPS, ATRAŠĀNĀS VIETA, TEKSTS, KRĀSA, FONTS, ATRAŠANĀS VIETA GRIDĀ
# NOSAUKUMS
nosauk_teksts = StringVar()
nosauk_label = tk.Label(text="NOSAUKUMS        ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
nosauk_label.grid(row=0, column=0, sticky=E)
nosauk_entry = customtkinter.CTkEntry(master=app, textvariable=nosauk_teksts)
nosauk_entry.grid(row=0, column=1)

# RAŽOTĀJS
razotajs_teksts= StringVar()
razotajs_label = tk.Label(text="RAŽOTĀJS             ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
razotajs_label.grid(row=1, column=0, sticky=E)
razotajs_entry = customtkinter.CTkEntry(master=app, textvariable=razotajs_teksts)
razotajs_entry.grid(row=1, column=1)

# MODELIS
modelis_teksts = StringVar()
modelis_label = tk.Label(text="MODELIS               ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
modelis_label.grid(row=2, column=0, sticky=E)
modelis_entry = customtkinter.CTkEntry(master=app, textvariable=modelis_teksts)
modelis_entry.grid(row=2, column=1)

# SKAITS
skaits_teksts = StringVar()
skaits_label = tk.Label(text="SKAITS                   ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
skaits_label.grid(row=3, column=0, sticky=E)
skaits_entry = customtkinter.CTkEntry(master=app, textvariable=skaits_teksts)
skaits_entry.grid(row=3, column=1)

# CENA
cena_teksts = StringVar()
cena_label = tk.Label(text="CENA                      ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
cena_label.grid(row=4, column=0, sticky=E)
cena_entry = customtkinter.CTkEntry(master=app, textvariable=cena_teksts)
cena_entry.grid(row=4, column=1)

#=================================================
# TABULAS IZKARTOJUMS -> (ATRODAS IEKŠĀ logā (app), AUGSTUMS, KRĀSA, PLATUMS, RĀMJA PLATUMS UN BIEZUMS)
detalu_saraksts = Listbox(app, height=13,bg="#7E8283", width=65, borderwidth=0, highlightthickness=0)
detalu_saraksts.grid(row=0, column=2, columnspan=3, rowspan=6, pady=10, padx=10)

# RITJOSLAS IESTATĪŠANA -> (ATRAŠĀNĀS VIETA-app ; TA IZKARTOJUMS GRIDĀ)
scrolls = Scrollbar(app)
scrolls.grid(row=1, column=8)

# RITJOSLAS IZVIETOJUMS ATTIECIGI TABULAI
detalu_saraksts.configure(yscrollcommand=scrolls.set)
scrolls.configure(command=detalu_saraksts.yview)

#=================================================
# ATLASĪŠANAS NOTIKŠANA
detalu_saraksts.bind('<<ListboxSelect>>', select_detalu)

#=================================================
# POGAS -> TO ATRASANAS VIETA, TEKSTS, FONA KRĀSA, PLATUMS, UN KOMANDA KAS IZPILDĀS, NOSPIEŽOT TO
pievienot_btn = customtkinter.CTkButton(app, text='PIEVIENOT',width=12, command=pievienot_detalu)
pievienot_btn.grid(row=6, column=0, pady=20)
#-------------
nonemt_btn = customtkinter.CTkButton(app, text='NOŅEMT',width=12, command=nonemt_detalu)
nonemt_btn.grid(row=6, column=1)
#-------------
rediget_btn = customtkinter.CTkButton(app, text='REDIĢĒT',width=12, command=rediget_detalu)
rediget_btn.grid(row=6, column=2)
#-------------
notirit_btn = customtkinter.CTkButton(app, text='ATCELT', width=12, command=notirit_teksts)
notirit_btn.grid(row=6, column=3)
#-------------
saglabat_btn = customtkinter.CTkButton(app, text='SAGLABĀT', width=12, command=lambda: save_database1(db))
saglabat_btn.grid(row=6, column=4)

#=================================================
# INFORMĀCIJAS AIZPILDĪŠANA TABULĀ/SARAKSTĀ
populet_sarakstu()

#LOGA UZSĀKŠANA
app.mainloop()

#=================================================
