# EvoFormer + Decision Field

Paczka zawiera kompletny przykład dydaktyczny:
- generator danych,
- model Transformer + Decision Field,
- algorytm ewolucyjny do strojenia architektury,
- wizualizację pola decyzyjnego.

## Pliki
- `evoformer_decision_field_notebook.ipynb` – główny notebook
- `run_demo.py` – opcjonalny skrypt uruchomieniowy w formie `.py`
- `README.md` – ten opis

## Wymagania
Python 3.10+ oraz biblioteki:
- numpy
- pandas
- matplotlib
- scikit-learn
- torch

## Uruchomienie
Notebook:
1. Otwórz `evoformer_decision_field_notebook.ipynb`
2. Uruchamiaj komórki po kolei

Skrypt:
```bash
python run_demo.py
```

## Uwaga
Parametry ewolucji są ustawione tak, aby przykład był realny do uruchomienia na CPU.
Na mocniejszej maszynie można zwiększyć:
- rozmiar populacji
- liczbę generacji
- liczbę epok na osobnika