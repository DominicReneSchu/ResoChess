# === ResoChess Dualsystem & Meta-KI Setup ===
# Enthält:
# 1. Selfplay V2 mit Sieg-Verstärkung
# 2. Stockfish-Match auf Maximalstärke
# 3. Meta-KI: Zusammenführung beider Erfahrungsquellen

import chess
import chess.engine
import numpy as np
import csv
import os
from experience_manager_v2 import save_experience, get_result_weight

# Settings
EPISODES = 10000
STOCKFISH_PATH = "stockfish"  # binary muss im PATH liegen
STOCKFISH_SKILL = 20          # Maximalstärke
STOCKFISH_THREADS = 1
THINKING_TIME = 0.5           # Sek. pro Zug
EXPERIENCE_FILE = "experience_vs_stockfish.csv"
SNAPSHOT_DIR = "snapshots/stockfish/"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Dummy KI-Model (Placeholder – Replace mit deinem NN)
class ResonanceChessAI:
    def __init__(self):
        pass

    def select_move(self, board):
        # Simple random move (replace with your model logic)
        return np.random.choice(list(board.legal_moves))

    def update(self, experience):
        # Placeholder: Insert model update logic here
        pass

def play_vs_stockfish_episode(ai, stockfish_is_white=True):
    board = chess.Board()
    experience_log = []

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        engine.configure({"Skill Level": STOCKFISH_SKILL, "Threads": STOCKFISH_THREADS})
        while not board.is_game_over():
            if (board.turn == chess.WHITE and stockfish_is_white) or (board.turn == chess.BLACK and not stockfish_is_white):
                # Stockfish move
                result = engine.play(board, chess.engine.Limit(time=THINKING_TIME))
                move = result.move
            else:
                # KI move
                move = ai.select_move(board)
            board.push(move)
            experience_log.append((board.fen(), move.uci()))
        result = board.result()
        weight = get_result_weight(result)
        return experience_log, result, weight

def main():
    ai = ResonanceChessAI()
    episode_counter = 0

    while episode_counter < EPISODES:
        episode_counter += 1
        # Alterniere Farben für statistische Balance
        stockfish_is_white = episode_counter % 2 == 1
        experience_log, result, weight = play_vs_stockfish_episode(ai, stockfish_is_white=stockfish_is_white)
        save_experience(EXPERIENCE_FILE, experience_log, result, weight)

        if episode_counter % 100 == 0:
            snapshot_file = os.path.join(
                SNAPSHOT_DIR, f"experience_snapshot_{episode_counter:05d}.csv")
            save_experience(snapshot_file, experience_log, result, weight)
            print(f"[Stockfish] Snapshot saved: {snapshot_file}")

    print("[Stockfish] Training finished.")

if __name__ == "__main__":
    main()