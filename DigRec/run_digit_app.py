#!/usr/bin/env python3
"""
Główny skrypt do uruchomienia aplikacji rozpoznawania cyfr
"""

import sys
import os
import subprocess

def install_requirements():
    """Instaluje wymagane pakiety"""
    print("📦 Instalowanie wymaganych pakietów...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Pakiety zainstalowane pomyślnie!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd podczas instalacji pakietów: {e}")
        return False

def check_model_exists():
    """Sprawdza czy model już istnieje"""
    return os.path.exists('digit_model.h5')

def train_model_if_needed():
    """Trenuje model jeśli nie istnieje"""
    if not check_model_exists():
        print("🤖 Model nie istnieje, trening modelu...")
        try:
            import main
            main.train_and_save_model()
            print("✅ Model wytrenowany pomyślnie!")
            return True
        except Exception as e:
            print(f"❌ Błąd podczas treningu modelu: {e}")
            return False
    else:
        print("✅ Model już istnieje, pomijam trening")
        return True

def run_app():
    """Uruchamia aplikację PyQt"""
    print("🚀 Uruchamianie aplikacji...")
    try:
        # Import tutaj aby uniknąć problemów jeśli PyQt nie jest zainstalowane
        from digit_drawing_app import main as app_main
        app_main()
        return True
    except ImportError as e:
        print(f"❌ Błąd importu PyQt5: {e}")
        print("💡 Sprawdź czy PyQt5 zostało poprawnie zainstalowane")
        return False
    except Exception as e:
        print(f"❌ Błąd podczas uruchamiania aplikacji: {e}")
        return False

def main():
    """Główna funkcja"""
    print("🎯 Aplikacja Rozpoznawania Cyfr")
    print("=" * 40)
    
    # Krok 1: Instalacja pakietów
    if not install_requirements():
        print("❌ Nie udało się zainstalować pakietów. Przerywam.")
        return
    
    print()
    
    # Krok 2: Trening modelu (jeśli potrzebny)
    if not train_model_if_needed():
        print("❌ Nie udało się przygotować modelu. Przerywam.")
        return
    
    print()
    
    # Krok 3: Uruchomienie aplikacji
    if not run_app():
        print("❌ Nie udało się uruchomić aplikacji.")
        return
    
    print("👋 Aplikacja zakończona")

if __name__ == "__main__":
    main() 