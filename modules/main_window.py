from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer, QUrl
from PyQt6.QtCore import pyqtSignal
from labels.text_box import TextBox
from labels.images import Images
from labels.face import Face

from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    signal_start_tracking = pyqtSignal()
    signal_stop_tracking = pyqtSignal()

    signal_start_listening = pyqtSignal()
    signal_ajust_noise = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotin")
        self.setStyleSheet("background-color: rgb(194,216,214);")
        self.showFullScreen()
        self.set_layout()

    def set_layout(self):
        self.layout = QVBoxLayout()

        self.h_layout = QHBoxLayout()

        # add face
        self.face = Face()

        # add web view
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://v2.ubicate.osuc.dev/map?place=B12"))
        self.webview.hide()

        self.layout.addWidget(self.face, 3)
        self.layout.addWidget(self.webview, 20)

        self.h_layout.addWidget(self.face, 1)
        self.h_layout.addWidget(self.webview, 1)
        self.layout.addLayout(self.h_layout, 3)


        # add text box
        self.text_box = TextBox("", self)
        self.layout.addWidget(self.text_box, 1)
        self.text_box.hide()

        # add image label
        self.image_label = Images()
        self.layout.addWidget(self.image_label, 27)
        self.image_label.hide()



        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        if event.key() == Qt.Key.Key_1:
            self.text_box.hide()
            self.image_label.hide()
            self.webview.hide()
        if event.key() == Qt.Key.Key_2:
            self.text_box.show()
            self.image_label.hide()
            self.webview.hide()
        if event.key() == Qt.Key.Key_3:
            self.text_box.hide()
            self.image_label.show()
            self.webview.hide()
        if event.key() == Qt.Key.Key_4:
            self.text_box.hide()
            self.image_label.hide()
            self.webview.show()
        if event.key() == Qt.Key.Key_Space:
            self.face.speaking = not self.face.speaking

        if event.key() == Qt.Key.Key_D:
            self.face.setMouseTracking(False)
            self.signal_start_tracking.emit()

        if event.key() == Qt.Key.Key_S:
            self.face.setMouseTracking(True)
            self.signal_stop_tracking.emit()

        if event.key() == Qt.Key.Key_L:
            self.signal_start_listening.emit()
        if event.key() == Qt.Key.Key_H:
            self.signal_ajust_noise.emit()

    def listening(self):
        self.face.speaking = False
        self.text_box.setText("Escuchando...")
        self.text_box.show()
        self.image_label.hide()

    def speech_detected(self, text):
        self.face.speaking = True
        self.text_box.setText(ajust_text(text))
        self.text_box.show()
        self.image_label.hide()


def ajust_text(text):
    text = text.split("\n")
    i = 0
    while i < len(text):
        if len(text[i]) > 80:
            text.insert(i+1, text[i][80:])
            text[i] = text[i][:80]
        i += 1
    return "\n".join(text)