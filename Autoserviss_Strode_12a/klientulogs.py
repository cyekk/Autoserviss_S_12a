#=================================
#IMPORTĒŠANA
from tkinter import *
from tkinter import messagebox
from db import Pasutitaji, save_database2
import customtkinter
import tkinter as tk
import re

#=================================
#LOGA IZVEIDE, NOSAUKUMS, IZMĒRS UN NOSACĪJUMS, KA IZMĒRU NEVAR MAINĪT LIETOTĀJS + LOGA NOFORMĒJUMS BŪS DARK MODE UN AKCENTA KRĀSAS BŪS ZILAS
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")  
app = customtkinter.CTk()  
app.title('KLIENTU REĢISTRĀCIJA')
app.geometry('780x340')
app.resizable(False, False)

#=================================
#DATUBĀZES DEFINĒŠANA
db = Pasutitaji('inventars.db')

#=================================
#DEFINĒT FUNKCIJU = POPULĒT DATUS TABULĀ (aizpildīt tabulu ar info)
def populet_sarakstu():
    detalu_saraksts.delete(0, END)
    for row in db.fetch():
        detalu_saraksts.insert(END, row)

#DEFINĒT DETAĻU PIEVIENOŠANU + LIETOTĀJA BRĪDINĀJUMI
def pievienot_detalu():
    vards = vards_teksts.get()
    uzvards = uzvards_teksts.get()
    pasutijums = pasutijums_teksts.get()
    skaits = skaits_teksts.get()
    numurs = numurs_teksts.get()

#Ja kāda no vērtībām atstāta tukša, lietotājs saņem brīdinājumu
    if vards == '' or uzvards == '' or pasutijums == '' or skaits == '' or numurs == '':
        messagebox.showerror('Kļūda', 'Aizpildiet visas sadaļas!') 
        return

#Ja vārds vai uzvārds nesastāv no burtiem un sekojošajām rakstzīmēm, lietotājs saņem brīdinājumu
    if not re.match("^[A-Za-zĀāČčĒēĢģĪīĶķĻļŅņŠšŪūŽž]+$", vards) or not re.match("^[A-Za-zĀāČčĒēĢģĪīĶķĻļŅņŠšŪūŽž]+$", uzvards):
        messagebox.showerror('Kļūda', 'VĀRDS un/vai UZVĀRDS var sastāvēt tikai no burtiem!')
        return

#Vērtībai skaits jābūt int; ja tas satur citas rakstzīmes, lietotājs saņem brīdinājumu
    try:
        skaits = int(skaits)
    except ValueError:
        messagebox.showerror('Kļūda', 'SKAITS nevar sastāvēt no citām rakstzīmēm')
        return
    
#Ja skaits ir mazāks vai vienāds ar 0, lietotājs saņem brīdinājumu
    if skaits <= 0 or pasutijums <= 0:
        messagebox.showerror('Kļūda', 'SKAITAM un/vai PASŪTIJUMAM jābūt pozitīvam!')
        return
    
#Vērtībai pasutijums jābūt int; ja tas satur citas rakstzīmes, lietotājs saņem brīdinājumu
    try:
        pasutijums = int(pasutijums)
    except ValueError:
        messagebox.showerror('Kļūda', 'PASŪTIJUMS nevar sastāvēt no citām rakstzīmēm')
        return

