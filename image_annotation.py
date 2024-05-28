import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Annotation Tool')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMouseTracking(True)

        self.open_button = QPushButton('Open Image')
        self.open_button.clicked.connect(self.open_image)

        self.save_button = QPushButton('Save Annotations')
        self.save_button.clicked.connect(self.save_annotations)
        self.save_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.start_point = QPointF()
        self.end_point = QPointF()
        self.rectangles = []

        self.image_path = None
        self.pixmap = QPixmap()

        self.drawing = False

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            self.pixmap.load(self.image_path)
            self.image_label.setPixmap(self.pixmap)
            self.save_button.setEnabled(True)

    def save_annotations(self):
        # Implement your logic to save annotations
        print("Annotations saved:")
        for rect in self.rectangles:
            print(f"Rectangle: {rect}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image_label.pixmap() is not None:
            self.start_point = self.image_label.mapFromParent(event.pos())
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing and self.image_label.pixmap() is not None:
            self.end_point = self.image_label.mapFromParent(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing and self.image_label.pixmap() is not None:
            self.end_point = self.image_label.mapFromParent(event.pos())
            rect = QRectF(self.start_point, self.end_point).normalized()
            self.rectangles.append(rect)
            self.drawing = False
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.image_label.pixmap() is not None:
            painter = QPainter(self.image_label.pixmap())
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)

            for rect in self.rectangles:
                painter.drawRect(rect)

            if self.drawing:
                rect = QRectF(self.start_point, self.end_point).normalized()
                painter.drawRect(rect)

            painter.end()
            self.image_label.setPixmap(self.pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    sys.exit(app.exec_())