
#=================================================
#IMPORTĀCIJA - sqlite3 un Fernet klase no cryptography
import sqlite3
import csv
from tkinter import messagebox

#=================================================
#KASES IZVEIDE, kurā tiek izveidota tabula ar vērtībām nosauk, razotajs, modelis, skaits, cena
class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tabula1 (id INTEGER PRIMARY KEY, nosauk text, razotajs text, modelis text, skaits text, cena text)")
        self.conn.commit()

#Definēta datu ieguve no tabulas
    def fetch(self):
        self.cur.execute("SELECT * FROM tabula1")
        rows = self.cur.fetchall()
        return rows
    
#Definēta datu ievietošana tabulā
    def insert(self, nosauk, razotajs, modelis, skaits, cena):
        self.cur.execute("INSERT INTO tabula1 VALUES(NULL, ?, ?, ?, ?, ?)",
                         (nosauk, razotajs, modelis, skaits, cena))
        self.conn.commit()

#Definēta datu izņemšanas no tabulas
    def nonemt(self, id):
        self.cur.execute("DELETE FROM tabula1 WHERE id=?", (id,))
        self.conn.commit()

#Definēta datu rediģēšana
    def rediget(self, id, nosauk, razotajs, modelis, skaits, cena):
        self.cur.execute("UPDATE tabula1 SET nosauk = ?, razotajs = ?, modelis = ?, skaits = ?, cena = ? WHERE id = ?",
                         (nosauk, razotajs, modelis, skaits, cena, id))
        self.conn.commit()

#TABULAS AIZVĒRŠANA
    def __del__(self):
        self.conn.close()
    
#TABULAS SAGLABĀŠANA KĀ CSV FAILU
def save_database1(db):
    filename = 'DETALAS.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['ID', 'Nosaukums', 'Ražotājs', 'Modelis', 'Skaits', 'Cena'])
        rows = db.fetch()
        for row in rows:
            writer.writerow(row)
    messagebox.showinfo('SAGLABĀŠANA VEIKSMĪGA', f'DETAĻU DB SAGLABĀTA - {filename}')

#=================================================
#KLASES Pasutitaji FUNKCIJAS IR TĀDAS PAŠAS KĀ KLASEI Database, tikai ar citām vērtībām
class Pasutitaji:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tabula2 (id INTEGER PRIMARY KEY, vards text, uzvards text, pasutijums text, skaits text, numurs text)")
        self.conn.commit()
        
    def fetch(self):
        self.cur.execute("SELECT * FROM tabula2")
        rows = self.cur.fetchall()
        return rows
        
    def insert(self, vards, uzvards, pasutijums, skaits, numurs):
        self.cur.execute("insert INTO tabula2 VALUES(NULL, ?, ?, ?, ?, ?)",
                         (vards, uzvards, pasutijums, skaits, numurs))
        self.conn.commit()
        
    def nonemt(self, id):
        self.cur.execute("DELETE FROM tabula2 WHERE id=?", (id,))
        self.conn.commit()
        
    def rediget(self, id, vards, uzvards, pasutijums, skaits, numurs):
        self.cur.execute("UPDATE tabula2 SET vards = ?, uzvards = ?, pasutijums = ?, skaits = ?, numurs = ? WHERE id = ?",
                         (vards, uzvards, pasutijums, skaits, numurs, id))
        self.conn.commit()

    def save(self, filename):
        with open(filename, 'w') as f:
            rows = self.fetch()
            for row in rows:
                f.write(','.join(str(i) for i in row) + '\n')

    def __del__(self):
        self.conn.close()
    
def save_database2(db):
    filename = 'KLIENTI.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['ID', 'vards', 'uzvards', 'pasutijums', 'skaits', 'numurs'])
        rows = db.fetch()
        for row in rows:
            writer.writerow(row)
    messagebox.showinfo('SAGLABĀŠANA VEIKSMĪGA', f'DETAĻU DB SAGLABĀTA - {filename}')

#=================================================
