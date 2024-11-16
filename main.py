# 16.11.2024

# verwende tkinter für gui, erstelle ein Fenster

import tkinter as tk

# erstelle ein Fenster

fenster = tk.Tk()
fenster.title("Notizbuch-App by Dandl and Raphi")
fenster.geometry("400x300")

# Mit dem Programm sollen Notizen erstellt und gespeichert werden können. Erstelle einen Button zum Hinzufügen von neuen Notizen und einen zum Löschen von Notizen.

# erstelle eine Liste für die Notizen

notizen = []

# erstelle eine Funktion zum Hinzufügen von Notizen

def add_note():
    notiz = eingabe.get()
    notizen.append(notiz)
    ausgabe.config(text=notizen)

# erstelle eine Funktion zum Löschen von Notizen

def delete_note():
    notiz = eingabe.get()
    notizen.remove(notiz)
    ausgabe.config(text=notizen)

# erstelle ein Eingabefeld für die Notizen

eingabe = tk.Entry(fenster)
eingabe.pack()

# erstelle einen Button zum Hinzufügen von Notizen

button_add = tk.Button(fenster, text="Hinzufügen", command=add_note)
button_add.pack()

# erstelle einen Button zum Löschen von Notizen

button_delete = tk.Button(fenster, text="Löschen", command=delete_note)
button_delete.pack()

# erstelle ein Ausgabefeld für die Notizen

ausgabe = tk.Label(fenster, text="")
ausgabe.pack()


# starte das Fenster

fenster.mainloop()