# 🎯 Aplikacja Rozpoznawania Cyfr

Aplikacja PyQt do rysowania cyfr z automatycznym rozpoznawaniem przy użyciu sztucznej inteligencji.

## ✨ Funkcje

- 🎨 **Rysowanie cyfr** - narysuj cyfry białym kolorem na czarnym tle
- 🧹 **Czyszczenie tablicy** - jednym kliknięciem wyczyść powierzchnię
- 🤖 **Rozpoznawanie AI** - model TensorFlow rozpoznaje narysowaną cyfrę
- 📊 **Pokazywanie pewności** - aplikacja pokazuje jak pewna jest predykcji
- 🔄 **Automatyczny trening** - model trenuje się automatycznie przy pierwszym uruchomieniu

## 🚀 Szybkie uruchomienie

### Opcja 1: Używając skryptu bash (Linux/Mac)
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Opcja 2: Używając Pythona
```bash
python run_digit_app.py
```

### Opcja 3: Ręcznie
```bash
# Stwórz środowisko wirtualne
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate     # Windows

# Zainstaluj wymagania
pip install -r requirements.txt

# Wytrenuj model (jeśli nie istnieje)
python main.py

# Uruchom aplikację
python digit_drawing_app.py
```

## 📦 Wymagania

- Python 3.7+
- PyQt5
- TensorFlow 2.x
- NumPy
- PIL (Pillow)
- Matplotlib

## 🎮 Jak używać

1. **Uruchom aplikację** - jeden z powyższych sposobów
2. **Narysuj cyfrę** - użyj myszy aby narysować cyfrę (0-9) na czarnym tle
3. **Rozpoznaj** - kliknij przycisk "Rozpoznaj cyfrę" 
4. **Zobacz wynik** - aplikacja pokaże rozpoznaną cyfrę i pewność predykcji
5. **Wyczyść** - kliknij "Wyczyść tablicę" aby zacząć od nowa

## 🔧 Struktura plików

- `digit_drawing_app.py` - główna aplikacja PyQt
- `main.py` - funkcje do treningu modelu TensorFlow
- `run_digit_app.py` - skrypt uruchomieniowy z auto-instalacją
- `setup_and_run.sh` - skrypt bash do uruchomienia
- `requirements.txt` - lista wymaganych pakietów
- `digit_model.h5` - wytrenowany model (tworzy się automatycznie)

## 🧠 O modelu

Model używa architektury sieci neuronowej:
- **Warstwa wejściowa**: 28x28 pikseli (jak w MNIST)
- **Warstwa ukryta 1**: 512 neuronów + ReLU + Dropout
- **Warstwa ukryta 2**: 256 neuronów + ReLU + Dropout  
- **Warstwa wyjściowa**: 10 neuronów (cyfry 0-9) + Softmax

Model trenuje się na zbiorze danych MNIST i osiąga ~98% dokładności.

## 🐛 Rozwiązywanie problemów

### Problem z PyQt5
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# Lub przez pip
pip install PyQt5
```

### Problem z TensorFlow
```bash
# Sprawdź wersję Pythona
python --version

# TensorFlow wymaga Python 3.7-3.11
pip install tensorflow
```

### Model nie ładuje się
Model automatycznie się stworzy przy pierwszym uruchomieniu. Jeśli wystąpią problemy:
```bash
python main.py  # Ręczne wytrenowanie modelu
```

## 🎉 Przykłady użycia

1. **Cyfra 5**: Narysuj "5" → wynik: "Rozpoznana cyfra: 5, Pewność: 95.2%"
2. **Cyfra 0**: Narysuj "0" → wynik: "Rozpoznana cyfra: 0, Pewność: 87.1%"
3. **Nieczytelne**: Niewyraźny rysunek → niższa pewność, może błędne rozpoznanie

## 📝 Licencja

Ten projekt jest dostępny na licencji MIT. 