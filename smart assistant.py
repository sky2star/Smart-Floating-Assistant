import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QRadialGradient
from PyQt5.QtCore import Qt, QPoint
from model_interaction import generate_response

class FloatingBall(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)
        self.move(QApplication.desktop().screen().rect().right() - 70,
                  QApplication.desktop().screen().rect().bottom() - 70)
        self.dragging = False
        self.offset = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QRadialGradient(30, 30, 30, 20, 20)
        gradient.setColorAt(0, QColor(70, 130, 180))
        gradient.setColorAt(0.8, QColor(30, 80, 120))
        gradient.setColorAt(1, QColor(20, 60, 100))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 60, 60)

        highlight = QRadialGradient(25, 25, 25, 15, 15)
        highlight.setColorAt(0, QColor(255, 255, 255, 100))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawEllipse(5, 5, 50, 50)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.hide()
            self.parent().show()
            self.parent().activateWindow()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initFloatingBall()
        print("应用程序已启动")
        self.show()

    def initUI(self):
        self.setWindowTitle('GPT 查询工具')
        self.setWindowIcon(QIcon('R.jpg'))
        self.setGeometry(300, 300, 600, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        labelInput = QLabel("输入或粘贴文字:")
        layout.addWidget(labelInput)

        self.textEdit = QTextEdit(self)
        self.textEdit.setPlaceholderText("在此输入问题或粘贴文字 (Ctrl+V)...")
        layout.addWidget(self.textEdit)

        self.submitButton = QPushButton('提交', self)
        self.submitButton.clicked.connect(self.on_submit)
        layout.addWidget(self.submitButton)

        self.hideButton = QPushButton('隐藏', self)
        self.hideButton.clicked.connect(self.toggleVisibility)
        layout.addWidget(self.hideButton)

        labelOutput = QLabel("AI 回答:")
        layout.addWidget(labelOutput)

        self.textOutput = QTextEdit(self)
        self.textOutput.setReadOnly(True)
        layout.addWidget(self.textOutput)

        self.setLayout(layout)

    def initFloatingBall(self):
        self.floatingBall = FloatingBall(self)

    def toggleVisibility(self):
        self.hide()
        self.floatingBall.show()

    def on_submit(self):
        question = self.textEdit.toPlainText()
        answer = generate_response(question)
        self.textOutput.setText(answer)

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()