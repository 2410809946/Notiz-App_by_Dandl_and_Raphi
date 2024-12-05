# 16.11.2024
# Notizbuch-App by Dandl and Raphi

# Imports
import tkinter as tk  # Importiere das tkinter Modul für GUI-Erstellung
from tkinter import ttk, messagebox, simpledialog  # Importiere spezifische tkinter-Module
from tkcalendar import DateEntry  # Importiere DateEntry für Datumsauswahl
from datetime import datetime  # Importiere datetime für Zeit- und Datumsfunktionen
import sqlite3  # Importiere sqlite3 für Datenbankoperationen


class NotizbuchApp:
    # Konstruktor
    def __init__(self, root):
        # Initialisiere das Hauptfenster
        self.root = root
        self.root.title("Notizbuch-App by Dandl and Raphi")
        self.root.geometry("500x415")
        self.root.minsize(300, 200)

        # Definiere Variablen
        self.notizen = []  # Liste für Notizen
        self.dark_mode = False  # Boolean für Dark Mode
        self.categories = []  # Liste für Kategorien

        # Erstelle SQL-Datenbank
        self.conn = sqlite3.connect('notizen.db')  # Verbindung zur SQLite-Datenbank
        self.c = self.conn.cursor()  # Erstelle einen Cursor für Datenbankoperationen
        self.create_table()  # Erstelle die notwendigen Tabellen

        # Lade Kategorien und Notizen
        self.load_categories()  # Lade Kategorien aus der Datenbank
        self.create_widgets()  # Erstelle die GUI-Widgets
        self.load_notes()  # Lade Notizen aus der Datenbank
        self.update_time()  # Starte die Zeitaktualisierung

    # Erstelle SQL-Tabellen
    def create_table(self):
        try:
            # Erstelle Tabelle für Notizen
            self.c.execute('''CREATE TABLE IF NOT EXISTS notizen
                              (id INTEGER PRIMARY KEY, timestamp TEXT, notiz TEXT, kategorie TEXT, faelligkeit TEXT)''')
            # Erstelle Tabelle für Kategorien
            self.c.execute('''CREATE TABLE IF NOT EXISTS kategorien
                              (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
            self.conn.commit()  # Speichere Änderungen
        except sqlite3.Error as e:
            if "duplicate column name" not in str(e):
                messagebox.showerror("Database Error", str(e))  # Zeige Fehlermeldung an

    # Erstelle Widgets des GUI-Fensters
    def create_widgets(self):
        # Erstelle Zeitlabel
        self.time_label = tk.Label(self.root, font=('Helvetica', 10))
        self.time_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Definiere Entry-Frame und Grid
        self.entry_frame = ttk.Frame(self.root)
        self.entry_frame.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        # Erstelle ToDoLabel
        self.todo_label = ttk.Label(self.entry_frame, text="To Do:")
        self.todo_label.grid(row=0, column=0, padx=5, sticky='w')

        # Erstelle Fälligkeit-Label
        self.falligkeit_label = ttk.Label(self.entry_frame, text="Fälligkeit:")
        self.falligkeit_label.grid(row=0, column=1, padx=5, sticky='w')

        # Erstelle Entry und DateEntry
        self.ToDoEntry = ttk.Entry(self.entry_frame, width=62)
        self.ToDoEntry.grid(row=1, column=0, padx=0, sticky='w')

        self.DateEntry = DateEntry(self.entry_frame, date_pattern='yyyy-mm-dd')
        self.DateEntry.grid(row=1, column=1, padx=5, sticky='w')

        # Erstelle Kategorie-Label und Kategorie-Menü
        self.category_label = ttk.Label(self.root, text="Kategorie:")
        self.category_label.grid(row=2, column=0, pady=5, padx=148, sticky='ew', columnspan=2)

        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.category_var, width=10)
        self.category_menu['values'] = self.categories
        self.category_menu.current(0)
        self.category_menu.grid(row=3, column=0, pady=5, padx=150, sticky='ew', columnspan=1)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=4, column=0, pady=5, padx=10, sticky='ew', columnspan=2)

        # Erstelle Kategorie-Buttons
        self.button_add_category = ttk.Button(self.button_frame, text="Neue Kategorie", command=self.add_category,
                                              width=20)
        self.button_add_category.grid(row=0, column=0, sticky='ew', padx=5)

        self.button_delete_category = ttk.Button(self.button_frame, text="Kategorie entfernen",
                                                 command=self.delete_category, width=20)
        self.button_delete_category.grid(row=0, column=1, sticky='ew', padx=5)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.button_frame2 = ttk.Frame(self.root)
        self.button_frame2.grid(row=5, column=0, pady=10, padx=10, sticky='w')

        self.button_add_note = ttk.Button(self.button_frame2, text="Neue Notiz hinzufügen", command=self.add_note)
        self.button_add_note.grid(row=0, column=0, padx=5)

        self.button_delete_note = ttk.Button(self.button_frame2, text="Als Erledigt markieren",
                                             command=self.delete_note)
        self.button_delete_note.grid(row=0, column=1, padx=5)

        self.button_edit_note = ttk.Button(self.button_frame2, text="Notiz bearbeiten", command=self.edit_note)
        self.button_edit_note.grid(row=0, column=2, padx=5)

        self.button_toggle = ttk.Button(self.button_frame2, text="Dark Mode", command=self.toggle_dark_mode)
        self.button_toggle.grid(row=0, column=3, padx=5)

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=6, column=0, pady=10, padx=10, sticky='nsew')

    # Lade Kategorien aus der Datenbank
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

    # Lade Notizen aus der Datenbank
    def load_notes(self):
        try:
            self.c.execute("SELECT timestamp, notiz, kategorie, faelligkeit FROM notizen")
            rows = self.c.fetchall()
            for row in rows:
                notiz_mit_zeit = f"{row[0]} - {row[1]} ({row[2]}) - Fällig bis: {row[3]}"
                self.notizen.append(notiz_mit_zeit)
                self.listbox.insert(tk.END, notiz_mit_zeit)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    # Füge eine neue Notiz hinzu
    def add_note(self):
        notiz = self.ToDoEntry.get()
        kategorie = self.category_var.get()
        faelligkeit = self.DateEntry.get_date().strftime("%Y-%m-%d")
        if notiz:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notiz_mit_zeit = f"{timestamp} - {notiz} ({kategorie}) - Fällig bis: {faelligkeit}"
            self.notizen.append(notiz_mit_zeit)
            self.listbox.insert(tk.END, notiz_mit_zeit)
            self.ToDoEntry.delete(0, tk.END)
            try:
                self.c.execute("INSERT INTO notizen (timestamp, notiz, kategorie, faelligkeit) VALUES (?, ?, ?, ?)",
                               (timestamp, notiz, kategorie, faelligkeit))
                self.conn.commit()
                messagebox.showinfo("Success", "Notiz hinzugefügt")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    # Lösche eine Notiz
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
                self.c.execute("DELETE FROM notizen WHERE timestamp = ? AND notiz = ? AND kategorie = ?",
                               (timestamp, notiz_text, kategorie))
                self.conn.commit()
                messagebox.showinfo("Success", "Notiz gelöscht")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    # Bearbeite eine Notiz
    def edit_note(self):
        selected_note_indices = self.listbox.curselection()
        if selected_note_indices:
            index = selected_note_indices[0]
            old_note = self.listbox.get(index)
            timestamp, old_text = old_note.split(" - ", 1)
            old_text, kategorie = old_text.rsplit(" (", 1)

            if " - Fällig bis: " in kategorie:
                kategorie, faelligkeit = kategorie.rsplit(" - Fällig bis: ", 1)
            else:
                faelligkeit = datetime.now().strftime("%Y-%m-%d")  # Setze Standarddatum, falls faelligkeit leer ist

            kategorie = kategorie.rstrip(")")

            # Erstelle ein neues Toplevel-Fenster zum Bearbeiten
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Notiz bearbeiten")

            # Text-Widget zum Bearbeiten der Beschreibung
            text_widget = tk.Text(edit_window, height=5, width=40)
            text_widget.insert(tk.END, old_text)
            text_widget.pack(pady=10)

            # DateEntry-Widget zum Bearbeiten des Fälligkeitsdatums
            date_entry = DateEntry(edit_window, date_pattern='yyyy-mm-dd')
            date_entry.set_date(faelligkeit)
            date_entry.pack(pady=10)

            # Combobox zum Bearbeiten der Kategorie
            category_var = tk.StringVar(value=kategorie)
            category_menu = ttk.Combobox(edit_window, textvariable=category_var, values=self.categories)
            category_menu.pack(pady=10)

            def save_changes():
                new_text = text_widget.get("1.0", tk.END).strip()
                new_faelligkeit = date_entry.get_date().strftime("%Y-%m-%d")
                new_kategorie = category_var.get()
                if new_text and new_faelligkeit and new_kategorie:
                    new_note = f"{timestamp} - {new_text} ({new_kategorie}) - Fällig bis: {new_faelligkeit}"
                    self.notizen[index] = new_note
                    self.listbox.delete(index)
                    self.listbox.insert(index, new_note)
                    try:
                        self.c.execute(
                            "UPDATE notizen SET notiz = ?, faelligkeit = ?, kategorie = ? WHERE timestamp = ? AND notiz = ? AND kategorie = ?",
                            (new_text, new_faelligkeit, new_kategorie, timestamp, old_text, kategorie))
                        self.conn.commit()
                        messagebox.showinfo("Success", "Notiz bearbeitet")
                    except sqlite3.Error as e:
                        messagebox.showerror("Database Error", str(e))
                edit_window.destroy()

            save_button = ttk.Button(edit_window, text="Speichern", command=save_changes)
            save_button.pack(pady=5)

    # Füge eine neue Kategorie hinzu
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

    # Lösche eine Kategorie
    def delete_category(self):
        # Ausgewählte Kategorie im Dropdown-Menü und in der SQL-Datenbank löschen
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

    # Schalte Dark Mode um
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        # Farben für Dark/Light Mode
        bg_color = 'black' if self.dark_mode else 'white'
        fg_color = 'white' if self.dark_mode else 'black'
        listbox_select_bg = 'gray' if self.dark_mode else 'systemHighlight'

        # 1. Hauptfenster und Zeitlabel (direkte Konfiguration für Zeitlabel, weil es ein tk.Label ist)
        self.root.configure(bg=bg_color)
        self.time_label.configure(bg=bg_color, fg=fg_color)


        style = ttk.Style()
        label_style = 'Dark.TLabel' if self.dark_mode else 'Light.TLabel'
        style.configure(label_style, background=bg_color, foreground=fg_color)
        for label in [self.todo_label, self.falligkeit_label, self.category_label]:
            label.configure(style=label_style)


        self.listbox.configure(
            bg=bg_color,
            fg=fg_color,
            selectbackground=listbox_select_bg,
            highlightbackground=fg_color,
            highlightcolor=fg_color
        )

        # 4. ttk.Entry anpassen (über Styles)
        # entry_style = 'Dark.TEntry' if self.dark_mode else 'Light.TEntry'
        # style.configure(entry_style, fieldbackground=bg_color, foreground=fg_color)
        # self.ToDoEntry.configure(style=entry_style)


        try:
            self.DateEntry.configure(
                background=bg_color,
                foreground=fg_color,
                selectbackground=listbox_select_bg,
                selectforeground=fg_color
            )
        except Exception as e:
            print(f"DateEntry Anpassung nicht unterstützt: {e}")

        # 6. ttk.Combobox anpassen (über Styles)
        # combobox_style = 'Dark.TCombobox' if self.dark_mode else 'Light.TCombobox'
        # style.configure(combobox_style, fieldbackground=bg_color, foreground='fg_color')
        # self.category_menu.configure(style=combobox_style)


        button_style = 'Dark.TButton' if self.dark_mode else 'Light.TButton'
        style.configure(button_style, background=bg_color, foreground='black')
        for button in [
            self.button_add_category, self.button_delete_category,
            self.button_add_note, self.button_delete_note,
            self.button_edit_note, self.button_toggle
        ]:
            button.configure(style=button_style)


        frame_style = 'Dark.TFrame' if self.dark_mode else 'Light.TFrame'
        style.configure(frame_style, background=bg_color)
        for frame in [self.entry_frame, self.button_frame, self.button_frame2]:
            frame.configure(style=frame_style)

    # Aktualisiere die Zeit
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    # Schließe die Anwendung und die Datenbankverbindung
    def on_closing(self):
        self.conn.close()
        self.root.destroy()


# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = NotizbuchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()