import webview
import threading
import subprocess
import sys
import os
import webbrowser

class Api:
    def __init__(self):
        self.process = None
        self.url = "http://127.0.0.1:5000"

    def start_server(self):
        if self.process is None:
            if getattr(sys, 'frozen', False):
                script_path = os.path.join(os.path.dirname(sys.executable), "LibManager.exe")
            else:
                script_path = [sys.executable, "app.py"]
            try:
                self.process = subprocess.Popen(script_path if isinstance(script_path, list) else [script_path])
                return "Servidor iniciado com sucesso!"
            except Exception as e:
                return f"Erro ao iniciar servidor: {e}"
        return "Servidor já está em execução."

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
            return "Servidor encerrado com sucesso!"
        return "Servidor não está em execução."

    def open_browser(self):
        webbrowser.open(self.url)
        return f"Abrindo {self.url}..."

def run_gui():
    api = Api()
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LibManager</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 40px; }
            button { padding: 10px 20px; margin: 10px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2 id="status">Servidor parado</h2>
        <p><a href="#" onclick="abrir()">http://127.0.0.1:5000</a></p>
        <button onclick="iniciar()">Iniciar Servidor</button>
        <button onclick="parar()">Encerrar Servidor</button>
        <button onclick="abrir()">Abrir no navegador</button>
        <p id="msg"></p>
        <script>
            function iniciar() {
                window.pywebview.api.start_server().then(msg => {
                    document.getElementById('status').innerText = 'Servidor em execução';
                    document.getElementById('msg').innerText = msg;
                });
            }
            function parar() {
                window.pywebview.api.stop_server().then(msg => {
                    document.getElementById('status').innerText = 'Servidor parado';
                    document.getElementById('msg').innerText = msg;
                });
            }
            function abrir() {
                window.pywebview.api.open_browser().then(msg => {
                    document.getElementById('msg').innerText = msg;
                });
            }
        </script>
    </body>
    </html>
    """

    window = webview.create_window("LibManager - Controle", html=html, width=500, height=500, js_api=api)
    webview.start(gui='edgechromium' if sys.platform == 'win32' else None)

if __name__ == "__main__":
    run_gui()
