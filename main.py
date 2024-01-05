import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil

def ordner_auswaehlen():
    # Öffne den Datei-Dialog, um einen Ordner auszuwählen
    ordner_pfad = filedialog.askdirectory()

    # Aktualisiere das Label mit dem ausgewählten Ordner oder dem Standardtext
    if ordner_pfad:
        label_ausgewaehlter_ordner.config(text=f"Ausgewählter Ordner: {ordner_pfad}")
        # Aktualisiere den Status des Funktionsaufruf-Buttons
        button_funktion_ausfuehren.config(state=tk.NORMAL)
    else:
        label_ausgewaehlter_ordner.config(text="Bitte wählen Sie einen Ordner aus")
        button_funktion_ausfuehren.config(state=tk.DISABLED)

def funktion_ausfuehren():
    # Hole den ausgewählten Ordnerpfad
    ordner_pfad = label_ausgewaehlter_ordner.cget('text')[21:]

    # Drucke den ausgewählten Ordnerpfad zur Überprüfung
    print(f"Ausgewählter Ordnerpfad: {ordner_pfad}")

    try:
        # Initialisiere die ProgressBar
        progress_bar_var.set(0)
        fenster.update_idletasks()  # Aktualisiere das Fenster, um die ProgressBar sofort zu zeigen

        # Verschiebe und leere den Ordner
        verschiebe_und_leere(ordner_pfad)

        # Zeige Erfolgsmeldung an
        messagebox.showinfo("Erfolg", "Alle Dateien wurden verschoben, und leere Ordner wurden gelöscht.")
    except Exception as e:
        # Zeige Fehlermeldung an
        messagebox.showerror("Fehler", f"Fehler beim Verschieben und Leeren des Ordners: {str(e)}")
    finally:
        # Setze den ProgressBar-Wert auf 100% (Vollständig)
        progress_bar_var.set(100)

def verschiebe_und_leere(ordner_pfad):
    total_files = sum(len(files) for _, _, files in os.walk(ordner_pfad))
    processed_files = 0

    # Durchlaufe alle Dateien und Ordner im angegebenen Ordner und dessen Unterordnern
    for ordner, _, dateien in os.walk(ordner_pfad):
        for datei in dateien:
            # Konstruiere die Pfade
            element_pfad = os.path.join(ordner, datei)
            ziel_pfad = os.path.join(ordner_pfad, datei)

            # Verschiebe die Datei nur, wenn sich der Pfad ändert
            if element_pfad != ziel_pfad:
                shutil.move(element_pfad, ziel_pfad)

            # Aktualisiere den ProgressBar-Wert
            processed_files += 1
            progress_value = int(processed_files / total_files * 100)
            progress_bar_var.set(progress_value)
            fenster.update_idletasks()  # Aktualisiere das Fenster, um die ProgressBar sofort zu zeigen

    # Durchlaufe alle Ordner und lösche leere Ordner
    for ordner, _, _ in os.walk(ordner_pfad, topdown=False):
        try:
            os.rmdir(ordner)
        except OSError:
            pass  # Ignoriere nicht leere Ordner

    # Verschiebe die Dateien in separate Ordner basierend auf ihrem Dateityp
    for datei in os.listdir(ordner_pfad):
        element_pfad = os.path.join(ordner_pfad, datei)

        # Erstelle einen Zielordner basierend auf dem Dateityp (Erweiterung)
        dateityp = os.path.splitext(datei)[1].lower()[1:]  # Erhalte die Dateiendung (ohne Punkt) in Kleinbuchstaben

        # Behandle spezielle Fälle für JPEG-Dateien
        if dateityp == 'jpeg':
            dateityp = 'jpg'

        # Erstelle den Zielordner, wenn er nicht existiert
        ziel_ordner = os.path.join(ordner_pfad, dateityp)
        os.makedirs(ziel_ordner, exist_ok=True)

        # Verschiebe die Datei in den Zielordner
        ziel_pfad = os.path.join(ziel_ordner, datei.lower())
        shutil.move(element_pfad, ziel_pfad)

# Erstelle das Hauptfenster
fenster = tk.Tk()
fenster.title("Dateien nach Typ sortieren")

# Setze Breite und Höhe des Fensters
fenster.geometry("600x250")

# Verhindere, dass das Fenster maximiert werden kann
fenster.resizable(False, False)

# Erstelle ein Label für den ausgewählten Ordnerpfad
label_ausgewaehlter_ordner = tk.Label(fenster, text="Bitte wählen Sie einen Ordner aus", wraplength=500, justify="left")
label_ausgewaehlter_ordner.pack(pady=10)

# Erstelle eine Schaltfläche zum Auswählen eines Ordners
button_ordner_auswaehlen = tk.Button(fenster, text="Ordner auswählen", command=ordner_auswaehlen, width=60, height=2)
button_ordner_auswaehlen.pack(pady=10)

# Erstelle die ProgressBar-Variable
progress_bar_var = tk.IntVar()

# Erstelle die ProgressBar
progress_bar = ttk.Progressbar(fenster, variable=progress_bar_var, length=430, mode="determinate")
progress_bar.pack(pady=10)

# Erstelle einen Button zum Ausführen einer Funktion
button_funktion_ausfuehren = tk.Button(fenster, text="Programm starten", command=funktion_ausfuehren, width=60, height=2, state=tk.DISABLED)
button_funktion_ausfuehren.pack(pady=10)

# Starte die Tkinter-Schleife
fenster.mainloop()