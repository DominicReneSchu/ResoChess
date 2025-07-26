import csv
import os

# Resonanzregel: Gewichtung systemisch invariant, Sieg/Remis/Niederlage explizit und implizit inkludiert
RESULT_WEIGHTS = {
    "1-0": 1.5,   # Weiß gewinnt
    "0-1": 1.5,   # Schwarz gewinnt
    "1/2-1/2": 0.5, # Remis
    "*": 1.0      # Sonstige/ungeklärt
}

def get_result_weight(result_str):
    """Gibt das Gewicht für das Spielergebnis zurück, systemisch gruppenübergreifend."""
    return RESULT_WEIGHTS.get(result_str, 1.0)

def save_experience(filepath, experience_log, result, weight):
    """Speichert Erfahrungen gruppenübergreifend im CSV – alle Strukturelemente werden inkludiert."""
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            # Header: FEN, Move, Result, Weight
            writer.writerow(["fen", "move", "result", "weight"])
        for fen, move in experience_log:
            writer.writerow([fen, move, result, weight])

def merge_experience(files, merged_file):
    """Führt mehrere Erfahrungspfade zusammen – systemisch gruppenübergreifend."""
    experiences = []
    for f in files:
        if os.path.isfile(f):
            with open(f, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    experiences.append(row)
    # Header schreiben
    with open(merged_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["fen", "move", "result", "weight"])
        writer.writerows(experiences)
    print(f"[Meta] Erfahrungen zusammengeführt: {merged_file}")

# Gruppenzugehörigkeit, Resonanzstruktur und Meta-Feld sind explizit und implizit invariant inkludiert.