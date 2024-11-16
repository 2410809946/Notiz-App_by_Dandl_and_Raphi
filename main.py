# 16.11.2024
# Notizbuch-App by Dandl and Raphi

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sqlite3

class NotizbuchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notizbuch-App by Dandl and Raphi")
        self.root.geometry("400x300")
        self.root.minsize(300, 200)

        self.notizen = []

        self.conn = sqlite3.connect('notizen.db')
        self.c = self.conn.cursor()
        self.create_table()

        self.create_widgets()
        self.load_notes()
        self.update_time()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS notizen
                              (id INTEGER PRIMARY KEY, timestamp TEXT, notiz TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def create_widgets(self):
        self.time_label = tk.Label(self.root, font=('Helvetica', 10))
        self.time_label.pack(anchor='nw', padx=10, pady=5)

        self.eingabe = ttk.Entry(self.root)
        self.eingabe.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        self.button_add = ttk.Button(button_frame, text="Neue Notiz hinzufügen", command=self.add_note)
        self.button_add.pack(side=tk.LEFT, padx=5)

        self.button_delete = ttk.Button(button_frame, text="Als Erledigt markieren", command=self.delete_note)
        self.button_delete.pack(side=tk.LEFT, padx=5)

        self.button_edit = ttk.Button(button_frame, text="Notiz bearbeiten", command=self.edit_note)
        self.button_edit.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

    def load_notes(self):
        try:
            self.c.execute("SELECT timestamp, notiz FROM notizen")
            rows = self.c.fetchall()
            for row in rows:
                notiz_mit_zeit = f"{row[0]} - {row[1]}"
                self.notizen.append(notiz_mit_zeit)
                self.listbox.insert(tk.END, notiz_mit_zeit)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def add_note(self):
        notiz = self.eingabe.get()
        if notiz:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notiz_mit_zeit = f"{timestamp} - {notiz}"
            self.notizen.append(notiz_mit_zeit)
            self.listbox.insert(tk.END, notiz_mit_zeit)
            self.eingabe.delete(0, tk.END)
            try:
                self.c.execute("INSERT INTO notizen (timestamp, notiz) VALUES (?, ?)", (timestamp, notiz))
                self.conn.commit()
                messagebox.showinfo("Success", "Notiz hinzugefügt")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def delete_note(self):
        selected_note_indices = self.listbox.curselection()
        for index in reversed(selected_note_indices):
            notiz = self.listbox.get(index)
            self.notizen.remove(notiz)
            self.listbox.delete(index)
            timestamp, notiz_text = notiz.split(" - ", 1)
            try:
                self.c.execute("DELETE FROM notizen WHERE timestamp = ? AND notiz = ?", (timestamp, notiz_text))
                self.conn.commit()
                messagebox.showinfo("Success", "Notiz gelöscht")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def edit_note(self):
        selected_note_indices = self.listbox.curselection()
        if selected_note_indices:
            index = selected_note_indices[0]
            old_note = self.listbox.get(index)
            timestamp, old_text = old_note.split(" - ", 1)
            new_text = simpledialog.askstring("Notiz bearbeiten", "Bearbeiten Sie die Notiz:", initialvalue=old_text)
            if new_text:
                new_note = f"{timestamp} - {new_text}"
                self.notizen[index] = new_note
                self.listbox.delete(index)
                self.listbox.insert(index, new_note)
                try:
                    self.c.execute("UPDATE notizen SET notiz = ? WHERE timestamp = ? AND notiz = ?", (new_text, timestamp, old_text))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Notiz bearbeitet")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotizbuchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()