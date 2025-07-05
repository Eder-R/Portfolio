import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
import os
import sys

class LibManagerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("LibManager - Controle do Servidor")
        self.root.geometry("320x180")
        self.root.resizable(False, False)

        self.server_process = None
        self.url = "http://127.0.0.1:5000"

        self.status_label = tk.Label(root, text="Servidor parado", fg="red", font=("Arial", 12))
        self.status_label.pack(pady=8)

        self.url_label = tk.Label(root, text=self.url, fg="blue", font=("Arial", 10, "underline"), cursor="hand2")
        self.url_label.pack()
        self.url_label.bind("<Button-1>", lambda e: webbrowser.open(self.url))

        self.start_button = tk.Button(root, text="Iniciar Servidor", command=self.iniciar_servidor, bg="green", fg="white")
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Encerrar Servidor", command=self.parar_servidor, state=tk.DISABLED, bg="darkred", fg="white")
        self.stop_button.pack(pady=5)

        self.open_button = tk.Button(root, text="Abrir no navegador", command=self.abrir_navegador, state=tk.DISABLED)
        self.open_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def iniciar_servidor(self):
        if self.server_process is None:
            if getattr(sys, 'frozen', False):
                script_path = os.path.join(os.path.dirname(sys.executable), "LibManager.exe")
            else:
                script_path = [sys.executable, "app.py"]

            try:
                self.server_process = subprocess.Popen(script_path if isinstance(script_path, list) else [script_path])
                self.status_label.config(text="Servidor em execução", fg="green")
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.open_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao iniciar servidor:\n{e}")

    def parar_servidor(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            self.status_label.config(text="Servidor parado", fg="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.open_button.config(state=tk.DISABLED)

    def abrir_navegador(self):
        webbrowser.open(self.url)

    def on_close(self):
        if self.server_process:
            if messagebox.askyesno("Encerrar", "Deseja encerrar o servidor antes de sair?"):
                self.parar_servidor()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibManagerLauncher(root)
    root.mainloop()
