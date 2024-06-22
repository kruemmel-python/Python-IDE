import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import queue

# Hauptfenster erstellen
root = tk.Tk()
root.title("Interaktive Python-Konsole")

# Textbox für die Codeeingabe
code_input = scrolledtext.ScrolledText(root, height=20)
code_input.pack(fill=tk.BOTH, expand=True)

# Textbox für die Ausgabe und Eingabe
console_output = scrolledtext.ScrolledText(root, height=20)
console_output.pack(fill=tk.BOTH, expand=True)

# Queue für die Kommunikation zwischen Threads
output_queue = queue.Queue()

# Funktion zum Ausführen des Codes in einem separaten Thread
def run_code():
    # Eingabe aus der Textbox holen
    code = code_input.get("1.0", tk.END)
    # Temporäre Datei erstellen und Code hineinschreiben
    with open("temp_code.py", "w", encoding="utf-8") as file:
        # Encoding-Deklaration hinzufügen
        file.write("# -*- coding: utf-8 -*-\n")
        file.write(code)
    print("temp_code.py erstellt mit folgendem Inhalt:")
    print(code)
    
    # Python-Subprozess starten
    process = subprocess.Popen(["python", "-u", "temp_code.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    
    # Thread für das Lesen der Ausgabe
    def read_output(process, output_queue):
        for line in iter(process.stdout.readline, ''):
            output_queue.put(line)
        for line in iter(process.stderr.readline, ''):
            output_queue.put(line)
        process.stdout.close()
        process.stderr.close()
    
    # Thread starten, um die Ausgabe zu lesen
    threading.Thread(target=read_output, args=(process, output_queue)).start()

    # Funktion zum Aktualisieren der Ausgabe
    def update_output():
        while not output_queue.empty():
            line = output_queue.get()
            if line:
                console_output.insert(tk.END, line)
                console_output.see(tk.END)
        root.after(50, update_output)  # Reduziere das Intervall auf 50ms
    
    # Update-Funktion regelmäßig aufrufen
    update_output()

    # Funktion zum Senden von Eingaben
    def send_input(event):
        input_text = console_output.get("end-1c linestart", "end-1c")
        console_output.delete("end-1c linestart", "end-1c")
        print(f"Eingabe gesendet: {input_text}")
        process.stdin.write(input_text + '\n')
        process.stdin.flush()
    
    # Event-Handler für Eingaben
    console_output.bind('<Return>', send_input)

# Schaltfläche zum Ausführen des Codes
run_button = tk.Button(root, text="Code ausführen", command=run_code)
run_button.pack()

# Hauptloop starten
root.mainloop()
