# 16.11.2024
# Notizbuch-App by Dandl and Raphi

import tkinter as tk

# erstelle ein Fenster
fenster = tk.Tk()
fenster.title("Notizbuch-App by Dandl and Raphi")
fenster.geometry("400x300")

# erstelle eine Liste für die Notizen
notizen = []

# erstelle eine Funktion zum Hinzufügen von Notizen
def add_note():
    notiz = eingabe.get()
    if notiz:
        notizen.append(notiz)
        listbox.insert(tk.END, notiz)
        eingabe.delete(0, tk.END)

# erstelle eine Funktion zum Löschen von Notizen
def delete_note():
    selected_note_index = listbox.curselection()
    if selected_note_index:
        notiz = listbox.get(selected_note_index)
        notizen.remove(notiz)
        listbox.delete(selected_note_index)

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
listbox = tk.Listbox(fenster)
listbox.pack(fill=tk.BOTH, expand=True)

# starte das Fenster
fenster.mainloop()