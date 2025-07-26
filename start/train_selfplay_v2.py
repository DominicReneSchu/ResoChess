# === ResoChess Dualsystem & Meta-KI Setup ===
# Enthält:
# 1. Selfplay V2 mit Sieg-Verstärkung
# 2. Stockfish-Match auf Maximalstärke
# 3. Meta-KI: Zusammenführung beider Erfahrungsquellen

# === 1. train_selfplay_v2.py ===
import chess
import numpy as np
import csv
import os
from experience_manager_v2 import save_experience, get_result_weight

# Settings
EPISODES = 10000
SNAPSHOT_INTERVAL = 100
EXPERIENCE_FILE = "experience_selfplay.csv"
SNAPSHOT_DIR = "snapshots/selfplay/"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Dummy KI-Model (Placeholder – Replace with your NN)
class ResonanceChessAI:
    def __init__(self):
        pass

    def select_move(self, board):
        # Simple random move (replace with your model logic)
        return np.random.choice(list(board.legal_moves))

    def update(self, experience):
        # Placeholder: Insert model update logic here
        pass

def play_selfplay_episode(ai_white, ai_black):
    board = chess.Board()
    experience_log = []
    while not board.is_game_over():
        ai = ai_white if board.turn == chess.WHITE else ai_black
        move = ai.select_move(board)
        board.push(move)
        experience_log.append((board.fen(), move.uci()))
    result = board.result()
    weight = get_result_weight(result)
    return experience_log, result, weight

def main():
    ai_white = ResonanceChessAI()
    ai_black = ResonanceChessAI()

    episode_counter = 0
    experience_buffer = []

    while episode_counter < EPISODES:
        episode_counter += 1
        experience_log, result, weight = play_selfplay_episode(ai_white, ai_black)

        # Save experience with aggressive weighting
        save_experience(EXPERIENCE_FILE, experience_log, result, weight)
        experience_buffer.append((experience_log, result, weight))

        if episode_counter % SNAPSHOT_INTERVAL == 0:
            snapshot_file = os.path.join(
                SNAPSHOT_DIR, f"experience_snapshot_{episode_counter:05d}.csv")
            save_experience(snapshot_file, experience_log, result, weight)
            print(f"[Selfplay] Snapshot saved: {snapshot_file}")

    print("[Selfplay] Training finished.")

if __name__ == "__main__":
    main()

# === Weiter mit Modul 2: train_vs_stockfish.py ===
