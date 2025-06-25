# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow.keras.datasets import mnist
# import time

# # Załaduj dane MNIST
# (x_train, y_train), _ = mnist.load_data()

# # Utwórz generator liczb losowych z seedem opartym na czasie
# seed = int(time.time())
# rng = np.random.default_rng(seed)
# print(f"🎲 Seed dla tego uruchomienia: {seed}")

# # Stwórz wykres
# fig, axs = plt.subplots(nrows=10, ncols=5, figsize=(7, 14))
# fig.suptitle("Po 5 losowych przykładów cyfr z zbioru MNIST")

# # Dla każdej cyfry (0-9)
# for i in range(10):
#     # Znajdź wszystkie indeksy dla cyfry i
#     idxs = np.where(y_train == i)[0]
#     # Losowo wybierz 5 różnych przykładów
#     chosen = rng.choice(idxs, size=5, replace=False)
    
#     # Wyświetl wybrane przykłady
#     for j in range(5):
#         axs[i, j].imshow(x_train[chosen[j]], cmap="gray")
#         axs[i, j].axis("off")
#         axs[i, j].set_title(f"Cyfra {i}", fontsize=8)

# plt.tight_layout()
# plt.show()

# print("✅ Wyświetlono losowe przykłady cyfr!")

###### NOCWA KOMORKA

# from tensorflow.keras.datasets import mnist
# import matplotlib.pyplot as plt
# import numpy as np

# # Załaduj dane MNIST
# (x_train, y_train), (x_test, y_test) = mnist.load_data()

# # Wybierz przykładowy obrazek przed normalizacją
# przed_norm = x_train[0]

# # Normalizacja
# po_norm = x_train[0].astype(np.float32) / 255.0

# # Zwizualizuj różnicę przed i po normalizacji
# fig, axs = plt.subplots(1, 2, figsize=(6, 3))
# axs[0].imshow(przed_norm, cmap='gray')
# axs[0].set_title("Przed normalizacją")
# axs[0].axis("off")
# axs[1].imshow(po_norm, cmap='gray')
# axs[1].set_title("Po normalizacji")
# axs[1].axis("off")
# plt.suptitle("Różnica przed i po normalizacji obrazu MNIST")
# plt.tight_layout()
# plt.show()



# ###### NOWA KOMORKA - Funkcje aktywacji

# import numpy as np
# import matplotlib.pyplot as plt

# # Zakres wartości dla funkcji aktywacji
# x = np.linspace(-5, 5, 1000)

# # Funkcje aktywacji
# def relu(x):
#     return np.maximum(0, x)

# def sigmoid(x):
#     return 1 / (1 + np.exp(-x))

# def tanh(x):
#     return np.tanh(x)

# # Wizualizacja funkcji aktywacji
# fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# # ReLU
# axs[0].plot(x, relu(x), 'b-', linewidth=2)
# axs[0].grid(True)
# axs[0].set_title('ReLU')
# axs[0].set_xlabel('x')
# axs[0].set_ylabel('ReLU(x)')
# axs[0].axhline(y=0, color='k', linestyle='-', alpha=0.3)
# axs[0].axvline(x=0, color='k', linestyle='-', alpha=0.3)

# # Sigmoid
# axs[1].plot(x, sigmoid(x), 'r-', linewidth=2)
# axs[1].grid(True)
# axs[1].set_title('Sigmoid')
# axs[1].set_xlabel('x')
# axs[1].set_ylabel('Sigmoid(x)')
# axs[1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
# axs[1].axhline(y=1, color='k', linestyle='-', alpha=0.3)
# axs[1].axhline(y=0.5, color='k', linestyle='--', alpha=0.3)
# axs[1].axvline(x=0, color='k', linestyle='-', alpha=0.3)

# # Tanh
# axs[2].plot(x, tanh(x), 'g-', linewidth=2)
# axs[2].grid(True)
# axs[2].set_title('Tanh')
# axs[2].set_xlabel('x')
# axs[2].set_ylabel('Tanh(x)')
# axs[2].axhline(y=0, color='k', linestyle='-', alpha=0.3)
# axs[2].axhline(y=1, color='k', linestyle='--', alpha=0.3)
# axs[2].axhline(y=-1, color='k', linestyle='--', alpha=0.3)
# axs[2].axvline(x=0, color='k', linestyle='-', alpha=0.3)

# plt.suptitle('Porównanie funkcji aktywacji: ReLU, Sigmoid i Tanh')
# plt.tight_layout()
# plt.show()

# ###### NOWA KOMORKA - Binaryzacja obrazu

# from tensorflow.keras.datasets import mnist
# import matplotlib.pyplot as plt
# import numpy as np

# # Załaduj dane MNIST
# (x_train, y_train), (x_test, y_test) = mnist.load_data()

# # Wybierz przykładowy obrazek
# oryginalny = x_train[0]

# # Binaryzacja - likwidacja odcieni szarości
# # Ustawienie progu - piksele powyżej 127 będą białe (1), poniżej czarne (0)
# prog = 127
# binarny = (oryginalny > prog).astype(np.float32)

# # Wizualizacja
# fig, axs = plt.subplots(1, 2, figsize=(6, 3))
# axs[0].imshow(oryginalny, cmap='gray')
# axs[0].set_title("Oryginalny obraz")
# axs[0].axis("off")
# axs[1].imshow(binarny, cmap='binary')
# axs[1].set_title("Po binaryzacji")
# axs[1].axis("off")
# plt.suptitle("Likwidacja odcieni szarości (binaryzacja)")
# plt.tight_layout()
# plt.show()





import tensorflow as tf
from tensorflow.keras import layers, Sequential
from tensorflow.keras.datasets import mnist
import numpy as np

def create_digit_recognition_model():
    """Tworzy model rozpoznawania cyfr"""
    model = Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model

def train_and_save_model():
    """Trenuje model i zapisuje go do pliku"""
    print("🔄 Tworzenie modelu...")
    model = create_digit_recognition_model()
    
    # Załaduj dane MNIST
    print("📥 Ładowanie danych MNIST...")
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalizacja danych
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    print("🏋️ Rozpoczęcie treningu modelu...")
    print("⏱️ To może potrwać kilka minut...")
    
    # Trenuj model
    history = model.fit(x_train, y_train, 
                       epochs=20, 
                       batch_size=128, 
                       validation_data=(x_test, y_test),
                       verbose=1)
    
    # Ocena modelu
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"\n✅ Trening zakończony!")
    print(f"📊 Dokładność na danych testowych: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"📉 Straty: {loss:.4f}")
    
    # Zapisz model
    model.save('digit_model.h5')
    print("💾 Model zapisany jako 'digit_model.h5'")
    
    return model, history

if __name__ == "__main__":
    # Jeśli uruchomiono ten plik bezpośrednio, wytrenuj model
    model, history = train_and_save_model()
    print("\n🎉 Model jest gotowy do użycia w aplikacji PyQt!")
    print("🚀 Uruchom aplikację PyQt poleceniem: python digit_drawing_app.py")







# ###### NOWA KOMORKA - Binaryzacja obrazu