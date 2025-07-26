""import os
import csv
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# === Systempfade ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")
OUTPUT_PNG = os.path.join(BASE_DIR, "result_distribution.png")
SNAPSHOT_PATTERN = re.compile(r"experience_snapshot_(\d{5})\.csv")


def get_snapshots_sorted():
    files = []
    for f in os.listdir(SNAPSHOT_DIR):
        m = SNAPSHOT_PATTERN.match(f)
        if m:
            files.append((int(m.group(1)), os.path.join(SNAPSHOT_DIR, f)))
    files.sort()
    return files


def evaluate_result_distribution():
    snapshots = get_snapshots_sorted()
    if not snapshots:
        print("Keine Snapshot-Dateien gefunden.")
        return

    snapshot_numbers = []
    success_counts = []
    failure_counts = []
    draw_counts = []

    for snap_num, snap_path in snapshots:
        result_counter = defaultdict(int)
        try:
            with open(snap_path, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    result = row.get("result", "draw").lower()
                    count = int(row.get("count", 1))
                    if result in ["success", "failure", "draw"]:
                        result_counter[result] += count
        except Exception as e:
            print(f"[Fehler] Snapshot {snap_path} konnte nicht gelesen werden: {e}")
            continue

        total = result_counter["success"] + result_counter["failure"] + result_counter["draw"]
        if total == 0:
            continue
        snapshot_numbers.append(snap_num * 100)
        success_counts.append(result_counter["success"] / total)
        failure_counts.append(result_counter["failure"] / total)
        draw_counts.append(result_counter["draw"] / total)

    if not snapshot_numbers:
        print("Keine auswertbaren Snapshots gefunden.")
        return

    # Plot
    ind = np.arange(len(snapshot_numbers))
    width = 0.6

    plt.figure(figsize=(10, 6))
    plt.bar(ind, success_counts, width, label='Erfolg', color='#4caf50')
    plt.bar(ind, draw_counts, width, bottom=success_counts, label='Remis', color='#ffc107')
    bottom_combined = np.array(success_counts) + np.array(draw_counts)
    plt.bar(ind, failure_counts, width, bottom=bottom_combined, label='Misserfolg', color='#f44336')

    plt.xticks(ind, [str(num) for num in snapshot_numbers], rotation=45)
    plt.ylabel("Anteil pro Ergebnis")
    plt.xlabel("Gesamtzahl Spiele")
    plt.title("Ergebnisverteilung pro Snapshot (KI vs Fixbot)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    print(f"[OK] Ergebnisverteilung gespeichert als '{OUTPUT_PNG}'.")


if __name__ == "__main__":
    evaluate_result_distribution()
