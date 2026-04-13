"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


def format_bar(score: float, max_score: float = 4.5, width: int = 20) -> str:
    filled = int((score / max_score) * width)
    return "#" * filled + "-" * (width - filled)


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    prefs_display = (
        f"Genre: {user_prefs.get('genre', '-'):12s} "
        f"Mood: {user_prefs.get('mood', '-'):12s} "
        f"Energy: {user_prefs.get('energy', '-'):<5} "
        f"Acoustic: {'yes' if user_prefs.get('likes_acoustic') else 'no'}"
    )

    print()
    print("+" + "-" * 58 + "+")
    print(f"|  PROFILE: {name:46s}|")
    print("|  " + prefs_display.ljust(56) + "|")
    print("+" + "-" * 58 + "+")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        bar = format_bar(score)
        reasons = explanation.split("; ")

        print(f"|                                                          |")
        print(f"|  #{rank}  {song['title']:<25s} {song['artist']:<18s}|")
        print(f"|       Genre: {song['genre']:<12s}  Mood: {song['mood']:<14s}   |")
        print(f"|       Score: {score:.2f} / 4.50  [{bar}]   |")

        for reason in reasons:
            print(f"|         {reason:<49s}|")

    print(f"|                                                          |")
    print("+" + "-" * 58 + "+")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        # The upbeat pop listener — wants high energy, mainstream, and electronic
        "Party Mode": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": False,
        },
        # The late-night study session — low energy, chill, acoustic lofi
        "Study Session": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        },
        # The workout grinder — max energy, intense, electronic production
        "Gym Grinder": {
            "genre": "metal",
            "mood": "aggressive",
            "energy": 0.95,
            "likes_acoustic": False,
        },
        # The mellow evening wind-down — mid-low energy, acoustic, soulful
        "Evening Wind-Down": {
            "genre": "blues",
            "mood": "soulful",
            "energy": 0.50,
            "likes_acoustic": True,
        },
        # The road trip vibe — mid-high energy, confident, electronic
        "Road Trip": {
            "genre": "hip-hop",
            "mood": "confident",
            "energy": 0.80,
            "likes_acoustic": False,
        },
    }

    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
