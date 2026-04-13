"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print(f"\n{'='*50}")
    print(f"Profile: {name}")
    print(f"Prefs:   {user_prefs}")
    print(f"{'='*50}\n")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"  {rank}. {song['title']} ({song['genre']}, {song['mood']}) - Score: {score:.2f}")
        print(f"     Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

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
