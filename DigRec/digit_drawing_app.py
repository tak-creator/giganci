import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPixmap, QFont
from PIL import Image
import tensorflow as tf
from tensorflow.keras import layers, Sequential

class DrawingWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.image = QPixmap(280, 280)  # 10x większy niż 28x28
        self.image.fill(Qt.black)  # Czarne tło
        self.drawing = False
        self.brush_size = 15
        self.last_point = QPoint()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.white, self.brush_size, Qt.SolidLine, 
                              Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            
    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawPixmap(self.rect(), self.image, self.image.rect())
        
    def clear_canvas(self):
        self.image.fill(Qt.black)
        self.update()
        
    def get_image_array(self):
        """Konwertuje narysowany obraz do tablicy numpy 28x28"""
        # Zapisz QPixmap do numpy array
        qimg = self.image.toImage()
        width = qimg.width()
        height = qimg.height()
        
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # RGBA
        
        # Konwertuj do skali szarości (weź tylko kanał alpha lub red)
        gray = arr[:, :, 0]  # Czerwony kanał
        
        # Zmień rozmiar do 28x28
        pil_img = Image.fromarray(gray)
        pil_img = pil_img.resize((28, 28), Image.LANCZOS)
        
        # Konwertuj do numpy i normalizuj
        img_array = np.array(pil_img)
        img_array = img_array.astype(np.float32) / 255.0
        
        return img_array

class DigitRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.init_ui()
        self.load_model()
        
    def init_ui(self):
        self.setWindowTitle('Rozpoznawanie Cyfr - Rysowanie')
        self.setGeometry(100, 100, 400, 500)
        
        # Główny widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout główny
        layout = QVBoxLayout()
        
        # Tytuł
        title = QLabel('Narysuj cyfrę na czarnym tle')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Widget do rysowania
        self.drawing_area = DrawingWidget()
        self.drawing_area.setFixedSize(280, 280)
        self.drawing_area.setFrameStyle(QFrame.Box)
        layout.addWidget(self.drawing_area, alignment=Qt.AlignCenter)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton('Wyczyść tablicę')
        self.clear_button.clicked.connect(self.clear_drawing)
        button_layout.addWidget(self.clear_button)
        
        self.predict_button = QPushButton('Rozpoznaj cyfrę')
        self.predict_button.clicked.connect(self.predict_digit)
        button_layout.addWidget(self.predict_button)
        
        layout.addLayout(button_layout)
        
        # Wynik predykcji
        self.result_label = QLabel('Narysuj cyfrę i kliknij "Rozpoznaj cyfrę"')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 14))
        self.result_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; margin: 10px; }")
        layout.addWidget(self.result_label)
        
        # Informacje o pewności predykcji
        self.confidence_label = QLabel('')
        self.confidence_label.setAlignment(Qt.AlignCenter)
        self.confidence_label.setFont(QFont('Arial', 10))
        layout.addWidget(self.confidence_label)
        
        main_widget.setLayout(layout)
        
    def load_model(self):
        """Ładuje lub tworzy model rozpoznawania cyfr"""
        try:
            # Spróbuj załadować zapisany model
            self.model = tf.keras.models.load_model('digit_model.h5')
            print("✅ Załadowano zapisany model")
        except:
            # Stwórz i wytrenuj nowy model
            print("🔄 Tworzenie nowego modelu...")
            self.create_and_train_model()
            
    def create_and_train_model(self):
        """Tworzy i trenuje model rozpoznawania cyfr"""
        # Stwórz model
        self.model = Sequential([
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(10, activation='softmax')
        ])
        
        self.model.compile(optimizer='adam', 
                          loss='sparse_categorical_crossentropy', 
                          metrics=['accuracy'])
        
        # Załaduj dane MNIST
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        
        # Trenuj model
        print("🏋️ Trening modelu... (może potrwać kilka minut)")
        self.result_label.setText("Trening modelu w toku... Proszę czekać...")
        QApplication.processEvents()  # Odśwież interfejs
        
        self.model.fit(x_train, y_train, 
                      epochs=15, 
                      batch_size=128, 
                      validation_data=(x_test, y_test),
                      verbose=1)
        
        # Zapisz model
        self.model.save('digit_model.h5')
        print("✅ Model wytrenowany i zapisany")
        self.result_label.setText("Model gotowy! Narysuj cyfrę i kliknij 'Rozpoznaj cyfrę'")
        
    def clear_drawing(self):
        """Czyści tablicę do rysowania"""
        self.drawing_area.clear_canvas()
        self.result_label.setText("Narysuj cyfrę i kliknij 'Rozpoznaj cyfrę'")
        self.confidence_label.setText("")
        
    def predict_digit(self):
        """Rozpoznaje narysowaną cyfrę"""
        if self.model is None:
            self.result_label.setText("Model nie jest gotowy!")
            return
            
        # Pobierz obraz z tablicy
        img_array = self.drawing_area.get_image_array()
        
        # Przygotuj do predykcji
        img_array = img_array.reshape(1, 28, 28)
        
        # Predykcja
        predictions = self.model.predict(img_array, verbose=0)
        predicted_digit = np.argmax(predictions[0])
        confidence = predictions[0][predicted_digit] * 100
        
        # Wyświetl wynik
        self.result_label.setText(f"🎯 Rozpoznana cyfra: {predicted_digit}")
        self.confidence_label.setText(f"Pewność: {confidence:.1f}%")
        
        # Wyświetl wszystkie prawdopodobieństwa
        all_probs = [(i, prob*100) for i, prob in enumerate(predictions[0])]
        all_probs.sort(key=lambda x: x[1], reverse=True)
        
        prob_text = "Wszystkie prawdopodobieństwa:\n"
        for digit, prob in all_probs[:3]:  # Pokaż top 3
            prob_text += f"Cyfra {digit}: {prob:.1f}%\n"
            
        print(prob_text)

def main():
    app = QApplication(sys.argv)
    
    # Ustaw styl aplikacji
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    """)
    
    window = DigitRecognitionApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 