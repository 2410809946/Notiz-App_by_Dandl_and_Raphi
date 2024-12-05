# 16.11.2024
# Notizbuch-App by Dandl and Raphi

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

class NotizbuchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notizbuch-App by Dandl and Raphi")
        self.root.geometry("500x415")
        self.root.minsize(300, 200)

        self.notizen = []
        self.dark_mode = False
        self.categories = []

        self.conn = sqlite3.connect('notizen.db')
        self.c = self.conn.cursor()
        self.create_table()

        self.load_categories()
        self.create_widgets()
        self.load_notes()
        self.update_time()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS notizen
                              (id INTEGER PRIMARY KEY, timestamp TEXT, notiz TEXT, kategorie TEXT, faelligkeit TEXT)''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS kategorien
                              (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
            self.conn.commit()
        except sqlite3.Error as e:
            if "duplicate column name" not in str(e):
                messagebox.showerror("Database Error", str(e))

    def create_widgets(self):
        self.time_label = tk.Label(self.root, font=('Helvetica', 10))
        self.time_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        entry_frame = ttk.Frame(self.root)
        entry_frame.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        self.todo_label = ttk.Label(entry_frame, text="To Do:")
        self.todo_label.grid(row=0, column=0, padx=5, sticky='w')

        self.falligkeit_label = ttk.Label(entry_frame, text="Fälligkeit:")
        self.falligkeit_label.grid(row=0, column=1, padx=5, sticky='w')

        self.eingabe = ttk.Entry(entry_frame, width=62)
        self.eingabe.grid(row=1, column=0, padx=0, sticky='w')

        self.eingabe2 = DateEntry(entry_frame, date_pattern='yyyy-mm-dd')
        self.eingabe2.grid(row=1, column=1, padx=5, sticky='w')

        self.category_label = ttk.Label(self.root, text="Kategorie:")
        self.category_label.grid(row=2, column=0, pady=5, padx=148, sticky='ew', columnspan=2)

        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.category_var, width=10)
        self.category_menu['values'] = self.categories
        self.category_menu.current(0)
        self.category_menu.grid(row=3, column=0, pady=5, padx=150, sticky='ew', columnspan=1)

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, pady=5, padx=10, sticky='ew', columnspan=2)

        self.add_category_button = ttk.Button(button_frame, text="Neue Kategorie", command=self.add_category, width=20)
        self.add_category_button.grid(row=0, column=0, sticky='ew', padx=5)

        self.remove_category_button = ttk.Button(button_frame, text="Kategorie entfernen", command=self.delete_category, width=20)
        self.remove_category_button.grid(row=0, column=1, sticky='ew', padx=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        button_frame2 = ttk.Frame(self.root)
        button_frame2.grid(row=5, column=0, pady=10, padx=10, sticky='w')

        self.button_add = ttk.Button(button_frame2, text="Neue Notiz hinzufügen", command=self.add_note)
        self.button_add.grid(row=0, column=0, padx=5)

        self.button_delete = ttk.Button(button_frame2, text="Als Erledigt markieren", command=self.delete_note)
        self.button_delete.grid(row=0, column=1, padx=5)

        self.button_edit = ttk.Button(button_frame2, text="Notiz bearbeiten", command=self.edit_note)
        self.button_edit.grid(row=0, column=2, padx=5)

        self.button_toggle = ttk.Button(button_frame2, text="Dark Mode", command=self.toggle_dark_mode)
        self.button_toggle.grid(row=0, column=3, padx=5)

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=6, column=0, pady=10, padx=10, sticky='nsew')

    def load_categories(self):
        try:
            self.c.execute("SELECT name FROM kategorien")
            rows = self.c.fetchall()
            if not rows:
                self.categories = ["Freizeit", "Geschäftliches", "Anderes"]
                for category in self.categories:
                    self.c.execute("INSERT INTO kategorien (name) VALUES (?)", (category,))
                self.conn.commit()
            else:
                self.categories = [row[0] for row in rows]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

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
        faelligkeit = self.eingabe2.get_date().strftime("%Y-%m-%d")
        if notiz:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notiz_mit_zeit = f"{timestamp} - {notiz} ({kategorie}) - Fällig bis: {faelligkeit}"
            self.notizen.append(notiz_mit_zeit)
            self.listbox.insert(tk.END, notiz_mit_zeit)
            self.eingabe.delete(0, tk.END)
            try:
                self.c.execute("INSERT INTO notizen (timestamp, notiz, kategorie, faelligkeit) VALUES (?, ?, ?, ?)",
                               (timestamp, notiz, kategorie, faelligkeit))
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
            try:
                self.c.execute("INSERT INTO kategorien (name) VALUES (?)", (new_category,))
                self.conn.commit()
                self.categories.append(new_category)
                self.category_menu['values'] = self.categories
                messagebox.showinfo("Success", "Kategorie hinzugefügt")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def delete_category(self):
        #Ausgewählte Kategorie in Dropdown-Menü in categories und der SQL Datenbank löschen
        selected_category = self.category_menu.get()
        if selected_category in self.categories:
            self.categories.remove(selected_category)
            self.category_menu['values'] = self.categories
            try:
                self.c.execute("DELETE FROM kategorien WHERE name = ?", (selected_category,))
                self.conn.commit()
                self.category_menu.current(0)
                messagebox.showinfo("Success", "Kategorie gelöscht")
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