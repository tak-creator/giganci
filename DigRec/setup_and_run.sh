#!/bin/bash

echo "🎯 Aplikacja Rozpoznawania Cyfr"
echo "================================"

# Sprawdź czy wirtualne środowisko istnieje
if [ ! -d "venv" ]; then
    echo "📦 Tworzenie wirtualnego środowiska..."
    python3 -m venv venv
fi

# Aktywuj wirtualne środowisko
echo "🔄 Aktywacja wirtualnego środowiska..."
source venv/bin/activate

# Instaluj wymagania
echo "📥 Instalacja wymaganych pakietów..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🚀 Uruchamianie aplikacji do rysowania cyfr..."
echo "📝 Instrukcje:"
echo "   - Rysuj białe cyfry na czarnym tle"
echo "   - Użyj przycisku 'Wyczyść tablicę' aby wyczyścić"
echo "   - Użyj przycisku 'Rozpoznaj cyfrę' aby sprawdzić wynik"
echo ""

# Uruchom aplikację
python digit_drawing_app.py

echo "👋 Aplikacja zakończona" 