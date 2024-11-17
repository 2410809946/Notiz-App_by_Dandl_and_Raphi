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
        self.root.geometry("500x300")
        self.root.minsize(300, 200)

        self.notizen = []
        self.dark_mode = False
        self.categories = ["Freizeit", "Geschäftliches", "Anderes"]

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
            self.c.execute('''ALTER TABLE notizen ADD COLUMN kategorie TEXT''')
            self.conn.commit()
        except sqlite3.Error as e:
            if "duplicate column name" not in str(e):
                messagebox.showerror("Database Error", str(e))

    def create_widgets(self):
        self.time_label = tk.Label(self.root, font=('Helvetica', 10))
        self.time_label.pack(anchor='nw', padx=10, pady=5)

        self.eingabe = ttk.Entry(self.root)
        self.eingabe.pack(pady=10)

        self.category_label = ttk.Label(self.root, text="Kategorie:")
        self.category_label.pack(pady=5)

        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_menu['values'] = self.categories
        self.category_menu.current(0)
        self.category_menu.pack(pady=5)

        self.add_category_button = ttk.Button(self.root, text="Neue Kategorie hinzufügen", command=self.add_category)
        self.add_category_button.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        self.button_add = ttk.Button(button_frame, text="Neue Notiz hinzufügen", command=self.add_note)
        self.button_add.pack(side=tk.LEFT, padx=5)

        self.button_delete = ttk.Button(button_frame, text="Als Erledigt markieren", command=self.delete_note)
        self.button_delete.pack(side=tk.LEFT, padx=5)

        self.button_edit = ttk.Button(button_frame, text="Notiz bearbeiten", command=self.edit_note)
        self.button_edit.pack(side=tk.LEFT, padx=5)

        self.button_toggle = ttk.Button(button_frame, text="Dark Mode", command=self.toggle_dark_mode)
        self.button_toggle.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

    def load_notes(self):
        try:
            self.c.execute("SELECT timestamp, notiz, kategorie FROM notizen")
            rows = self.c.fetchall()
            for row in rows:
                notiz_mit_zeit = f"{row[0]} - {row[1]} ({row[2]})"
                self.notizen.append(notiz_mit_zeit)
                self.listbox.insert(tk.END, notiz_mit_zeit)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def add_note(self):
        notiz = self.eingabe.get()
        kategorie = self.category_var.get()
        if notiz:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notiz_mit_zeit = f"{timestamp} - {notiz} ({kategorie})"
            self.notizen.append(notiz_mit_zeit)
            self.listbox.insert(tk.END, notiz_mit_zeit)
            self.eingabe.delete(0, tk.END)
            try:
                self.c.execute("INSERT INTO notizen (timestamp, notiz, kategorie) VALUES (?, ?, ?)", (timestamp, notiz, kategorie))
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
            notiz_text, kategorie = notiz_text.rsplit(" (", 1)
            kategorie = kategorie.rstrip(")")
            try:
                self.c.execute("DELETE FROM notizen WHERE timestamp = ? AND notiz = ? AND kategorie = ?", (timestamp, notiz_text, kategorie))
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
            old_text, kategorie = old_text.rsplit(" (", 1)
            kategorie = kategorie.rstrip(")")
            new_text = simpledialog.askstring("Notiz bearbeiten", "Bearbeiten Sie die Notiz:", initialvalue=old_text)
            if new_text:
                new_note = f"{timestamp} - {new_text} ({kategorie})"
                self.notizen[index] = new_note
                self.listbox.delete(index)
                self.listbox.insert(index, new_note)
                try:
                    self.c.execute("UPDATE notizen SET notiz = ? WHERE timestamp = ? AND notiz = ? AND kategorie = ?", (new_text, timestamp, old_text, kategorie))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Notiz bearbeitet")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.configure(bg='black')
            self.time_label.configure(bg='black', fg='white')
            self.eingabe.configure(style='TEntry')
            self.category_label.configure(background='black', foreground='white')
            self.category_menu.configure(style='TCombobox')
            self.listbox.configure(bg='black', fg='white')
        else:
            self.root.configure(bg='white')
            self.time_label.configure(bg='white', fg='black')
            self.eingabe.configure(style='TEntry')
            self.category_label.configure(background='white', foreground='black')
            self.category_menu.configure(style='TCombobox')
            self.listbox.configure(bg='white', fg='black')

    def add_category(self):
        new_category = simpledialog.askstring("Neue Kategorie", "Geben Sie den Namen der neuen Kategorie ein:")
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_menu['values'] = self.categories
            messagebox.showinfo("Success", "Kategorie hinzugefügt")

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