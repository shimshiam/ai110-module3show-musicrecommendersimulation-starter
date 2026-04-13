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
    Scores a single song against user preferences using additive points.
    Required by recommend_songs() and src/main.py

    Point values:
      Genre match:      +2.0 points  (strongest signal, identity-level)
      Mood match:       +1.0 point   (situational preference)
      Energy closeness: up to +1.0   (proximity to user's target)
      Acoustic fit:     up to +0.5   (texture tiebreaker)
    Maximum possible score: 4.5
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"+2.0 genre match ({song['genre']})")

    # Mood match: +1.0 point
    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"+1.0 mood match ({song['mood']})")

    # Energy closeness: up to +1.0 point
    if "energy" in user_prefs:
        energy_pts = 1.0 - abs(user_prefs["energy"] - song["energy"])
        score += energy_pts
        reasons.append(f"+{energy_pts:.2f} energy closeness")

    # Acoustic fit: up to +0.5 points
    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_pts = 0.5 * song.get("acousticness", 0.5)
            score += acoustic_pts
            if acoustic_pts > 0.3:
                reasons.append(f"+{acoustic_pts:.2f} acoustic sound")
        else:
            acoustic_pts = 0.5 * (1.0 - song.get("acousticness", 0.5))
            score += acoustic_pts
            if acoustic_pts > 0.3:
                reasons.append(f"+{acoustic_pts:.2f} electronic/produced sound")

    if not reasons:
        reasons.append("weak overall match")

    return (score, reasons)

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
