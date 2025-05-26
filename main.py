import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from app import app  # importa seu Flask

def start_flask():
    app.run(debug=False, use_reloader=False)

class LibManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LibManager")
        self.setGeometry(100, 100, 1024, 768)

        browser = QWebEngineView()
        browser.setUrl(QUrl("http://127.0.0.1:5000"))
        self.setCentralWidget(browser)

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()
    qt_app = QApplication(sys.argv)
    window = LibManagerApp()
    window.show()
    sys.exit(qt_app.exec_())
