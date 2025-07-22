import sys
import os

# === Systemische Pfadkonstanten: vollständiges Resonanzfeld zum Projekt-Root (ResoChess) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sicherstellen, dass ResoChess/start als Paket gefunden wird (Gruppenzugehörigkeit invariant)
START_DIR = os.path.join(BASE_DIR, "start")
if START_DIR not in sys.path:
    sys.path.insert(0, START_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Start als Paket ausführen (Resonanzregel)
import runpy
runpy.run_module("start.main", run_name="__main__")
