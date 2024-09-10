from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtCore import pyqtSignal


class Face(QWidget):

    blink_step = 6
    speak_step = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMouseTracking(True)

        self.scale = 10

        self.blink_count = 0
        self.speak_count = 0

        self.eye_size = 12
        self.mouth_size = 1

        self.speaking = 0

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(self.blink_step)

        self.speak_timer = QTimer(self)
        self.speak_timer.timeout.connect(self.speak)
        self.speak_timer.start(self.speak_step)

        self.pose = QPoint(self.c_x, self.c_y)
        self.target = QPoint(self.c_x, self.c_y)
        self.face_timer = QTimer(self)
        self.face_timer.timeout.connect(self.move_face)
        self.face_timer.start(10)


    @property
    def c_x(self):
        return int(self.width()/2)

    @property
    def c_y(self):
        return int(self.height()/2)

    def resizeEvent(self, event):
        self.scale = min(event.size().height()*0.015, event.size().width()*0.01)
        self.centro_ojos = QPoint(self.c_x, self.c_y)
        self.centro_boca = QPoint(self.c_x, self.c_y + int(self.scale*8))
        self.target_cero()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # -- Ojos --
        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(self.centro_ojos + QPoint(-int(20 * self.scale), 0), int(5 * self.scale), int(self.eye_size * self.scale))
        painter.drawEllipse(self.centro_ojos + QPoint( int(20 * self.scale), 0), int(5 * self.scale), int(self.eye_size * self.scale))

        # -- Boca --
        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(
            self.centro_boca,
            int(6 * self.scale),
            int(3 * self.scale))

        painter.setBrush(QBrush(QColor(194, 216, 214)))
        painter.drawEllipse(
            self.centro_boca,
            int(5 * self.scale),
            int(2 * self.scale * self.mouth_size))
        painter.drawRect(
            self.centro_boca.x() - int(6 * self.scale),
            self.centro_boca.y() - int(4 * self.scale),
            int(12 * self.scale),
            int( 4 * self.scale))

        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(self.centro_boca + QPoint(
            -int(5.5 * self.scale), 0),
            int(0.55 * self.scale),
            int(0.55 * self.scale))
        painter.drawEllipse(self.centro_boca + QPoint(
            int(5.5 * self.scale), 0),
            int(0.55 * self.scale),
            int(0.55 * self.scale))

    def mouseMoveEvent(self, event):
        self.target = event.pos()

    def move_face(self):
        self.step_face()
        self.centro_ojos = QPoint(
            int(self.c_x + (self.pose.x() - self.c_x) * 0.5),
            int(self.c_y + (self.pose.y() - self.c_y) * 0.5)
        )
        self.centro_boca = QPoint(
            int(self.c_x + (self.pose.x() - self.c_x) * 0.45),
            int(self.c_y + (self.pose.y() - self.c_y) * 0.45) + int(8 * self.scale)
        )
        self.update()

    def blink(self):
        self.blink_count += self.blink_step
        if self.blink_count < 100:
            self.eye_size = 12 - self.blink_count/10
        elif self.blink_count < 200:
            self.eye_size = 2 + (self.blink_count - 100)/10
        elif self.blink_count > 4000:
            self.blink_count = 0
        self.update()

    def speak(self):
        if self.speaking:
            self.speak_count += self.speak_step
            if self.speak_count < 150:
                self.mouth_size = 1 - self.speak_count/150
            elif self.speak_count < 300:
                self.mouth_size = (self.speak_count - 150)/300
            else:
                self.speak_count = 0
        else:
            self.speak_count = 100
            self.mouth_size = 1

    def step_face(self):
        self.pose = QPoint(
            int(self.pose.x() + (self.target.x() - self.pose.x()) * 0.3),
            int(self.pose.y() + (self.target.y() - self.pose.y()) * 0.3)
        )

    def face_tracking_target(self, x, y):
        self.target = QPoint(
            int(self.width()  * x * 0.6 + self.width()  * 0.15),
            int(self.height() * y * 0.8 + self.height() * 0.1)
        )

    def target_cero(self):
        self.target = QPoint(self.c_x, self.c_y)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.blink_count = 75
