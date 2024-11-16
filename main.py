# 16.11.2024
# Notizbuch-App by Dandl and Raphi

import tkinter as tk
from datetime import datetime

# erstelle ein Fenster
fenster = tk.Tk()
fenster.title("Notizbuch-App by Dandl and Raphi")
fenster.geometry("400x300")

# Mindestgröße festlegen (Breite x Höhe in Pixel)
fenster.minsize(300, 200)

# erstelle eine Liste für die Notizen
notizen = []

# erstelle eine Funktion zum Hinzufügen von Notizen
def add_note():
    notiz = eingabe.get()
    if notiz:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notiz_mit_zeit = f"{timestamp} - {notiz}"
        notizen.append(notiz_mit_zeit)
        listbox.insert(tk.END, notiz_mit_zeit)
        eingabe.delete(0, tk.END)

# erstelle eine Funktion zum Löschen von Notizen
def delete_note():
    selected_note_indices = listbox.curselection()
    for index in reversed(selected_note_indices):
        notiz = listbox.get(index)
        notizen.remove(notiz)
        listbox.delete(index)

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

# starte das Fenster
fenster.mainloop()