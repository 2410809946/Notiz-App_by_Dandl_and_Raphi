# 16.11.2024
# Notizbuch-App by Dandl and Raphi

import tkinter as tk
from datetime import datetime
import sqlite3

# erstelle ein Fenster
fenster = tk.Tk()
fenster.title("Notizbuch-App by Dandl and Raphi")
fenster.geometry("400x300")
fenster.minsize(300, 200)

# erstelle eine Liste für die Notizen
notizen = []

# erstelle eine Datenbankverbindung
conn = sqlite3.connect('notizen.db')
c = conn.cursor()

# erstelle eine Tabelle für die Notizen, falls sie nicht existiert
c.execute('''CREATE TABLE IF NOT EXISTS notizen
             (id INTEGER PRIMARY KEY, timestamp TEXT, notiz TEXT)''')
conn.commit()

# lade die Notizen aus der Datenbank
def load_notes():
    c.execute("SELECT timestamp, notiz FROM notizen")
    rows = c.fetchall()
    for row in rows:
        notiz_mit_zeit = f"{row[0]} - {row[1]}"
        notizen.append(notiz_mit_zeit)
        listbox.insert(tk.END, notiz_mit_zeit)

# erstelle eine Funktion zum Hinzufügen von Notizen
def add_note():
    notiz = eingabe.get()
    if notiz:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notiz_mit_zeit = f"{timestamp} - {notiz}"
        notizen.append(notiz_mit_zeit)
        listbox.insert(tk.END, notiz_mit_zeit)
        eingabe.delete(0, tk.END)
        # speichere die Notiz in der Datenbank
        c.execute("INSERT INTO notizen (timestamp, notiz) VALUES (?, ?)", (timestamp, notiz))
        conn.commit()

# erstelle eine Funktion zum Löschen von Notizen
def delete_note():
    selected_note_indices = listbox.curselection()
    for index in reversed(selected_note_indices):
        notiz = listbox.get(index)
        notizen.remove(notiz)
        listbox.delete(index)
        # lösche die Notiz aus der Datenbank
        timestamp, notiz_text = notiz.split(" - ", 1)
        c.execute("DELETE FROM notizen WHERE timestamp = ? AND notiz = ?", (timestamp, notiz_text))
        conn.commit()

# erstelle ein Eingabefeld für die Notizen
eingabe = tk.Entry(fenster)
eingabe.pack()

# erstelle einen Button zum Hinzufügen von Notizen
button_add = tk.Button(fenster, text="Hinzufügen", command=add_note)
button_add.pack()

# erstelle einen Button zum Löschen von Notizen
button_delete = tk.Button(fenster, text="Löschen", command=delete_note)
button_delete.pack()

# erstelle eine Listbox für die Notizen
listbox = tk.Listbox(fenster, selectmode=tk.MULTIPLE)
listbox.pack(fill=tk.BOTH, expand=True)

# lade die Notizen beim Start des Programms
load_notes()

# starte das Fenster
fenster.mainloop()

# schließe die Datenbankverbindung, wenn das Fenster geschlossen wird
conn.close()