#Vērtībai numurs jābūt int;
    try:
        numurs = str(numurs)
        #Ja numurs nesākās ar '+371', lietotājs saņem brīdinājumu
        if not numurs.startswith('+371'):
            raise ValueError('Nummuram jāsākas ar "+371"!')
        
        #Ja numura garums nav vienāds ar 12, lietotājs saņem brīdinājumu
        if len(numurs) != 12:
            raise ValueError('Telefona numuram pēc "+371" jābūt 8 cipariem!')
        
        #Ja numurs pēc 4 vērtībām satur citas rakstzīmes, lietotājs saņem brīdinājumu
        if not numurs[4:].isdigit():
            raise ValueError('numurs var saturēt tikai ciparus pēc "+371"!')
        
   #Ja notiek errors, loga nosaukums būs "Kļūda" un loga teksts būs attiecīgs kļūdai
    except ValueError as e:
        messagebox.showerror('Kļūda', str(e))
        return
    
    #Visas ievades vērtības ievietotas attiecīgajās tabulas vietās
    db.insert(vards, uzvards, pasutijums, skaits, numurs)
    detalu_saraksts.delete(0, END)
    detalu_saraksts.insert(END, (vards, uzvards, pasutijums, skaits, numurs))

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

        vards_entry.delete(0, END)
        vards_entry.insert(END, selected_detalu[1])

        uzvards_entry.delete(0, END)
        uzvards_entry.insert(END, selected_detalu[2])

        pasutijums_entry.delete(0, END)
        pasutijums_entry.insert(END, selected_detalu[3])

        skaits_entry.delete(0, END)
        skaits_entry.insert(END, selected_detalu[4])

        numurs_entry.delete(0, END)
        numurs_entry.insert(END, selected_detalu[5])
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
    db.rediget(selected_detalu[0], vards_teksts.get(), uzvards_teksts.get(),
              pasutijums_teksts.get(), skaits_teksts.get(), numurs_teksts.get())
    populet_sarakstu()

#IERAKSTITO DATU ATCELŠANA JEB NOTĪRĪŠANA
def notirit_teksts():
    vards_entry.delete(0, END)
    uzvards_entry.delete(0, END)
    pasutijums_entry.delete(0, END)
    skaits_entry.delete(0, END)
    numurs_entry.delete(0, END)
#=================================================
#NOSAUKUMI UN TO ATTIECĪGĀS IEVADES VIETAS -> TO DATU TIPS, ATRAŠĀNĀS VIETA, TEKSTS, KRĀSA, FONTS, ATRAŠANĀS VIETA GRIDĀ
# VARDS
vards_teksts = StringVar()
vards_label = tk.Label(text="VARDS                              ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
vards_label.grid(row=0, column=0, sticky=E)
vards_entry = customtkinter.CTkEntry(master=app, textvariable=vards_teksts)
vards_entry.grid(row=0, column=1)

# UZVARDS
uzvards_teksts= StringVar()
uzvards_label = tk.Label(text="UZVARDS                         ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
uzvards_label.grid(row=1, column=0, sticky=E)
uzvards_entry = customtkinter.CTkEntry(master=app, textvariable=uzvards_teksts)
uzvards_entry.grid(row=1, column=1)

# PASUTIJUMS
pasutijums_teksts = StringVar()
pasutijums_label = tk.Label(text="PASŪTĪJUMA ID              ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
pasutijums_label.grid(row=2, column=0, sticky=E)
pasutijums_entry = customtkinter.CTkEntry(master=app, textvariable=pasutijums_teksts)
pasutijums_entry.grid(row=2, column=1)

# SKAITS
skaits_teksts = StringVar()
skaits_label = tk.Label(text="SKAITS                             ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
skaits_label.grid(row=3, column=0, sticky=E)
skaits_entry = customtkinter.CTkEntry(master=app, textvariable=skaits_teksts)
skaits_entry.grid(row=3, column=1)

# NUMURS
numurs_teksts = StringVar()
numurs_label = tk.Label(text="NUMURS                           ",foreground="#636566", background="#242424",font=('Oswald',14,'bold'))
numurs_label.grid(row=4, column=0, sticky=E)
numurs_entry = customtkinter.CTkEntry(master=app, textvariable=numurs_teksts)
numurs_entry.grid(row=4, column=1)

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
notirit_btn = customtkinter.CTkButton(app, text='ATCELT',width=12, command=notirit_teksts)
notirit_btn.grid(row=6, column=3)
#-------------
saglabat_btn = customtkinter.CTkButton(app, text='SAGLABĀT', width=12, command=lambda: save_database2(db))
saglabat_btn.grid(row=6, column=4)
#=================================================
# INFORMĀCIJAS AIZPILDĪŠANA TABULĀ/SARAKSTĀ
populet_sarakstu()

#LOGA UZSĀKŠANA
app.mainloop()

#=================================================
