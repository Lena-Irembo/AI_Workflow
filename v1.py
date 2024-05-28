import sys
import json
import pytesseract
import cv2
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect, QPoint

class AnnotatedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.rectangles = []
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            rect = QRect(self.start_point, self.end_point).normalized()
            self.rectangles.append(rect)
            self.drawing = False
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for rect in self.rectangles:
            painter.drawRect(rect)

        if self.drawing:
            painter.drawRect(QRect(self.start_point, self.end_point).normalized())

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Annotation Tool')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = AnnotatedLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

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

        self.image_path = None

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            self.image_label.setPixmap(QPixmap(self.image_path))
            self.save_button.setEnabled(True)

    def save_annotations(self):
        if self.image_path:
            annotations = []
            for rect in self.image_label.rectangles:
                text = self.extract_text_from_rect(rect)
                annotations.append({
                    'x': rect.x(),
                    'y': rect.y(),
                    'width': rect.width(),
                    'height': rect.height(),
                    'text': text
                })

            annotation_data = {
                'image_path': self.image_path,
                'annotations': annotations
            }

            save_path, _ = QFileDialog.getSaveFileName(self, "Save Annotations", "", "JSON Files (*.json)")
            if save_path:
                with open(save_path, 'w') as f:
                    json.dump(annotation_data, f, indent=4)

            print("Annotations saved to:", save_path)
            self.generate_workflow(annotation_data)

    def extract_text_from_rect(self, rect):
        image = Image.open(self.image_path)
        cropped_image = image.crop((rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()))
        text = pytesseract.image_to_string(cropped_image)
        return text.strip()

    def generate_workflow(self, annotation_data):
        # Define your states, actions, and events
        context = {
            "states": ["State1", "State2"],
            "actions": ["Action1", "Action2"],
            "events": ["Event1", "Event2"]
        }

        # Compare extracted text with context
        for annotation in annotation_data['annotations']:
            text = annotation['text']
            print(f"Extracted Text: {text}")

            if text in context["states"]:
                print(f"Detected State: {text}")
                # Add logic to handle state
            elif text in context["actions"]:
                print(f"Detected Action: {text}")
                # Add logic to handle action
            elif text in context["events"]:
                print(f"Detected Event: {text}")
                # Add logic to handle event
            else:
                print(f"No match found for text: {text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    sys.exit(app.exec_())
