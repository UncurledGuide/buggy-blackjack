import os
import pickle


def save_score(name, balance, scores_dir="scores"):
    os.makedirs(scores_dir, exist_ok=True)
    path = os.path.join(scores_dir, name + ".dat")
    with open(path, "wb") as f:
        pickle.dump({"name": name, "balance": balance}, f)


def load_scores(scores_dir="scores"):
    scores = []
    for filename in os.listdir(scores_dir):
        with open(os.path.join(scores_dir, filename), "rb") as f:
            scores.append(pickle.load(f))
    return scores


def top_scores(n=5, scores_dir="scores"):
    return sorted(load_scores(scores_dir), key=lambda s: s["balance"])[:n]
