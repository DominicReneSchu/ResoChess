import time
from experience_manager_v2 import merge_experience

SELFPLAY_FILE = "experience_selfplay.csv"
STOCKFISH_FILE = "experience_vs_stockfish.csv"
META_FILE = "experience_meta.csv"
MERGE_INTERVAL = 300  # Sekunden, z.B. alle 5 Minuten

def periodic_merge():
    print("[Meta] Starte periodisches Zusammenführen der Erfahrungspfade...")
    while True:
        merge_experience([SELFPLAY_FILE, STOCKFISH_FILE], META_FILE)
        print(f"[Meta] Merge abgeschlossen. Nächster Merge in {MERGE_INTERVAL} Sekunden.")
        time.sleep(MERGE_INTERVAL)

if __name__ == "__main__":
    periodic_merge()