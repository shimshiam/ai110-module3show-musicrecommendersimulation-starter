import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            }
            user_dict = {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            }
            score, _ = score_song(user_dict, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        user_dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_dict, song_dict)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Weights: genre 0.35, mood 0.25, energy 0.25, acousticness 0.15
    Each sub-score is 0.0–1.0, so total score is 0.0–1.0.
    """
    reasons = []

    # Genre match (binary: 0 or 1)
    genre_score = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0
    if genre_score == 1.0:
        reasons.append(f"genre match ({song['genre']})")

    # Mood match (binary: 0 or 1)
    mood_score = 1.0 if song["mood"] == user_prefs.get("mood") else 0.0
    if mood_score == 1.0:
        reasons.append(f"mood match ({song['mood']})")

    # Energy closeness: 1 - |target - actual|
    energy_score = 0.0
    if "energy" in user_prefs:
        energy_diff = abs(user_prefs["energy"] - song["energy"])
        energy_score = 1.0 - energy_diff
        reasons.append(f"energy closeness {energy_score:.0%}")

    # Acoustic fit: use raw acousticness or its inverse
    acoustic_score = 0.5  # neutral default when preference not specified
    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_score = song.get("acousticness", 0.5)
            if acoustic_score > 0.6:
                reasons.append("acoustic sound")
        else:
            acoustic_score = 1.0 - song.get("acousticness", 0.5)
            if acoustic_score > 0.6:
                reasons.append("electronic/produced sound")

    total = (0.35 * genre_score
             + 0.25 * mood_score
             + 0.25 * energy_score
             + 0.15 * acoustic_score)

    if not reasons:
        reasons.append("weak overall match")

    return (total, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
